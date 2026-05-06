# Superintendent MCP Server

## Overview
A Rust-based MCP (Model Context Protocol) server built on the official rust-mcp-sdk. Provides resources and prompts for orchestrating deployments, content scheduling, and activity analysis.

## Project Structure
- **main.rs**: MCP server initialization, message loop, resource/prompt handlers
- **Dependencies**:
  - mcp v0.1.1 (official SDK)
  - tokio v1.35 (async runtime)
  - serde/serde_json (serialization)
  - reqwest v0.11 (HTTP client)
  - tracing (structured logging)

## Features

### Resources
- `system-status`: Real-time system health + deployment status
- `content-schedule`: Content calendar for all platforms (YouTube, Buffer, etc.)
- `activity-logs`: Historical activity logs with filtering

### Prompts
- `deployment-analyzer`: Analyze deployment history, failures, rollbacks
- `content-scheduler`: Generate content calendars for multiple platforms
- `activity-analyzer`: Summarize activity patterns, identify blockers

## Architecture

### Message Loop
1. Listen on stdin (MCP protocol)
2. Parse request: `{"type": "resource"|"prompt", "name": "..."}`
3. Route to handler: `handle_resource_request()` or `handle_prompt_request()`
4. Return JSON response on stdout

### Transport
- **Stdio**: Direct connection from Claude Code
- **Async**: Tokio-based async handlers
- **Logging**: Structured tracing (JSON format for production)

## Building & Running

### Build
```bash
cargo build --release
```

### Run
```bash
cargo run
```

Server starts and waits for Claude Code to connect via MCP.

## Integration Points

### External APIs (Future Stages)
- **Render**: Deployment status, logs
- **Vercel**: Frontend deployments, analytics
- **Buffer**: Social media scheduling
- **Firestore**: Historical data storage

## Stages

**Stage 1 (Foundation)**: Core MCP server + stdio transport  
**Stage 2 (Current)**: Resources + Prompts framework  
**Stage 3 (Planned)**: Full API integrations + Firestore persistence  
**Stage 4 (Planned)**: Dashboard + real-time updates  

## Development Notes

- Cargo.toml specifies 2021 edition
- Release build uses LTO for minimal binary size
- All handlers use async/await (tokio runtime)
- Environment variables via dotenv

## Testing

```bash
# Send resource request
echo '{"type":"resource","name":"system-status"}' | cargo run

# Send prompt request
echo '{"type":"prompt","name":"deployment-analyzer"}' | cargo run
```
