# CONN-UPTIME-KUMA-AGENT-CONNECTOR-CONTENT — Design and implementation plan

Governing spec: [spec.md](spec.md).

## Architecture

`pyproject.toml` declares `uptime-kuma` as the connector identity. `create_mcp_server` resolves the packaged content of `uptime_kuma_agent` from it.
## Amendment: portable skill examples

Packaged skill examples use synthetic operator identities. They do not embed
the identity of a local account or host.
