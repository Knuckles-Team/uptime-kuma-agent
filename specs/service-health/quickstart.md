# CONN-UPTIME-KUMA-AGENT-SERVICE-HEALTH — Quickstart

The shortest path that shows the served behaviour working.

```text
uv run pytest tests/test_service_health.py
```

The command starts the connector in process and calls the served tools through the MCP client. A test marked planned in `test-spec.md` runs once the code change that lands its row adds it.
