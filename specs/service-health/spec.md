# CONN-UPTIME-KUMA-AGENT-SERVICE-HEALTH — Service health access

Owner: uptime-kuma-agent. Cross-repo ID: `SCION-CONNECTOR-CONTROL-R038`.

## Purpose and user stories

A caller reads monitor health and its last observed check through one tool.

## Why a new spec

The connector-content and connector-identity specs cover packaging and naming,
not monitor health or its access contract.

## Delivery mapping

Component: uptime-kuma-agent connector

Code: ../../uptime_kuma_agent/__init__.py

## User Scenarios & Testing

### User Story 1 - Service health access (Priority: P1)

The fleet operator and the engine rely on this behaviour of `uptime-kuma-agent`: Serve monitor ID, name, latest provider heartbeat status and check time through a read-only MCP operation. It is proven independently of the other stories.

**Acceptance Scenarios**:

1. **Given** the `uptime-kuma-agent` connector built from the default branch, **When** `tests/test_service_health.py::test_served_health_contract` runs, **Then** `tests/test_service_health.py` exercises the served tool with a synthetic provider, checks the contract and tests refusal.

### User Story 2 - Service-health tool matches the declared UptimeMonitor contract (Priority: P1)

The fleet operator and the engine rely on this behaviour of `uptime-kuma-agent`: The served `uptime_kuma_service_health` tool returns name, status and last-check for each monitor, matching `access_contracts.ttl`. It is proven independently of the other stories.

**Acceptance Scenarios**:

1. **Given** the `uptime-kuma-agent` connector built from the default branch, **When** `tests/test_service_health.py::test_served_health_contract` runs, **Then** test: `tests/test_service_health.py::test_served_health_contract` (L3).

### Edge Cases

- The vendor service is unreachable or rejects the credential: the connector returns the SDK typed error and never a partial result.
- An argument outside the documented inputs is refused with the SDK typed refusal and causes no effect on the vendor service.

## Requirements

- **FR-001**: Service health access. Rows: `CONN-UPTIME-KUMA-AGENT-SERVICE-HEALTH-R001`.
- **FR-002**: Service-health tool matches the declared UptimeMonitor contract. Rows: `CONN-UPTIME-KUMA-AGENT-SERVICE-HEALTH-R002`.

## Success Criteria

- **SC-001**: `tests/test_service_health.py` exercises the served tool with a synthetic provider, checks the contract and tests refusal. Rows: `CONN-UPTIME-KUMA-AGENT-SERVICE-HEALTH-R001`.
- **SC-002**: Test: `tests/test_service_health.py::test_served_health_contract` (L3). Rows: `CONN-UPTIME-KUMA-AGENT-SERVICE-HEALTH-R002`.

## Assumptions

- The `uptime-kuma-agent` package keeps the entry point and module layout named in the rows.
- The shared SDK supplies the transport, authentication, retry and certification helpers the rows reuse.

## Traceability

| Label | Rows | Design section | Test ID | Evidence |
|---|---|---|---|---|
| FR-001 | `CONN-UPTIME-KUMA-AGENT-SERVICE-HEALTH-R001` | plan.md Production caller chain | T-001 | tests/test_service_health.py::test_served_health_contract |
| FR-002 | `CONN-UPTIME-KUMA-AGENT-SERVICE-HEALTH-R002` | plan.md Production caller chain | T-002 | tests/test_service_health.py::test_served_health_contract |
