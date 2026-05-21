# Uptime Kuma Agent - A2A | AG-UI | MCP

![PyPI - Version](https://img.shields.io/pypi/v/uptime-kuma-agent)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
![PyPI - Downloads](https://img.shields.io/pypi/dd/uptime-kuma-agent)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/uptime-kuma-agent)
![GitHub forks](https://img.shields.io/github/forks/Knuckles-Team/uptime-kuma-agent)
![GitHub contributors](https://img.shields.io/github/contributors/Knuckles-Team/uptime-kuma-agent)
![PyPI - License](https://img.shields.io/pypi/l/uptime-kuma-agent)
![GitHub](https://img.shields.io/github/license/Knuckles-Team/uptime-kuma-agent)

![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/uptime-kuma-agent)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Knuckles-Team/uptime-kuma-agent)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/Knuckles-Team/uptime-kuma-agent)
![GitHub issues](https://img.shields.io/github/issues/Knuckles-Team/uptime-kuma-agent)

![GitHub top language](https://img.shields.io/github/languages/top/Knuckles-Team/uptime-kuma-agent)
![GitHub language count](https://img.shields.io/github/languages/count/Knuckles-Team/uptime-kuma-agent)
![GitHub repo size](https://img.shields.io/github/repo-size/Knuckles-Team/uptime-kuma-agent)
![GitHub repo file count (file type)](https://img.shields.io/github/directory-file-count/Knuckles-Team/uptime-kuma-agent)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/uptime-kuma-agent)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/uptime-kuma-agent)

*Version: 0.11.1*

## Overview

**Uptime Kuma Agent MCP Server + A2A Agent**

Agent for interacting with Uptime Kuma API

This repository is actively maintained - Contributions are welcome!

## MCP

### Using as an MCP Server

The MCP Server can be run in two modes: `stdio` (for local testing) or `http` (for networked access).

#### Environment Variables

*   `UPTIME_KUMA_URL`: The URL of the target service.
*   `UPTIME_KUMA_TOKEN`: The API token or access token.

#### Run in stdio mode (default):
```bash
export UPTIME_KUMA_URL="http://localhost:8080"
export UPTIME_KUMA_TOKEN="your_token"
uptime-kuma-mcp --transport "stdio"
```

#### Run in HTTP mode:
```bash
export UPTIME_KUMA_URL="http://localhost:8080"
export UPTIME_KUMA_TOKEN="your_token"
uptime-kuma-mcp --transport "http" --host "0.0.0.0" --port "8000"
```

## A2A Agent

### Run A2A Server
```bash
export UPTIME_KUMA_URL="http://localhost:8080"
export UPTIME_KUMA_TOKEN="your_token"
uptime-kuma-agent --provider openai --model-id gpt-4o --api-key sk-...
```

## Security & Governance

This project is built on [`agent-utilities`](https://github.com/Knuckles-Team/agent-utilities), inheriting enterprise-grade security and governance features.

### Authentication & Authorization
| Feature | Description |
|---------|-------------|
| **OIDC Token Delegation** | RFC 8693 token exchange for user-context propagation from A2A → MCP |
| **Eunomia Policies** | Fine-grained, policy-driven tool authorization (`none`, `embedded`, `remote`) |
| **Scoped Credentials** | Tools execute with the caller's scoped identity where possible |
| **3LO / OAuth / API Token** | Multiple auth strategies with graceful fallback |

### Eunomia Policy Enforcement
Eunomia provides a policy enforcement point for all tool calls:
- **Embedded mode**: Load local `mcp_policies.json` for role-based access, sensitivity gating, and audit logging
- **Remote mode**: Forward authorization decisions to a central Eunomia policy server for multi-agent governance
- Enable via CLI: `--eunomia-type embedded --eunomia-policy-file mcp_policies.json`

### Runtime Protections
| Protection | Description |
|------------|-------------|
| **Tool Guard** | Sensitivity detection with human-in-the-loop approval gating |
| **Prompt Injection Defense** | Input scanning and repetition/loop guards |
| **Content Filtering** | Output schema enforcement and cost budget controls |
| **Stuck Loop Detection** | Automatic detection and recovery from agent loops |
| **Context Limit Warnings** | Proactive alerts before context window exhaustion |

### Graph Agent Architecture
The A2A agent uses `pydantic-graph` orchestration with:
- **RouterNode**: Lightweight classifier that routes queries to specialized domains
- **DomainNode**: Focused executor with only relevant tools loaded, preventing tool hallucination
- **Approval Gates**: Policy-driven approval workflows before sensitive operations
- **Usage Guards**: Budget and rate limiting enforcement

> **Production Recommendation**: Enable `--eunomia-type embedded` (or `remote`) + OIDC delegation + containerized deployment. See [`agent-utilities` documentation](https://github.com/Knuckles-Team/agent-utilities) for full policy configuration.

## Docker

### Build

```bash
docker build -t uptime-kuma-agent .
```

### Run MCP Server

```bash
docker run -d \
  --name uptime-kuma-agent \
  -p 8000:8000 \
  -e TRANSPORT=http \
  -e UPTIME_KUMA_URL="http://your-service:8080" \
  -e UPTIME_KUMA_TOKEN="your_token" \
  knucklessg1/uptime-kuma-agent:latest
```

### Deploy with Docker Compose

```yaml
services:
  uptime-kuma-agent:
    image: knucklessg1/uptime-kuma-agent:latest
    environment:
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=http
      - UPTIME_KUMA_URL=http://your-service:8080
      - UPTIME_KUMA_TOKEN=your_token
    ports:
      - 8000:8000
```

#### Configure `mcp.json` for AI Integration (e.g. Claude Desktop)

```json
{
  "mcpServers": {
    "uptime-kuma": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "uptime-kuma-agent",
        "uptime-kuma-mcp"
      ],
      "env": {
        "UPTIME_KUMA_URL": "http://your-service:8080",
        "UPTIME_KUMA_TOKEN": "your_token"
      }
    }
  }
}
```

## Install Python Package

```bash
python -m pip install uptime-kuma-agent
```
```bash
uv pip install uptime-kuma-agent
```

## Repository Owners

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=Knucklessg1&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/Knucklessg1)
![GitHub User's stars](https://img.shields.io/github/stars/Knucklessg1)


## MCP Configuration Examples

### stdio (recommended for local development)
```json
{
  "mcpServers": {
    "uptime": {
      "command": ".venv/bin/uptime-mcp",
      "args": [],
      "env": {
        "UPTIME_KUMA_URL": "",
        "UPTIME_KUMA_TOKEN": ""
}
    }
  }
}
```

### Streamable HTTP (recommended for production)
```json
{
  "mcpServers": {
    "uptime": {
      "url": "http://localhost:8080/uptime-mcp/mcp"
    }
  }
}
```
## Available MCP Tools

This server utilizes dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

| Tool Name | Description |
|-----------|-------------|
| `uptime_kuma_monitors` | Consolidated Action-Routed tool for monitors. Methods: get_monitors, get_monitor, add_monitor, edit_monitor, delete_monitor, pause_monitor, resume_monitor |
| `uptime_kuma_status` | Consolidated Action-Routed tool for status. Methods: get_heartbeats, info |
