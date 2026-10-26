# second-brain-kit

> **Multi-Agent Knowledge Architecture & Ambient Assistant Kit**: A structured, plain-Markdown PARA vault shared across coding agents (Claude Code, Antigravity, Cursor) and a hardened, always-on Telegram assistant (Hermes).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/umairmsm/second-brain-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/umairmsm/second-brain-kit/actions)
[![Good First Issues](https://img.shields.io/github/issues/umairmsm/second-brain-kit/good%20first%20issue?color=brightgreen&label=Good%20First%20Issues)](https://github.com/umairmsm/second-brain-kit/issues)

---

## 1. What is this?

Most personal AI setups suffer from two chronic problems:
1. **Tool Amnesia**: Every time you launch a new coding agent session (Claude Code, Antigravity, Cursor), it starts with zero context of your ongoing projects, infrastructure, or decisions.
2. **Unsafe Chat Assistants**: Exposing terminal execution tools to an always-on remote chat bot (e.g. Telegram or Discord) creates catastrophic prompt injection risks.

**`second-brain-kit` provides a unified, air-gapped solution:**
* **The Shared PARA Vault**: Plain Markdown files with strict YAML frontmatter. All AI tools read the exact same source of truth without proprietary database locks.
* **The Multi-Agent Constitution (`00-Conventions.md`)**: Strict operational rules defining what orchestrator agents, coding executors, and ambient assistants can and cannot edit.
* **Hardened Ambient Assistant**: A production-ready blueprint for Nous Research's Hermes Agent with a strict **Read-Only / Inbox-Only MCP split**.

```
                           THE MULTI-AGENT SECOND BRAIN
    ┌────────────────────────────────────────────────────────────────────────┐
    │                        HUMAN MAINTAINER                                │
    │            (Decides P0, approves architecture & deploys)               │
    └───────────────────────────────────┬────────────────────────────────────┘
                                        │
           ┌────────────────────────────┼────────────────────────────┐
           ▼                            ▼                            ▼
  [ Orchestrator Agent ]      [ Coding Executors ]         [ Ambient Assistant ]
  (Antigravity / Gemini)     (Claude Code / Cursor)         (Telegram / Hermes)
  • AM Standups               • Deep implementations        • Voice note capture
  • Evening Rollups           • Test execution              • Read-only lookups
  • Vault git sync            • Documentation               • Writes ONLY to Inbox
           │                            │                            │
           └────────────────────────────┼────────────────────────────┘
                                        ▼
                     ┌─────────────────────────────────────┐
                     │          SHARED PARA VAULT          │
                     │  ├── 0_Inbox/ (Intake)              │
                     │  ├── 1_Projects/ (Active goals)     │
                     │  ├── 2_Areas_Infrastructure/        │
                     │  ├── 3_Areas_Operations/            │
                     │  ├── 4_Daily-Logs/ (Standups)       │
                     │  ├── 5_Resources_Knowledge/         │
                     │  └── 7_Archive/                     │
                     └─────────────────────────────────────┘
```

---

## 2. Quickstart

### 1. Initialize Your Vault
Clone the kit and copy the `vault/` starter directory into your desired location:
```bash
git clone https://github.com/umairmsm/second-brain-kit.git
cd second-brain-kit
```

### 2. Generate Your First Dashboard
Index your active projects and daily logs without any external dependencies:
```bash
python3 scripts/generate-dashboard.py --vault ./vault
```
Open `vault/00-Dashboard.md` to see your generated project table.

### 3. Deploy the Hardened Assistant (Optional)
Inspect [`hermes/`](hermes/) for production systemd unit templates and sandboxing rules:
```bash
cp hermes/config.yaml.example ~/.hermes/config.yaml
cp hermes/SOUL.md ~/.hermes/SOUL.md
```

---

## 3. Directory Layout

```
second-brain-kit/
├── vault/                              # The Plain-Markdown PARA Vault
│   ├── 00-Conventions.md               # The Constitution: rules of engagement
│   ├── 00-Dashboard.md                 # Generated project board
│   ├── AGENTS.md                       # Root agent contract
│   ├── 0_Inbox/                        # Fast capture funnel (voice notes, clips)
│   ├── 1_Projects/                     # Active projects with target dates
│   ├── 2_Areas_Infrastructure/         # Long-term topologies, backup policies
│   ├── 3_Areas_Operations/             # SRE runbooks and incident checklists
│   ├── 4_Daily-Logs/                   # Dated daily standups (YYYY-MM-DD.md)
│   ├── 5_Resources_Knowledge/          # Cheatsheets and reference guides
│   └── 7_Archive/                      # Historical records
├── hermes/                             # Always-on Telegram Assistant Setup
│   ├── SOUL.md                         # Direct, receipt-backed assistant persona
│   ├── config.yaml.example             # Sandboxed tool configuration
│   └── systemd/                        # Linux security drop-ins (NoNewPrivileges)
└── scripts/                            # Zero-Token Automation Utilities
    ├── generate-dashboard.py           # Auto-generates Markdown dashboard
    ├── homelab_watchdog.py             # Silent cron-based health monitor
    └── morning_brief.py                # Plain-text daily brief compiler
```

---

## 4. Contributing & Community

We welcome contributions! Check out our guidelines in [CONTRIBUTING.md](CONTRIBUTING.md):
* Adding platform-specific service templates (macOS launchd, Docker Compose).
* Extending `scripts/generate-dashboard.py` with custom metrics.
* Contributing specialized runbooks for common self-hosted infrastructure.

---

## 5. License

MIT License. Copyright (c) 2026 [umairmsm](https://github.com/umairmsm).
