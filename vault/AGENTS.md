# AGENTS.md — Universal Agent Guide for this Vault

> **Any AI agent working in this vault reads this file first.**  
> Claude Code, Antigravity, Gemini CLI, Cursor, Codex, Cline, Windsurf, Aider — all of them.

---

## 1. Ground Rules
1. **The Constitution**: [`00-Conventions.md`](00-Conventions.md) is the absolute authority. If you encounter contradictory notes, `00-Conventions.md` wins.
2. **Read Order**:
   1. [`00-Dashboard.md`](00-Dashboard.md): Current active projects and status.
   2. Current Daily Log: `4_Daily-Logs/YYYY-MM-DD.md`.
   3. Relevant project note in `1_Projects/`.
3. **Write Scope**:
   - Ambient or autonomous chat agents (e.g. Hermes, Telegram bots) are restricted to writing inside `0_Inbox/`.
   - Coding executors (Claude Code, Antigravity) update task checkboxes and technical runbooks upon verified completion.
   - Never edit `00-Dashboard.md` directly (run `python3 scripts/generate-dashboard.py` instead).

---

## 2. Note Structure Standards
Every note must include YAML frontmatter:
```yaml
---
title: "Document Title"
type: project | runbook | infrastructure | daily-log | resource
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - tag1
  - tag2
---
```
