# CONN-UPTIME-KUMA-AGENT-SERVICE-HEALTH requirements

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-UPTIME-KUMA-AGENT-SERVICE-HEALTH-R001` | **Service health access.** Serve monitor ID, name, latest provider heartbeat status and check time through a read-only MCP operation. Missing heartbeat yields unknown status and no check time. Refuse malformed or oversized provider results without exposing raw configuration. Publish an SDK-readable access contract for these fields. | `tests/test_service_health.py` exercises the served tool with a synthetic provider, checks the contract and tests refusal. |
| `CONN-UPTIME-KUMA-AGENT-SERVICE-HEALTH-R002` | **Service-health tool matches the declared UptimeMonitor contract.** The served `uptime_kuma_service_health` tool returns name, status and last-check for each monitor, matching `access_contracts.ttl`. Provider of `SCION-CONNECTOR-CONTROL-R038`. | Test: `tests/test_service_health.py::test_served_health_contract` (L3). |
