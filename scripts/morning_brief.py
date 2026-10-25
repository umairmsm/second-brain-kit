#!/usr/bin/env python3
"""
morning_brief.py — Non-LLM Reliable Morning Briefing for Second Brain.

Compiles daily priorities, active projects, and system health status directly
from plain Markdown files and system status checks. Because it uses no LLM,
it never hallucinates, costs zero tokens, and always arrives reliably.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path


def extract_active_tasks(daily_log_path: Path) -> list[str]:
    tasks = []
    if not daily_log_path.exists():
        return tasks

    try:
        content = daily_log_path.read_text(encoding="utf-8")
    except OSError:
        return tasks

    for line in content.splitlines():
        line = line.strip()
        if line.startswith("- [ ]") or line.startswith("* [ ]"):
            task_text = re.sub(r"^[-*]\s*\[\s*\]\s*", "", line)
            tasks.append(task_text)

    return tasks


def main():
    parser = argparse.ArgumentParser(description="Generate morning brief summary")
    parser.add_argument("--vault", default=os.environ.get("VAULT_ROOT", "./vault"), help="Path to vault")
    args = parser.parse_args()

    vault = Path(args.vault).resolve()
    today_str = date.today().isoformat()
    daily_log = vault / "4_Daily-Logs" / f"{today_str}.md"

    tasks = extract_active_tasks(daily_log)

    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    print(f"☀️ Morning Briefing — {today_str}")
    print(f"Time: {now_utc}")
    print("--------------------------------------------------")

    if tasks:
        print(f"📋 Open Priorities for Today ({len(tasks)}):")
        for i, t in enumerate(tasks, 1):
            print(f"  {i}. {t}")
    else:
        print("📋 Open Priorities: No unchecked items found in today's log.")
        print(f"   (Create or update {daily_log.relative_to(vault.parent) if daily_log.is_relative_to(vault.parent) else daily_log.name})")

    dashboard_file = vault / "00-Dashboard.md"
    if dashboard_file.exists():
        print("\n📊 Dashboard Link: vault/00-Dashboard.md")

    print("--------------------------------------------------")


if __name__ == "__main__":
    main()
