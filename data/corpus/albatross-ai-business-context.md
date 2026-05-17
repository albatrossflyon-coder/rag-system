# Albatross AI — Business Context and Operations

## What Albatross AI Is

Albatross AI is an AI infrastructure company founded by Chris Brown. It builds AI-powered products and automation tools, primarily targeting:
1. Small business owners (Builder Buddy — AI chatbot for trades)
2. Developers / AI teams (MCP servers, RAG pipelines, agent infrastructure)

The company is in early revenue stage: Builder Buddy is live with Gumroad billing, omni-console dashboard is operational, and multiple automation pipelines are in production.

## Current Revenue Streams

### Builder Buddy (Primary Revenue, Live)
- Product: AI chatbot for trade professionals (electricians, plumbers, HVAC)
- URL: albatrossai.online
- Backend: Fly.io (claude-haiku-4-5-20251001, SQLite)
- Billing: Gumroad ($39/mo Pro plan)
- Gate: 5 free uses, then Gumroad payment wall
- Admin bypass: `?aai_admin=Bass2277$$`
- Status: Live and taking money. Voice integration (ElevenLabs) pending.

### Content / YouTube (Pipeline in Progress)
- Remotion videos rendering (builder-buddy-video repo)
- 4 compositions: Short1, Short2, Short3, MainVideo
- Publishing to: YouTube, LinkedIn, Facebook (via Buffer), Publer
- Goal: Drive Builder Buddy sales via educational content

### Site Receptionist (Next Product)
- Planned AI voice receptionist for small businesses
- Leverages ElevenLabs + vapi.ai
- Will follow same "free trial → paid" model as Builder Buddy

### Remote Job Island / remote-island (Future Product)
- Free job board for remote seekers, employer-side monetization
- Featured listings: $99–299/mo; sponsored slots: $49–99/post
- First niche: remote AI/automation/agent developer jobs
- Repo: remote-island (planned, not yet built)

## Infrastructure Overview

| Service | Platform | Status |
|---------|----------|--------|
| Builder Buddy backend | Fly.io | Live |
| omni-console dashboard | Vercel | Live |
| OB1 memory system | Supabase | Live |
| agentic-rust-mcp | Local / Fly.io pending | Built |
| rag-system | Local | Built (Phase 1) |
| job-hunter | Fly.io pending | Built, awaiting OAuth |

## Agent Team

Chris runs a multi-agent AI stack:
- **Claude Code (CC)** — primary coding agent, MCP wiring, infrastructure
- **Gemini (Jim)** — research, documentation, Gmail-native tasks, multi-modal
- **GitHub Copilot** — VS Code inline suggestions, paired with Claude Code

All agents share memory via OB1 (Supabase) + Obsidian vault + agent mailboxes in OB1-Brain/messages/.

## Key Financial Targets

- Short term: $500/mo MRR from Builder Buddy
- Medium term: $5k/mo MRR combined (Builder Buddy + Site Receptionist)
- Long term: Remote Job Island employer revenue

## Repository Map

| Repo | Purpose | Location |
|------|---------|----------|
| agentic-rust-mcp | Rust MCP server | C:\Repos\Albatross\agentic-rust-mcp |
| omni-console | Dashboard | C:\Repos\Albatross\omni-console |
| rag-system | RAG pipeline | C:\Repos\Albatross\rag-system |
| job-hunter | Automated resume sender | C:\Repos\Albatross\job-hunter |
| job-lead-discovery | Lead scraper pipeline | C:\Repos\Albatross\job-lead-discovery |
| career-ops | Career context + CV data | C:\Repos\Albatross\career-ops |
| builder-buddy-video | Remotion video pipeline | C:\Repos\Albatross\builder-buddy-video |
| AlbatrossAI-Website | albatrossai.online site | C:\Repos\Albatross\AlbatrossAI-Website |
