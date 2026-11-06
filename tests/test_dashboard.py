import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "generate-dashboard.py"
SPEC = importlib.util.spec_from_file_location("dashboard", SCRIPT)
dashboard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(dashboard)
NOW = datetime(2026, 10, 28, tzinfo=timezone.utc)


class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.vault = Path(self.temp.name)
        self.projects = self.vault / "1_Projects"
        self.projects.mkdir()

    def note(self, name, updated=None, status="Active", age=30):
        path = self.projects / (name + ".md")
        fields = f"---\ntitle: {name}\nstatus: {status}\nhealth: red\n"
        if updated is not None:
            fields += f"updatedAt: {updated}\n"
        path.write_text(fields + "---\nProject notes\n", encoding="utf-8")
        stamp = (NOW - timedelta(days=age)).timestamp()
        os.utime(path, (stamp, stamp))
        return path

    def render(self, days=14):
        return dashboard.build_dashboard(
            dashboard.scan_projects(self.projects), self.vault,
            stale_days=days, now=NOW,
        )

    def test_strict_threshold_recent_and_future_dates(self):
        for name, days in [("Old", 15), ("Boundary", 14), ("Recent", 1), ("Future", -1)]:
            self.note(name, (NOW - timedelta(days=days)).isoformat())
        text = self.render()
        self.assertEqual(text.count("⚠️ Stale"), 1)
        self.assertIn("**Old** ⚠️ Stale", text)
        self.assertIn("🔴 Red", text)
        self.assertNotIn("**Boundary** ⚠️ Stale", text)

    def test_timestamp_formats_and_mtime_fallback(self):
        cases = [
            ("2026-10-14", False),
            ("2026-10-13T23:59:59Z", True),
            ("2026-10-14T02:00:00+02:00", False),
            ("2026-10-14T00:00:00", False),
            ("2026-10-27", False),
            ("not-a-date", True),
            ("2026-02-30", True),
            ("0001-01-01T00:00:00+01:00", True),
            ("", True),
            (None, True),
        ]
        for index, (stamp, stale) in enumerate(cases):
            with self.subTest(stamp=stamp):
                path = self.note(f"Case{index}", stamp)
                self.assertEqual("⚠️ Stale" in self.render(), stale)
                path.unlink()

    def test_only_active_projects_get_badge(self):
        for status in ["blocked", "paused", "backlog", "completed"]:
            self.note(status, "2020-01-01", status=status)
        self.assertNotIn("⚠️ Stale", self.render())

    def test_mtime_fallback_can_be_recent(self):
        self.note("Recent", age=1)
        self.assertNotIn("⚠️ Stale", self.render())

    def test_cli_threshold_and_notes_are_unchanged(self):
        path = self.note("Project", datetime.now(timezone.utc).isoformat(), age=1)
        path.write_text("---\nstatus: active\n---\nKeep this note\n", encoding="utf-8")
        stamp = (datetime.now(timezone.utc) - timedelta(days=5)).timestamp()
        os.utime(path, (stamp, stamp))
        original = (path.read_bytes(), path.stat().st_mtime_ns)
        for extra, stale in [([], False), (["--stale-days", "1"], True)]:
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--vault", str(self.vault), "--quiet", *extra],
                capture_output=True, encoding="utf-8",
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            self.assertEqual("⚠️ Stale" in (self.vault / "00-Dashboard.md").read_text(encoding="utf-8"), stale)
        self.assertEqual((path.read_bytes(), path.stat().st_mtime_ns), original)

    def test_cli_rejects_negative_threshold(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--stale-days", "-1"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("--stale-days must be non-negative", result.stderr)


if __name__ == "__main__":
    unittest.main()
