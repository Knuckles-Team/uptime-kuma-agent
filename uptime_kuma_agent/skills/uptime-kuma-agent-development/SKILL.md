---
name: uptime-kuma-agent-development
skill_type: skill
description: >-
  Develop, test, and release the uptime-kuma-agent connector while preserving
  its typed Uptime Kuma client, action-routed MCP surface, packaged content,
  spec evidence, and shared release gates.
license: MIT
tags: [uptime-kuma-agent, connector, development, testing, packaging, pages, specs]
metadata:
  author: Project Maintainers
  version: '0.1.0'
---

# uptime-kuma-agent development

This skill is the repository contract for the uptime-kuma-agent connector. The
package owns the Uptime Kuma client and models, authentication, MCP actions,
connector source mappings, packaged prompts, skills, and ontology. Shared
transport, connector validation, release rendering, and delivery gates belong
to `scion-sdk` and `pipelines`; admission and durable graph state
belong to their owning repositories.

## Repository map

- `uptime_kuma_agent/api_client.py` exposes the typed Uptime Kuma operations.
- `uptime_kuma_agent/auth.py` resolves the configured endpoint and credential
  references before a provider request.
- `uptime_kuma_agent/mcp_server.py` registers the monitor and status action
  surfaces through the SDK's MCP server helpers.
- `uptime_kuma_agent/connector_sources.py`, `kg_ingest.py`, and
  `uptime_kuma_agent/ontology/` own source mappings and the metadata projection.
- `uptime_kuma_agent/skills/`, prompts, ontology, and connector resources are
  packaged content exposed through the connector entry point.
- `tests/` contains the focused action, packaged-content, identity, MCP, and
  ingestion checks; `docs/` is the MkDocs source published by Pages.

## Rapid delivery: the 5-minute contract

Specs are already designed. Deliver one small, reviewable slice at a time.

- Find the owning row with `git grep -n "<term>" -- specs` before changing
  behavior. Extend an existing spec before writing a new requirement.
- Trace a changed action from its typed input through the MCP router, client,
  authentication policy, response model, and source mapping. Reuse those seams
  instead of adding a second connector path.
- Keep changes inside this connector. SDK transports, Arbora admission, MCP
  multiplexing, and graph persistence belong in their owning repositories.
- Keep credentials, provider URLs, monitor data, and live Uptime Kuma calls out
  of tests and logs. Use the existing fakes and task-local configuration seams.
- Generated `specs/*/status.json` files come from `pipelines-hook spec-status`;
  never hand-edit delivery state. Use an explicit `Spec:` trailer or
  `Spec: none (<reason>)` in the final commit paragraph.
- Stage only reviewed paths, and keep packaged skill and resource paths inside
  the existing `uptime_kuma_agent` package-data globs.

## Setup and gates

Use the locked project environment when it is already available:

```bash
uv sync --locked
uvx pre-commit run --all-files
```

For focused feedback, run the smallest existing tests for the changed seam:

```bash
uv run --frozen pytest -q tests/test_action_discovery.py
uv run --frozen pytest -q tests/test_default_content_surfaces.py
uv run --frozen pytest -q tests/test_kg_ingest.py
uv run --frozen pytest -q tests/unit/test_mcp_server.py
```

The canonical pre-commit configuration delegates connector-standard, secrets,
spec (standard, decomposition, generated status, and trailers), tests-fast,
and dependency-readiness checks to `Knuckles-Team/pipelines` at `rev: main`.
Keep those shared hooks; do not copy their implementation here or bypass a
failure.

## Spec delivery and Pages

`.github/workflows/pages.yml` calls
`Knuckles-Team/pipelines/.github/workflows/pages_pipeline.yml@main` with
`content_source: docs`, `spec_dashboard_enabled: true`, and
`.github/spec-dashboard.json`. The version-1 dashboard reads only
`specs/*/status.json`. Keep the push paths for docs, specs, the dashboard
configuration, and this caller so a source change publishes the page.

A local YAML check proves wiring only. Delivery proof requires a successful
hosted Pages run whose source revision equals the candidate merge SHA and the
public `/spec-delivery/` page and snapshot serving that revision.

## Packaging and release

The existing package-data declaration includes `skills/**`, prompts, ontology,
and connector resources. A packaged skill or resource change therefore gets a
normal patch bump in `pyproject.toml` and a matching `uv.lock` update. Verify
that the wheel contains the new development skill before publication. The
central Python workflow publishes the wheel first; the connector container
workflow then uses the canonical renderer. Do not add a synthetic extra or
rewrite a runtime image to satisfy a central check.

## Safety

Never commit `.env` files, credentials, raw provider responses, generated site
output, caches, or temporary command output. Work in a real Git worktree based
on current `origin/main`, preserve the existing tool and authentication
contracts, and do not use `git stash`, `git add -A`, or `git add .`.
