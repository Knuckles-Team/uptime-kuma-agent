# CONN-UPTIME-KUMA-AGENT-SERVICE-HEALTH — Implementation plan

Governing spec: [spec.md](spec.md). Rows: [requirements.md](requirements.md).

## Summary

This plan states how `uptime-kuma-agent` delivers the rows of `CONN-UPTIME-KUMA-AGENT-SERVICE-HEALTH`. The live caller is the `uptime-mcp` console script. The owner is the `uptime_kuma_agent` package. The rows reuse the `scion-sdk` helpers and add no second authority. The plan changes no runtime code.

## Technical Context

- **Language/Version**: Python >=3.12, <3.15
- **Primary Dependencies**: scion-sdk[mcp]>=0.6.4,<0.7.0; fastmcp; further pins in `pyproject.toml` (scion-sdk[mcp]>=0.6.4,<0.7.0, uptime-kuma-api>=1.2.1, requests>=2.34.2)
- **Storage**: N/A, the connector keeps no store of its own
- **Testing**: pytest; each row names the proving test as `path::name`
- **Target Platform**: Linux container and stdio or streamable HTTP MCP clients
- **Project Type**: connector
- **Performance Goals**: N/A, the vendor service sets the latency
- **Constraints**: vendor calls go through the SDK governed client; no connector-local transport
- **Scale/Scope**: 2 active row(s) in this spec

## Constitution Check

- Organization constitution 1.5.0, spec-first change: pass. Every behaviour is a row of this spec with a bound or planned test.
- Repository article R-I, connector scope: pass. The rows stay inside this connector's one external system and reuse the SDK for shared capabilities.

## Project Structure

- `uptime_kuma_agent/service_health.py` (existing)
- `tests/test_service_health.py` (existing)
- `uptime_kuma_agent/ontology/access_contracts.ttl` (existing)

## Phase 0: Research

No unknowns. Every row names its code and test; the caller chain of each row was read from the code.

## Phase 1: Design

Read monitors and heartbeat lists from the existing Uptime Kuma client. Select
the latest valid heartbeat by its timestamp and return only the four declared
fields. Bound the number of monitors and inspected heartbeats. The SDK access
contract names the served operation. A synthetic provider exercises the real
MCP call. The connector does not claim an approved engine virtual mapping.

## Phase 2: Task approach

`tasks.md` holds one task per row, producer first. Rows that depend on none run in parallel. A task is checked when its `Spec:` trailer is on the default branch.

## Complexity Tracking

None. The constitution check passed.

## Build contract

- `pre-commit run --all-files` runs ruff check, ruff format, the shared `connector-standard`, `spec`, `secrets` and `dependency-readiness` gates at the pinned shared revision.
- `uv run pytest tests` runs the proving tests; the shared complexity, duplication and KISS gates apply their org thresholds and this repository sets no local override.
- A change adds no scanner suppression and no duplicate implementation of an SDK helper.

## Production caller chain

- `CONN-UPTIME-KUMA-AGENT-SERVICE-HEALTH-R001`: an MCP client calls `uptime_kuma_service_health` (uptime_kuma_agent/mcp_server.py:144), which calls `service_health` of `uptime_kuma_agent/service_health.py`.
- `CONN-UPTIME-KUMA-AGENT-SERVICE-HEALTH-R002`: an MCP client calls `uptime_kuma_service_health` (uptime_kuma_agent/mcp_server.py:144).

## Cross-repo seams

None. The rows depend only on the published `scion-sdk` package, which the connector imports.
