# CONN-UPTIME-KUMA-AGENT-CONNECTOR-CONTENT — Requirements

Governing spec: [spec.md](spec.md).

Each row is one requirement. A row names the file it touches and the test that proves it. The generator sets each row's state in `status.json`.

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-UPTIME-KUMA-AGENT-CONNECTOR-CONTENT-R001` | **Default content.** `pyproject.toml` declares `uptime-kuma` as the single `agent_connector_sdk.connector` entry point. The server lists the packaged `skill://` and `ontology://` resources and the packaged prompts with no `content=` argument. Proving test: `tests/test_default_content_surfaces.py`. | `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt. |
| `CONN-UPTIME-KUMA-AGENT-CONNECTOR-CONTENT-R002` | **Access contract for monitors and heartbeats.** Access contract for `UptimeMonitor` (`uptime_kuma_monitors get_monitors`) and `HeartbeatStat` (`uptime_kuma_status get_heartbeats`). | Connector ontology certification passes. |
