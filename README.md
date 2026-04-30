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

*Version: 0.1.9*

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
