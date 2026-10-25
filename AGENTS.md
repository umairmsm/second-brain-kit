# AGENTS.md — Universal Agent Contract for second-brain-kit

> **Any AI coding agent working in this repository reads this file first.**  
> Claude Code, Antigravity, Gemini CLI, Cursor, Codex, Cline, Windsurf, Aider — all of them.  
> The pointer files at this root (`agent.md`, `CLAUDE.md`, `GEMINI.md`, `.cursorrules`) are **symlinks to this file**.

---

## 1. Architectural Mission
`second-brain-kit` provides a multi-agent, plain-Markdown PARA knowledge system that synchronizes human intentions with coding executors (Claude Code, Antigravity) and an always-on Telegram assistant (Hermes).

## 2. Invariants & Rules
1. **Plain Markdown Only**: Never introduce proprietary binary database formats. Everything must remain readable by standard POSIX text tools and local LLMs (e.g. Ollama).
2. **Zero Secrets**: Never commit real API keys, tokens, or personal identifiers. All configuration files in this repository are sanitized examples (`.example`).
3. **Strict Assistant Sandboxing**: Remote chat assistants must never be granted arbitrary shell access or write permissions outside `vault/0_Inbox/`.

## 3. Verification Commands
```bash
# Verify Python scripts syntax
python3 -m py_compile scripts/*.py

# Test dashboard generator on starter vault
python3 scripts/generate-dashboard.py --vault ./vault

# Test morning brief generator
python3 scripts/morning_brief.py --vault ./vault

# Run metal detector scan
bash ../scan.sh .
```
