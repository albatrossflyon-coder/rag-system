# MCP Protocol Overview

## What is MCP?

Model Context Protocol (MCP) is a standardized interface for AI models (Claude, etc.) to request resources and services from external systems.

## Request/Response Pattern

### Client sends:
```json
{
  "type": "resource",
  "name": "system-status"
}
```

### Server responds:
```json
{
  "type": "resource_response",
  "name": "system-status",
  "data": {...},
  "status": "success"
}
```

## Resource Types

- **system-status**: Query deployment health
- **content-schedule**: Get content calendar
- **activity-logs**: Fetch activity history

## Prompt Types

- **deployment-analyzer**: AI-powered deployment insights
- **content-scheduler**: AI-powered content planning
- **activity-analyzer**: AI-powered activity analysis

## Transport Options

1. **Stdio**: Direct stdin/stdout connection (simplest)
2. **HTTP**: REST endpoint
3. **WebSocket**: Real-time bidirectional

Superintendent MCP uses **Stdio** (Stage 1-2) with future HTTP/WS support.
