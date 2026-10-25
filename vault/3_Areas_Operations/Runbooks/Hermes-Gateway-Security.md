---
title: "Runbook: Hardened Telegram AI Assistant (Hermes) Gateway Security"
type: runbook
area: operations
status: active
tags:
  - runbook
  - hermes
  - security
  - telegram
---

# Runbook: Hardened Telegram AI Assistant Gateway Security

An always-on AI assistant with tool-calling capabilities presents a unique attack surface. Without strict containment, prompt injection from web pages or group chats could trick the agent into running destructive commands, exfiltrating credentials, or overwriting critical files.

This runbook documents the security posture required to run an autonomous Telegram AI assistant (e.g., Hermes Agent by Nous Research) safely.

---

## 1. Security Controls & Sandboxing

| Control | Enforced Setting | Purpose |
| :--- | :--- | :--- |
| **Allowed Users** | Single User ID (`<TELEGRAM_USER_ID>`). | Unauthorized DMs are dropped silently. All group chats are disabled. |
| **Tool Restrictions** | Web search, file reading, knowledge lookup. **No terminal access and no bash execution in chat.** | Eliminates arbitrary code execution risk via remote chat. |
| **Vault Access Boundary** | **Read-Only MCP** over the vault; **Write-Only MCP** restricted strictly to `0_Inbox/`. | Prevents prompt injection from corrupting existing projects, policies, or runbooks. |
| **Supply Chain Pinned** | MCP servers pinned to audited npm/git packages with `--ignore-scripts`. | Blocks malicious lifecycle scripts in dependencies. |
| **Lazy Installs Disabled** | `security.allow_lazy_installs: false` | Prevents the model from dynamically downloading unverified packages. |
| **Systemd Sandboxing** | `NoNewPrivileges=true`, `UMask=0077`, `MemoryMax=4G`, `TasksMax=512`. | OS kernel isolation limiting blast radius. |

---

## 2. MCP Filesystem Separation

The assistant accesses the Markdown vault using two distinct Model Context Protocol (MCP) servers:

```
                      TELEGRAM USER PROMPT
                               │
                               ▼
                    [ Hermes Agent Process ]
                     (Isolated Systemd Unit)
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
   [ second_brain MCP ]                  [ brain_inbox MCP ]
   - Mode: READ-ONLY                     - Mode: WRITE-ONLY
   - Scope: Entire Vault                 - Scope: 0_Inbox/ ONLY
   - Rejects writes                      - Rejects ../ path traversal
```

1. **`second_brain`**: Read-only access across `1_Projects/`, `2_Areas_Infrastructure/`, `3_Areas_Operations/`, `4_Daily-Logs/`. The agent can search and read context, but cannot modify anything.
2. **`brain_inbox`**: Write access strictly confined to `0_Inbox/`. Any attempt to write outside `0_Inbox/` or use relative directory traversal (`../`) is rejected by the server.

---

## 3. Systemd Unit Hardening

When running the gateway service on Linux, apply systemd security hardening directives:

```ini
[Unit]
Description=Hermes Telegram AI Gateway
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/hermes gateway
Restart=on-failure
RestartSec=10s

# Security Hardening
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=%h/.hermes %h/vault/0_Inbox
PrivateTmp=true
UMask=0077
MemoryMax=4G
TasksMax=512

[Install]
WantedBy=default.target
```

---

## 4. Prompt Injection & SSRF Defenses

1. **Information vs. Instruction**: The assistant's `SOUL.md` persona instructs it to treat all external web pages, emails, and fetched documents as **raw data**, never as operational instructions.
2. **SSRF Blocking**: Outbound HTTP requests from web search tools are blocked from reaching private network ranges (RFC 1918 subnets and loopback addresses).
3. **Strict Media Delivery**: The gateway only uploads files to chat if they originate within explicitly approved output directories.
