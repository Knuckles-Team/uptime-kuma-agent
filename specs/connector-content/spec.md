# CONN-UPTIME-KUMA-AGENT-CONNECTOR-CONTENT — The connector serves its packaged content

Owner: uptime-kuma-agent. Cross-repo IDs: `SCION-CONNECTOR-CONTROL-R071`, `SCION-CONNECTOR-CONTROL-R073`.

## Purpose and user stories

The `uptime-kuma` server serves its packaged skills, prompts and ontology to any client, with no wiring of its own.

## Delivery mapping

Component: uptime-kuma-agent connector

Code: ../../uptime_kuma_agent/__init__.py

## User Scenarios & Testing

### User Story 1 - Default content (Priority: P1)

The fleet operator and the engine rely on this behaviour of `uptime-kuma-agent`: `pyproject.toml` declares `uptime-kuma` as the single `scion_sdk.connector` entry point. It is proven independently of the other stories.

**Acceptance Scenarios**:

1. **Given** the `uptime-kuma-agent` connector built from the default branch, **When** `tests/test_default_content_surfaces.py::test_default_content_surfaces` runs, **Then** `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt.

### User Story 2 - Declare access contracts for the competency reads of uptime-kuma-agent (Priority: P1)

The fleet operator and the engine rely on this behaviour of `uptime-kuma-agent`: Subsystem: connector `uptime-kuma-agent`. It is proven independently of the other stories.

**Acceptance Scenarios**:

1. **Given** the `uptime-kuma-agent` connector built from the default branch, **When** `tests/test_access_contracts.py::test_competency_contracts_certified` runs, **Then** test: `tests/test_access_contracts.py::test_competency_contracts_certified` (L2) runs the connector ontology certification and validates each recording against its contract.

### User Story 3 - Monitor list operation contract and recorded response for the cross-source mapping (Priority: P1)

The fleet operator and the engine rely on this behaviour of `uptime-kuma-agent`: Stage: connector served tool. It is proven independently of the other stories.

**Acceptance Scenarios**:

1. **Given** the `uptime-kuma-agent` connector built from the default branch, **When** `tests/test_service_health.py::test_served_health_contract` runs, **Then** l3: a served-tool test in the connector returns the recorded fields, and the conformance kit run of `scion-sdk` passes.

### User Story 4 - Add access contracts for monitors and heartbeats (Priority: P2)

The fleet operator and the engine rely on this behaviour of `uptime-kuma-agent`: Subsystem: connector `uptime-kuma-agent`. It is proven independently of the other stories.

**Acceptance Scenarios**:

1. **Given** the `uptime-kuma-agent` connector built from the default branch, **When** `tests/test_access_contracts.py::test_monitor_and_heartbeat_contracts` runs, **Then** test: `tests/test_access_contracts.py::test_monitor_and_heartbeat_contracts` (L2) runs the ontology certification.

### Edge Cases

- The vendor service is unreachable or rejects the credential: the connector returns the SDK typed error and never a partial result.
- An argument outside the documented inputs is refused with the SDK typed refusal and causes no effect on the vendor service.

## Requirements

- **FR-001**: Default content. Rows: `CONN-UPTIME-KUMA-AGENT-CONNECTOR-CONTENT-R001`.
- **FR-002**: Declare access contracts for the competency reads of uptime-kuma-agent. Rows: `CONN-UPTIME-KUMA-AGENT-CONNECTOR-CONTENT-R005`.
- **FR-003**: Monitor list operation contract and recorded response for the cross-source mapping. Rows: `CONN-UPTIME-KUMA-AGENT-CONNECTOR-CONTENT-R003`.
- **FR-004**: Add access contracts for monitors and heartbeats. Rows: `CONN-UPTIME-KUMA-AGENT-CONNECTOR-CONTENT-R002`.

## Success Criteria

- **SC-001**: `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt. Rows: `CONN-UPTIME-KUMA-AGENT-CONNECTOR-CONTENT-R001`.
- **SC-002**: Test: `tests/test_access_contracts.py::test_competency_contracts_certified` (L2) runs the connector ontology certification and validates each recording against its contract. Rows: `CONN-UPTIME-KUMA-AGENT-CONNECTOR-CONTENT-R005`.
- **SC-003**: L3: a served-tool test in the connector returns the recorded fields, and the conformance kit run of `scion-sdk` passes. Rows: `CONN-UPTIME-KUMA-AGENT-CONNECTOR-CONTENT-R003`.
- **SC-004**: Test: `tests/test_access_contracts.py::test_monitor_and_heartbeat_contracts` (L2) runs the ontology certification. Rows: `CONN-UPTIME-KUMA-AGENT-CONNECTOR-CONTENT-R002`.

## Assumptions

- The `uptime-kuma-agent` package keeps the entry point and module layout named in the rows.
- The shared SDK supplies the transport, authentication, retry and certification helpers the rows reuse.

## Why a new spec

Searched `specs/` of `uptime-kuma-agent` with `git grep` for the terms of this spec. No other spec of this repository owns the capability, so this spec owns it.

## Traceability

| Label | Rows | Design section | Test ID | Evidence |
|---|---|---|---|---|
| FR-001 | `CONN-UPTIME-KUMA-AGENT-CONNECTOR-CONTENT-R001` | plan.md Production caller chain | T-001 | tests/test_default_content_surfaces.py::test_default_content_surfaces |
| FR-002 | `CONN-UPTIME-KUMA-AGENT-CONNECTOR-CONTENT-R005` | plan.md Production caller chain | T-002 | tests/test_access_contracts.py::test_competency_contracts_certified |
| FR-003 | `CONN-UPTIME-KUMA-AGENT-CONNECTOR-CONTENT-R003` | plan.md Production caller chain | T-003 | tests/test_service_health.py::test_served_health_contract |
| FR-004 | `CONN-UPTIME-KUMA-AGENT-CONNECTOR-CONTENT-R002` | plan.md Production caller chain | T-004 | tests/test_access_contracts.py::test_monitor_and_heartbeat_contracts |
