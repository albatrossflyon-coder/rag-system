# Chris Brown — Background, Skills, and Experience

## Professional Identity

Chris Brown is an AI infrastructure engineer and founder of Albatross AI, based in Texas. He specializes in building production-grade AI agent systems, MCP (Model Context Protocol) servers, and automation pipelines that generate real business outcomes.

He is actively seeking remote AI/automation engineering roles — specifically positions focused on AI infrastructure, agent tooling, MCP platform engineering, and developer experience for AI teams.

## Core Technical Skills

### AI & Agent Infrastructure
- Claude API (Anthropic) — prompt engineering, tool use, multi-agent orchestration
- MCP (Model Context Protocol) — built and deployed production Rust MCP servers
- Multi-agent systems — Claude Code + Gemini + Copilot running in parallel, coordinated via shared memory
- RAG (Retrieval-Augmented Generation) — hybrid BM25 + vector search, cross-encoder reranking, Ragas evaluation
- LLM deployment — model routing, prompt caching, token optimization

### Languages
- Rust — production MCP server (agentic-rust-mcp), 4-stage pipeline, SMTP integration
- Python — RAG pipelines, scraping, automation, FastAPI
- JavaScript/TypeScript — Next.js dashboards (omni-console), React components
- Bash/shell — CI/CD scripting, deployment automation

### Platforms & Infrastructure
- Fly.io — deployed production services (Builder Buddy backend, job-hunter)
- Vercel — deployed omni-console command center dashboard
- Supabase — OB1 memory system (Postgres + Edge Functions)
- GitHub Actions — CI/CD pipelines
- Docker — containerized deployments

### AI Tools & Integrations
- ElevenLabs — voice synthesis integration
- Remotion — programmatic video generation (Builder Buddy content)
- Crawl4AI / web scraping — lead discovery pipelines
- Gmail API — automated email workflows via SMTP App Password

## Key Projects Built

### agentic-rust-mcp (v0.4.0)
Production Rust MCP server with 4 stages: agency_pulse, content_check, data_vault, streaming. Integrated Gmail sender (SMTP), Firebase token validation, and reqwest HTTP client. Security: moved credentials from URL query params to headers; added 10s timeouts.

### Builder Buddy (albatrossai.online)
AI chatbot for trade professionals (electricians, plumbers, HVAC). Live product. Stack: Claude Haiku backend on Fly.io, SQLite, Gumroad billing ($39/mo), YouTube gate (5 free uses). ElevenLabs voice integration in progress.

### omni-console (Command Center Dashboard)
Next.js + Turbopack unified dashboard for all AI services — 26+ panels covering infrastructure health, YouTube metrics, AI tools, social posting status, business revenue. Deployed on Vercel: omni-console-eight.vercel.app.

### rag-system (this repo)
Production-grade RAG pipeline: hybrid BM25 + TF-IDF retrieval with RRF fusion, cross-encoder reranking, Claude-powered answer generation, Ragas evaluation. Purpose: employment — feed job listings and career context so agents can query for job matching and application drafting.

### job-hunter
Automated resume sender: scans Gmail 2x/day, Claude Haiku scores each job (threshold: 85+), auto-sends matching resume, sends daily digest. Fly.io deployment pending.

## Contact
- Email: albatrossflyon1@gmail.com
- Phone: 832-996-9554
- GitHub: github.com/albatrossflyon-coder
- Website: albatrossai.online
- Location: Texas (remote preferred)
