# Job Listings and Opportunities Index

## How to Use This File

This file tracks active job opportunities, their status, and fit scores. AI agents should query this file when asked about job leads, company opportunities, or application status.

When new job listings are discovered (via job-hunter or manual search), add them here with the format below.

## Active Opportunities

### Anthropic — AI Infrastructure / Claude Code Ecosystem
- **Relevance**: Extremely high — Chris uses Claude Code daily, built MCP servers
- **Key match**: MCP platform engineering, Claude API, agent infrastructure
- **URL**: anthropic.com/careers
- **Application angle**: agentic-rust-mcp + rag-system demonstrate production-grade Claude API usage
- **Resume version**: resume-mcp-platform
- **Status**: Not yet applied — priority target

### ElevenLabs — AI Infrastructure / Voice
- **Relevance**: High — already integrated ElevenLabs API in Builder Buddy
- **Key match**: Voice AI, real-time synthesis, API infrastructure
- **Application angle**: Voice integration work in Builder Buddy chatbot
- **Resume version**: resume-ai-engineer
- **Status**: Not yet applied

### Zapier — Automation Engineering
- **Relevance**: High — automation is Chris's core work
- **Key match**: workflow automation, API integrations, agent-triggered actions
- **Application angle**: Multi-agent orchestration pipelines, agentic-rust-mcp tools
- **Resume version**: resume-ai-engineer
- **Status**: Not yet applied

### Vercel — Developer Experience
- **Relevance**: Medium-high — deployed omni-console on Vercel, Next.js experience
- **Key match**: DevEx, frontend infrastructure, AI integrations
- **Application angle**: omni-console dashboard, Next.js + Turbopack
- **Resume version**: resume-ai-engineer
- **Status**: Not yet applied

### Cohere — NLP / Reranking Infrastructure
- **Relevance**: Medium — integrated Cohere reranking API in rag-system
- **Key match**: NLP infrastructure, retrieval systems, enterprise AI
- **Application angle**: rag-system cross-encoder integration
- **Resume version**: resume-mcp-platform
- **Status**: Not yet applied

## Evaluation Criteria for New Leads

When Claude Haiku or any agent scores a new job listing, use these criteria:

| Criterion | Weight | Notes |
|-----------|--------|-------|
| Remote-only | Required | Auto-reject if not remote |
| AI/automation domain | 30 | Core domain match |
| MCP or agent infrastructure | 25 | Strongest differentiator |
| Python or Rust | 15 | Language fit |
| Early-stage or product-focused | 15 | Better equity upside |
| Salary ≥ $120k | 15 | Minimum threshold |

**Reject if:** data annotation, Alignerr, non-remote, non-tech

## Application Templates

### Cover Letter Opening (MCP-focused)
"I've been building production MCP servers in Rust since MCP launched — agentic-rust-mcp (github.com/albatrossflyon-coder/agentic-rust-mcp) is a 4-stage pipeline with Gmail integration that I use in my own automation stack. I'm looking for a role where that depth of agent infrastructure work is the job, not a side project."

### Cover Letter Opening (AI products-focused)
"I built Builder Buddy — an AI chatbot for trade professionals (albatrossai.online) — from zero to live product with paying customers in 60 days. I'd like to bring that same bias toward shipping to [Company]."

## Recently Reviewed (Rejected)
- **Benefits All In — AI Engineer (Cincinnati)**: PASS — not remote
