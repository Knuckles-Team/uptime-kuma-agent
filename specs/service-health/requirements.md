# CONN-UPTIME-KUMA-AGENT-SERVICE-HEALTH requirements

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-UPTIME-KUMA-AGENT-SERVICE-HEALTH-R001` | **Service health access.** Serve monitor ID, name, latest provider heartbeat status and check time through a read-only MCP operation. Missing heartbeat yields unknown status and no check time. Refuse malformed or oversized provider results without exposing raw configuration. Publish an SDK-readable access contract for these fields. | `tests/test_service_health.py` exercises the served tool with a synthetic provider, checks the contract and tests refusal. |
