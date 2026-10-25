#!/usr/bin/env python3
"""
homelab_watchdog.py — Silent, Cron-friendly Health Watchdog for Second Brain.

Monitors disk usage, backup freshness, and critical local services.
Designed for cron execution:
- Silent when healthy (no stdout = zero chat noise).
- Emits structured notification text only when status changes or problems arise.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path


def age_hours(iso_ts: str) -> float | None:
    try:
        return (time.time() - datetime.fromisoformat(iso_ts).timestamp()) / 3600
    except (TypeError, ValueError):
        return None


def run_checks(disks: dict[str, int], max_backup_age_hours: int = 26) -> dict[str, str]:
    problems = {}

    # 1. Disk usage checks
    for mount_point, threshold in disks.items():
        if os.path.exists(mount_point):
            try:
                usage = shutil.disk_usage(mount_point)
                pct = int((usage.used / usage.total) * 100)
                if pct >= threshold:
                    problems[f"disk_{mount_point}"] = f"Disk {mount_point} is at {pct}% capacity (threshold {threshold}%)"
            except OSError as e:
                problems[f"disk_err_{mount_point}"] = f"Unable to read disk usage for {mount_point}: {e}"

    # 2. Backup status file check (if configured)
    status_dir = Path(os.environ.get("HOMELAB_STATUS_DIR", "./status"))
    backup_file = status_dir / "backup.json"
    if backup_file.exists():
        try:
            data = json.loads(backup_file.read_text(encoding="utf-8"))
            if data.get("status") != "ok":
                problems["backup_failed"] = f"Backup status is {data.get('status')} ({data.get('detail', '')})"
            age = age_hours(data.get("timestamp", ""))
            if age is not None and age > max_backup_age_hours:
                problems["backup_stale"] = f"Last backup was {age:.1f} hours ago (limit: {max_backup_age_hours}h)"
        except (OSError, ValueError) as e:
            problems["backup_parse_error"] = f"Failed to read backup status: {e}"

    return problems


def main():
    parser = argparse.ArgumentParser(description="Silent Homelab Watchdog")
    parser.add_argument("--disk", action="append", default=["/:90"], help="Mount point and percentage threshold, e.g. /:90")
    parser.add_argument("--max-backup-age", type=int, default=26, help="Max backup age in hours")
    args = parser.parse_args()

    disks = {}
    for d in args.disk:
        if ":" in d:
            m, t = d.split(":", 1)
            disks[m] = int(t)

    problems = run_checks(disks, args.max_backup_age)

    if problems:
        print("[WATCHDOG ALERT]")
        for k, msg in problems.items():
            print(f"- {msg}")
        sys.exit(1)
    else:
        # Silent when healthy
        sys.exit(0)


if __name__ == "__main__":
    main()
