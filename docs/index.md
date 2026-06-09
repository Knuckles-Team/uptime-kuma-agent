# uptime-kuma-agent

Uptime Kuma **MCP Server + A2A Agent** for the agent-utilities ecosystem — a typed,
deterministic tool surface over the Uptime Kuma monitoring API.

!!! info "Official documentation"
    This site is the canonical reference for `uptime-kuma-agent`, maintained alongside
    every release.

[![PyPI](https://img.shields.io/pypi/v/uptime-kuma-agent)](https://pypi.org/project/uptime-kuma-agent/)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
[![License](https://img.shields.io/pypi/l/uptime-kuma-agent)](https://github.com/Knuckles-Team/uptime-kuma-agent/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/source-GitHub-181717?logo=github)](https://github.com/Knuckles-Team/uptime-kuma-agent)

## Overview

`uptime-kuma-agent` wraps the [Uptime Kuma](https://github.com/louislam/uptime-kuma)
monitoring API with consolidated, action-routed MCP tools and ships an integrated
Pydantic AI agent. It provides:

- **Action-routed MCP tools** — `uptime_kuma_monitors` and `uptime_kuma_status`
  consolidate the monitor lifecycle and status/heartbeat surface into two togglable
  tools, minimizing context overhead for language models.
- **An integrated A2A agent** (`uptime-agent` console script) — a Pydantic AI graph
  agent with a web UI that calls the MCP server over `streamable-http`.
- **Enterprise governance** inherited from `agent-utilities` — OpenTelemetry tracing,
  Eunomia policy enforcement, and OIDC token delegation.

Authentication is configured entirely from the environment, and each tool module
remains inactive when its toggle is disabled.

## Explore the documentation

<div class="grid cards" markdown>

- :material-rocket-launch: **[Installation](installation.md)** — pip, source, extras, and the prebuilt Docker image.
- :material-server-network: **[Deployment](deployment.md)** — run the MCP server and agent, Docker Compose, Caddy + Technitium.
- :material-console: **[Usage](usage.md)** — the MCP tools, the `UptimeKumaApi` client, and the agent CLI.
- :material-database-cog: **[Backing Platform](platform.md)** — deploy Uptime Kuma with Docker.
- :material-tag-multiple: **[Overview](overview.md)** — ecosystem role and enterprise readiness.
- :material-sitemap: **[Concepts](concepts.md)** — the `CONCEPT:UKA-*` registry.

</div>

## Quick start

```bash
pip install "uptime-kuma-agent[mcp]"
uptime-mcp                       # stdio MCP server (default transport)
```

Connect it to an Uptime Kuma instance:

```bash
export UPTIME_KUMA_URL=http://localhost:3001
export UPTIME_KUMA_USERNAME=admin
export UPTIME_KUMA_PASSWORD=your_password_here
uptime-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

See **[Installation](installation.md)** and **[Deployment](deployment.md)** for the
full matrix (PyPI extras, Docker image, all transports, the agent server, reverse
proxy, DNS).
