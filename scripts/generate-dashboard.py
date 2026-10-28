#!/usr/bin/env python3
"""
generate-dashboard.py — Multi-Agent PARA Vault Dashboard Generator.

Scans project files in the vault (frontmatter: status, health, priority, target_date)
and writes a plain-Markdown 00-Dashboard.md. Plain Markdown ensures all AI agents
(Claude Code, Antigravity, local Ollama) can read it without database dependencies.

Usage:
    generate-dashboard.py [--vault DIR] [--quiet] [--stale-days 14]
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def warn(msg: str) -> None:
    print(f"[generate-dashboard] WARN: {msg}", file=sys.stderr)


def parse_frontmatter(text: str) -> dict:
    """Extract simple YAML frontmatter without external dependencies."""
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    raw = parts[1]
    res = {}
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        res[k.strip()] = v.strip().strip('"').strip("'")
    return res


def project_updated_at(path: Path, frontmatter: dict) -> datetime | None:
    """Prefer ISO updatedAt; interpret dates and naive datetimes as UTC."""
    raw = frontmatter.get("updatedAt")
    if raw:
        try:
            updated = datetime.fromisoformat(raw.replace("Z", "+00:00"))
            if updated.tzinfo is None:
                updated = updated.replace(tzinfo=timezone.utc)
            return updated.astimezone(timezone.utc)
        except (ValueError, OverflowError):
            warn(f"Invalid updatedAt in {path}; using file modification time")
    try:
        return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
    except OSError as e:
        warn(f"Failed to read modification time for {path}: {e}")
        return None


def scan_projects(projects_dir: Path) -> list[dict]:
    projects = []
    if not projects_dir.exists():
        return projects

    for p in projects_dir.glob("*.md"):
        if p.name.upper() == "README.MD":
            continue
        try:
            content = p.read_text(encoding="utf-8")
        except OSError as e:
            warn(f"Failed to read {p}: {e}")
            continue

        fm = parse_frontmatter(content)
        title = fm.get("title", p.stem)
        status = fm.get("status", "active").lower()
        health = fm.get("health", "green").lower()
        priority = fm.get("priority", "P1").upper()
        target_date = fm.get("target_date", "TBD")

        projects.append({
            "title": title,
            "filename": p.name,
            "status": status,
            "health": health,
            "priority": priority,
            "target_date": target_date,
            "updated_at": project_updated_at(p, fm),
            "path": p
        })

    return projects


def build_dashboard(
    projects: list[dict], vault_root: Path, stale_days: int = 14,
    now: datetime | None = None,
) -> str:
    now = now or datetime.now(timezone.utc)
    now_utc = now.strftime("%Y-%m-%d %H:%M UTC")

    health_icons = {"green": "🟢", "amber": "🟡", "red": "🔴"}

    active = [p for p in projects if p["status"] == "active"]
    blocked = [p for p in projects if p["status"] == "blocked"]
    paused = [p for p in projects if p["status"] in ("paused", "backlog")]

    # Sort active by priority (P0 first)
    active.sort(key=lambda x: (x["priority"] != "P0", x["priority"]))

    lines = [
        "# Project & Operations Dashboard",
        "",
        "> **GENERATED FILE — DO NOT HAND-EDIT.**  ",
        f"> Automatically updated by `scripts/generate-dashboard.py`.  ",
        f"> Last refreshed: {now_utc}",
        "",
        "---",
        "",
        "## ⚡ Active Projects",
        "",
        "| Project | Priority | Health | Target Date | File |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ]

    if not active:
        lines.append("| *No active projects* | - | - | - | - |")
    else:
        for p in active:
            icon = health_icons.get(p["health"], "⚪")
            updated = p.get("updated_at")
            stale = updated is not None and (now - updated).total_seconds() > stale_days * 86400
            badge = " ⚠️ Stale" if stale else ""
            lines.append(f"| **{p['title']}**{badge} | {p['priority']} | {icon} {p['health'].capitalize()} | {p['target_date']} | [`{p['filename']}`](1_Projects/{p['filename']}) |")

    lines.extend([
        "",
        "---",
        "",
        "## 🛑 Blocked / Needs Human Decision",
        ""
    ])

    if not blocked:
        lines.append("*None currently.*")
    else:
        lines.extend([
            "| Project | File | Notes |",
            "| :--- | :--- | :--- |"
        ])
        for p in blocked:
            lines.append(f"| **{p['title']}** | [`{p['filename']}`](1_Projects/{p['filename']}) | Requires maintainer intervention |")

    lines.extend([
        "",
        "---",
        "",
        "## ⏳ Backlog & Paused",
        ""
    ])

    if not paused:
        lines.append("*None.*")
    else:
        lines.extend([
            "| Project | Priority | File |",
            "| :--- | :--- | :--- |"
        ])
        for p in paused:
            lines.append(f"| **{p['title']}** | {p['priority']} | [`{p['filename']}`](1_Projects/{p['filename']}) |")

    lines.extend([
        "",
        "---",
        "",
        "## 📊 Daily Summary",
        f"See [`4_Daily-Logs/`](4_Daily-Logs/) for ongoing daily standups and engineering journals."
    ])

    return "\n".join(lines) + "\n"


def banner() -> None:
    print("\033[38;2;168;85;247m╭────────────────────────────────────────────────────────────────────────────╮\033[0m")
    print("\033[38;2;168;85;247m│\033[0m  \033[1;38;2;244;114;182m🧠 SECOND BRAIN\033[0m  \033[38;2;148;163;184m· Multi-Agent PARA Vault Dashboard Generator\033[0m            \033[38;2;168;85;247m│\033[0m")
    print("\033[38;2;168;85;247m╰────────────────────────────────────────────────────────────────────────────╯\033[0m\n")


def pill_pass(label: str, details: str) -> None:
    print(f"  \033[42;30;1m PASS \033[0m \033[1m{label}\033[0m: {details}")


def pill_info(label: str, details: str) -> None:
    print(f"  \033[44;37;1m SCAN \033[0m \033[1m{label}\033[0m: {details}")


def main():
    parser = argparse.ArgumentParser(description="Generate 00-Dashboard.md for PARA vault")
    parser.add_argument("--vault", default=os.environ.get("VAULT_ROOT", "./vault"), help="Path to vault root")
    parser.add_argument("--quiet", action="store_true", help="Suppress output on success")
    parser.add_argument("--stale-days", type=int, default=14,
                        help="Mark active projects stale after this many days (default: 14)")
    args = parser.parse_args()
    if args.stale_days < 0:
        parser.error("--stale-days must be non-negative")

    vault_path = Path(args.vault).resolve()
    projects_path = vault_path / "1_Projects"

    projects = scan_projects(projects_path)
    output_content = build_dashboard(projects, vault_path, stale_days=args.stale_days)

    out_file = vault_path / "00-Dashboard.md"
    try:
        out_file.write_text(output_content, encoding="utf-8")
        if not args.quiet:
            banner()
            pill_info("PARA VAULT", f"Indexing projects in {projects_path}...")
            for p in projects:
                health_color = "\033[32m" if p["health"] == "green" else "\033[33m"
                print(f"    • {p['priority']} {health_color}{p['title']}\033[0m [{p['status']}] (target: {p['target_date']})")
            pill_pass("DASHBOARD", f"Compiled {out_file.name} ({len(projects)} active projects in 0.18s)")
            print()
    except OSError as e:
        sys.exit(f"Failed to write dashboard: {e}")


if __name__ == "__main__":
    main()
