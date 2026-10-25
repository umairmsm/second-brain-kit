# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-10-26

### Added
- **Multi-Agent PARA Vault**: Starter skeleton with `0_Inbox/`, `1_Projects/`, `2_Areas_Infrastructure/`, `3_Areas_Operations/`, `4_Daily-Logs/`, `5_Resources_Knowledge/`, and `7_Archive/`.
- **The Constitution (`00-Conventions.md`)**: Shared governance rules for multi-agent workflows.
- **Hardened Assistant Architecture (`hermes/`)**:
  - `SOUL.md`: Receipt-backed persona template.
  - `config.yaml.example`: Sandboxed tool configuration with read-only / inbox-only MCP split.
  - `systemd/`: Linux security drop-ins (`NoNewPrivileges=true`, `UMask=0077`).
- **Automation Utilities (`scripts/`)**:
  - `generate-dashboard.py`: Zero-dependency Markdown dashboard generator.
  - `homelab_watchdog.py`: Silent cron-friendly health monitor.
  - `morning_brief.py`: Plain-text morning briefing generator.
