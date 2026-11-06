# CONN-UPTIME-KUMA-AGENT-CONNECTOR-CONTENT — Test specification

Governing spec: [spec.md](spec.md).

| Test ID | Requirement | Proving test | Expected observation |
|---|---|---|---|
| T-001 | `CONN-UPTIME-KUMA-AGENT-CONNECTOR-CONTENT-R001` | `tests/test_default_content_surfaces.py::test_default_content_surfaces` | `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt. |
| T-002 | `CONN-UPTIME-KUMA-AGENT-CONNECTOR-CONTENT-R005` | `tests/test_access_contracts.py::test_competency_contracts_certified` (planned) | Test: `tests/test_access_contracts.py::test_competency_contracts_certified` (L2) runs the connector ontology certification and validates each recording against its contract. |
| T-003 | `CONN-UPTIME-KUMA-AGENT-CONNECTOR-CONTENT-R003` | `tests/test_service_health.py::test_served_health_contract` | L3: a served-tool test in the connector returns the recorded fields, and the conformance kit run of `scion-sdk` passes. |
| T-004 | `CONN-UPTIME-KUMA-AGENT-CONNECTOR-CONTENT-R002` | `tests/test_access_contracts.py::test_monitor_and_heartbeat_contracts` (planned) | Test: `tests/test_access_contracts.py::test_monitor_and_heartbeat_contracts` (L2) runs the ontology certification. |
| T-005 | `CONN-UPTIME-KUMA-AGENT-CONNECTOR-CONTENT-R006` | `tests/unit/test_auth_timeout.py::test_default_timeout_covers_a_slow_login` | With no override the client is built with a 120 second timeout and the prompt no longer lists the retired action tools. |

## Negative and boundary cases

Each proving test above includes the refusal or error case that its row names. A vendor outage or an unauthorised call must return the SDK typed error.

## Quality and release proof

Run `uv run pytest tests` and `pre-commit run --all-files` from the repository root. A planned test is added by the code change that lands the row.
