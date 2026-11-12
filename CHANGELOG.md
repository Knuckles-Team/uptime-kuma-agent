# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.3.9] - 2026-11-12

### Changed
- The hand-written `action`-routed tools `uptime_kuma_monitors` and `uptime_kuma_status` are removed. Every Uptime Kuma operation is served as one typed tool per client method (`uptime_kuma_get_monitors`, `uptime_kuma_pause_monitor`, ...); `uptime_kuma_service_health` and `uptime_ingest_monitors` stay.
- Declare tool-use contracts, prompt and skill links, a data location and business roles; ship an operator and three business-role agent prompts in place of the placeholder specialist prompt; root every ontology class in a core class.
- Require `scion-sdk>=0.9.0,<0.10.0`.

## [2.3.8] - 2026-11-06

### Fixed
- The observability specialist prompt names the typed `uptime_kuma_*` tools instead of the retired `uptime_kuma_monitors` and `uptime_kuma_status` tools.
- `UPTIME_KUMA_TIMEOUT` defaults to 120 seconds: a large Uptime Kuma database takes over 25 seconds to log in and longer to return the monitor list.
- Require `scion-sdk>=0.6.5` so destructive tools accept `confirm=true`.

## [2.3.7] - 2026-10-30

### Changed
- Require `scion-sdk>=0.6.4,<0.7.0`; `uv.lock` relocked.

## [2.3.3] - 2026-10-23

### Changed
- Requires `agent-connector-sdk>=0.4.1`; data sources are declared in code (`connector_sources`).

## [Unreleased]

### Added
- Created Concept Registry in `AGENTS.md` for strict design and implementation traceability.
- Decorated all test functions in the suite with `@pytest.mark.concept()` custom marker.
- Documented key required and optional environment variables in a newly established `.env.example`.

### Changed
- Standardized the test suite structure by migrating all tests to `tests/unit/`.
- Introduced `tests/conftest.py` with dynamic modules cache cleaning to guarantee total isolation between test invocations.
- Converted dynamic package initialization check blocks into clean data-driven parameterized tests.
- Polished `README.md` with a complete Table of Contents, detailed Usage & Quick Start guide, and a registered MCP Tools table.

## [0.14.0] - 2026-05-22

### Changed
- Updated package and dependency configurations to align with the `agent-utilities` ecosystem.

## [0.1.7] - 2026-04-29

### Added
- Initial release of the `uptime-kuma-agent`.
