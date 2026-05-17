# Agent Roles and Workflows

## The Albatross AI Agent Stack

Chris Brown runs a polyglot AI agent team where each agent has a defined role and specialty. Agents share state via the OB1 memory system and communicate via agent mailboxes.

## Agent Profiles

### Claude Code (CC) — Primary Infrastructure Agent
- **Role**: Primary coding agent, architecture, MCP wiring, deployment
- **Runs in**: Claude Code CLI (terminal), Desktop app, IDE extension
- **Strengths**: Deep codebase understanding, multi-file edits, tool use, MCP server wiring
- **Memory**: Reads/writes OB1 (Supabase), Obsidian vault, project memory files
- **Session pattern**: GSM (get session memory) → read mailbox → work → capture_thought + Obsidian write
- **Mailbox**: G:\Other computers\My Laptop\Desktop\OB1-Brain\messages\to-claude.md

### Jim (Gemini) — Research and Documentation Agent
- **Role**: Research, documentation, multi-modal tasks, Gmail-native workflows
- **Runs in**: Gemini Desktop, Gemini CLI (terminal)
- **Strengths**: Gmail reading (native), long context, documentation generation, RAG-style research
- **Weaknesses**: Cursor free plan blocks premium models; Gemini CLI had red error (needs fix)
- **Mailbox**: G:\Other computers\My Laptop\Desktop\OB1-Brain\messages\to-jim.md

### GitHub Copilot — Inline Coding Assistant
- **Role**: VS Code inline suggestions, code completion, quick refactors
- **Runs in**: VS Code (Acer machine), Rockport 1 (partially broken)
- **Memory issue**: Copilot was saving to OneDrive (wrong). Fix: All memory/notes go to Google Drive (G:\) and Obsidian vault.
- **Mailbox**: G:\Other computers\My Laptop\Desktop\OB1-Brain\messages\to-copilot.md

## Memory System Architecture

### OB1 (Open Brain 1) — Primary Shared Memory
- Backend: Supabase (Postgres + Edge Functions)
- URL: https://kydqbupmktfhawizspdt.supabase.co/functions/v1/open-brain-mcp
- GSM protocol: `list_thoughts(limit:20)` at session start
- Session end: `capture_thought` to OB1 AND write .md to Obsidian vault
- Fallback: G:\Other computers\My Laptop\Desktop\OB1-Brain\thoughts\ (highest numbered file)

### Obsidian Vault — Local Backup
- Path: G:\Other computers\My Laptop\Universal Brain Vault\
- Port: 27123 (Obsidian must be open)
- Purpose: Session logs, fallback when Supabase is down

### Agent Mailboxes
- Path: G:\Other computers\My Laptop\Desktop\OB1-Brain\messages\
- Files: to-claude.md, to-jim.md, to-copilot.md
- Protocol: Before starting any coordinated session, check mailbox. After session, write summary to mailbox for other agents.

## Standard Session Workflow

1. **GSM** — read OB1 via list_thoughts(limit:20)
2. **Open omni-console** — https://omni-console-eight.vercel.app (check service health)
3. **Read mailbox** — check to-claude.md for coordination messages
4. **Work** — execute tasks per session goal
5. **Session end** — capture_thought to OB1 AND write session log to Obsidian vault

## Parallel Agent Sessions

Claude Code supports multiple parallel terminal sessions. Each session is independent with its own context. Sessions can coordinate via:
- OB1 mailboxes (async messaging)
- Shared git repo state
- Verbally relayed messages from Chris

## Key Automation Pipelines

### Job Discovery Pipeline
1. YC Jobs / company ATS pages scraped by crawl4ai (job-lead-discovery)
2. Leads filtered by PERSONA.md criteria (remote, AI/automation, no annotation)
3. Digest emailed via send_gmail MCP tool in agentic-rust-mcp
4. Scored by Claude Haiku in job-hunter; auto-sends resume if score ≥ 85

### Content Pipeline
1. Chris records voice (phone memo)
2. Remotion assembles video (images + script + voiceover) in builder-buddy-video
3. Rendered video pushed to YouTube, LinkedIn, Facebook via Buffer/Publer

### Memory Pipeline
1. All agent activity ends with capture_thought (Supabase) + Obsidian write
2. Session summaries stored in OB1 as type:session-summary
3. Decisions and architecture stored in project memory files (C:\Users\albat\.claude\projects\...)
