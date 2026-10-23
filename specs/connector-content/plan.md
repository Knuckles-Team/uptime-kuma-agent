# CONN-UPTIME-KUMA-AGENT-CONNECTOR-CONTENT — Design and implementation plan

Governing spec: [spec.md](spec.md).

## Architecture

`pyproject.toml` declares `uptime-kuma` as the connector identity. `create_mcp_server` resolves the packaged content of `uptime_kuma_agent` from it.
