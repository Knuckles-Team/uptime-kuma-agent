# CONN-UPTIME-KUMA-AGENT-SERVICE-HEALTH — Test specification

Governing spec: [spec.md](spec.md).

| Test ID | Requirement | Proving test | Expected observation |
|---|---|---|---|
| T-001 | `CONN-UPTIME-KUMA-AGENT-SERVICE-HEALTH-R001` | `tests/test_service_health.py::test_served_health_contract` | `tests/test_service_health.py` exercises the served tool with a synthetic provider, checks the contract and tests refusal. |
| T-002 | `CONN-UPTIME-KUMA-AGENT-SERVICE-HEALTH-R002` | `tests/test_service_health.py::test_served_health_contract` | Test: `tests/test_service_health.py::test_served_health_contract` (L3). |

## Negative and boundary cases

Each proving test above includes the refusal or error case that its row names. A vendor outage or an unauthorised call must return the SDK typed error.

## Quality and release proof

Run `uv run pytest tests` and `pre-commit run --all-files` from the repository root. A planned test is added by the code change that lands the row.
