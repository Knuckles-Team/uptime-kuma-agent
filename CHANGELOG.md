# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Created Concept Registry in `AGENTS.md` for strict design and implementation traceability.
- Decorated all test functions in the suite with `@pytest.mark.concept()` custom marker.
- Documented key required and optional environment variables in a newly established `.env.example`.

### Changed
- Standardized the test suite structure by migrating all tests to `tests/unit/`.
- Introduced `tests/conftest.py` with dynamic modules cache cleaning to guarantee total isolation between test invocations.
- Converted dynamic package initialization check blocks into clean data-driven parameterized tests.
- Polished `README.md` with a comprehensive Table of Contents, detailed Usage & Quick Start guide, and a registered MCP Tools table.

## [0.14.0] - 2026-05-22

### Changed
- Updated package and dependency configurations to align with the `agent-utilities` ecosystem.

## [0.1.7] - 2026-04-29

### Added
- Initial release of the `uptime-kuma-agent`.
