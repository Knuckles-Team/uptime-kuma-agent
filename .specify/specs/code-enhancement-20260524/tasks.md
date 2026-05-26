# Tasks: Code Enhancement: uptime-kuma-agent

Generated: 2026-05-24T04:17:16.245125+00:00
Skipped informational: 5

- [ ] [P] **T001** [Dependency Audit] Minor update: agent-utilities 0.2.40 (installed) -> 0.16.0
  - Priority: P3-Low | Effort: Small
- [ ] [P] **T002** [Dependency Audit] Minor update: requests 2.32.5 (installed) -> 2.34.2
  - Priority: P3-Low | Effort: Small
- [ ] [P] **T003** [Dependency Audit] Minor update: pytest-xdist 3.6.0 (constraint — not installed) -> 3.8.0
  - Priority: P3-Low | Effort: Small
- [ ] [P] **T004** [Security Analysis] 1 MEDIUM severity vulnerabilities found
  - Priority: P2-Medium | Effort: Medium
- [ ] [P] **T005** [Test Coverage] 18 potential doc-test drift items
  - Priority: P3-Low | Effort: Medium
- [ ] [P] **T006** [Architecture & Design Patterns] No discernible layer architecture (no domain/service/adapter separation)
  - Priority: P2-Medium | Effort: Medium
- [ ] [P] **T007** [Concept Traceability] 14 orphaned concepts (only in one source)
  - Priority: P4-Enhancement | Effort: Medium
- [ ] [P] **T008** [Concept Traceability] 5 test functions missing concept markers
  - Priority: P4-Enhancement | Effort: Small
- [ ] [P] **T009** [Linting & Formatting] Total lint findings: 0 (high/error: 0, medium/warning: 0, low: 0)
  - Priority: P4-Enhancement | Effort: Medium
- [ ] [P] **T010** [Pre-Commit Compliance] 2 hook(s) may be outdated: ruff-pre-commit, uv-pre-commit
  - Priority: P2-Medium | Effort: Small
- [ ] [P] **T011** [Version Sync Analysis] Found 1 file(s) with version '0.14.0' that are NOT tracked in .bumpversion.cfg:
  - Priority: P2-Medium | Effort: Small
- [ ] [P] **T012** [Version Sync Analysis]   - .specify/reports/uptime-kuma-agent/results.json
  - Priority: P2-Medium | Effort: Medium
- [ ] [P] **T013** [Changelog Audit] CHANGELOG.md exists but could not be parsed — check format compliance
  - Priority: P3-Low | Effort: Medium
- [ ] [P] **T014** [Changelog Audit] No changelog entries within the last 30 days
  - Priority: P3-Low | Effort: Medium
- [ ] [P] **T015** [Changelog Audit] keepachangelog not installed — pip install 'universal-skills[code-enhancer]'
  - Priority: P3-Low | Effort: Small
- [ ] [P] **T016** [Pytest Quality] 2 tests have no assertions
  - Priority: P4-Enhancement | Effort: Medium
- [ ] [P] **T017** [Pytest Quality] 1 tests exceed 100 lines — likely doing too much per test
  - Priority: P4-Enhancement | Effort: Medium
- [ ] [P] **T018** [Environment Variables] 3 Python env vars not in .env.example: UPTIME_KUMA_PASSWORD, UPTIME_KUMA_TOKEN,
  - Priority: P4-Enhancement | Effort: Medium
- [ ] [P] **T019** [analyze_xdg_kg] Analysis error: No module named 'agent_utilities.knowledge_graph'
  - Priority: P1-High | Effort: Medium
