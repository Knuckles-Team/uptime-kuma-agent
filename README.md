# Uptime Kuma Agent
## CLI or API | MCP | Agent

![PyPI - Version](https://img.shields.io/pypi/v/uptime-kuma-agent)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
![PyPI - Downloads](https://img.shields.io/pypi/dd/uptime-kuma-agent)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/uptime-kuma-agent)
![GitHub forks](https://img.shields.io/github/forks/Knuckles-Team/uptime-kuma-agent)
![GitHub contributors](https://img.shields.io/github/contributors/Knuckles-Team/uptime-kuma-agent)
![PyPI - License](https://img.shields.io/pypi/l/uptime-kuma-agent)
![GitHub](https://img.shields.io/github/license/Knuckles-Team/uptime-kuma-agent)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/uptime-kuma-agent)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Knuckles-Team/uptime-kuma-agent)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/Knuckles-Team/uptime-kuma-agent)
![GitHub issues](https://img.shields.io/github/issues/Knuckles-Team/uptime-kuma-agent)
![GitHub top language](https://img.shields.io/github/languages/top/Knuckles-Team/uptime-kuma-agent)
![GitHub language count](https://img.shields.io/github/languages/count/Knuckles-Team/uptime-kuma-agent)
![GitHub repo size](https://img.shields.io/github/repo-size/Knuckles-Team/uptime-kuma-agent)
![GitHub repo file count (file type)](https://img.shields.io/github/directory-file-count/Knuckles-Team/uptime-kuma-agent)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/uptime-kuma-agent)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/uptime-kuma-agent)

*Version: 1.0.1*

> **Documentation** — Installation, deployment, usage across the API, CLI, and MCP
> interfaces, the integrated A2A agent, and guidance for provisioning the Uptime Kuma
> platform are maintained in the [official documentation](https://knuckles-team.github.io/uptime-kuma-agent/).

---

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Environment Variables](#environment-variables)
- [Usage & Quick Start](#usage--quick-start)
- [MCP Architecture](#mcp)
- [Agentic Graph Architecture](#agent)
- [Security & Access Governance](#security--governance)
- [Installation](#installation)
- [Documentation](#documentation)
- [Contribution Guidelines](#contribute)

---

## Overview

**Uptime Kuma Agent** is a production-grade Agent and Model Context Protocol (MCP) server designed to interface directly with Agent for interacting with Uptime Kuma API.

---

## Key Features

- **Consolidated Action-Routed MCP Tools:** Minimizes token overhead and eliminates tool bloat in LLM contexts by grouping methods into optimized, togglable tool modules.
- **Enterprise-Grade Security:** Comprehensive support for Eunomia policies, OIDC token delegation, and granular execution context tracking.
- **Integrated Graph Agent:** Built-in Pydantic AI agent supporting the Agent Control Protocol (ACP) and standard Web interfaces (AG-UI).
- **Native Telemetry & Tracing:** Out-of-the-box OpenTelemetry exports and native Langfuse tracing.

---

## Environment Variables

<!-- ENV-VARS-TABLE:START -->

#### Package environment variables

| Variable | Example | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` |  |
| `PORT` | `8000` |  |
| `TRANSPORT` | `stdio` | options: stdio, streamable-http, sse |
| `ENABLE_OTEL` | `True` |  |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:8080/api/public/otel` |  |
| `OTEL_EXPORTER_OTLP_PUBLIC_KEY` | `pk-...` |  |
| `OTEL_EXPORTER_OTLP_SECRET_KEY` | `sk-...` |  |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` |  |
| `EUNOMIA_TYPE` | `none` | options: none, embedded, remote |
| `EUNOMIA_POLICY_FILE` | `mcp_policies.json` |  |
| `EUNOMIA_REMOTE_URL` | `http://eunomia-server:8000` |  |
| `UPTIME_KUMA_URL` | `http://localhost:3001` |  |
| `UPTIME_KUMA_TOKEN` | `your_token_here (used if AUTH_TYPE is token)` |  |
| `UPTIME_KUMA_USERNAME` | `admin (used if AUTH_TYPE is password)` |  |
| `UPTIME_KUMA_PASSWORD` | `your_password_here` |  |
| `AUTH_TYPE` | `password` | options: password, token |
| `CADDYFILE_PATH` | `/home/apps/caddy/Caddyfile` | Caddyfile parsed by the kuma-sync skill |
| `KUMA_DB_PATH` | `/home/apps/uptime-kuma/data/kuma.db` | Uptime-Kuma SQLite DB used by the kuma-sync skill |
| `MONITORSTOOL` | `True` |  |
| `STATUSTOOL` | `True` |  |

#### Inherited agent-utilities variables (apply to every connector)

| Variable | Example | Description |
|----------|---------|-------------|
| `MCP_TOOL_MODE` | `condensed` | Tool surface: `condensed` | `verbose` | `both` |
| `MCP_ENABLED_TOOLS` | — | Comma-separated tool allow-list |
| `MCP_DISABLED_TOOLS` | — | Comma-separated tool deny-list |
| `MCP_ENABLED_TAGS` | — | Comma-separated tag allow-list |
| `MCP_DISABLED_TAGS` | — | Comma-separated tag deny-list |
| `MCP_CLIENT_AUTH` | — | Outbound MCP auth (`oidc-client-credentials` for fleet calls) |
| `OIDC_CLIENT_ID` | — | OIDC client id (service-account auth) |
| `OIDC_CLIENT_SECRET` | — | OIDC client secret (service-account auth) |
| `DEBUG` | `False` | Verbose logging |
| `PYTHONUNBUFFERED` | `1` | Unbuffered stdout (recommended in containers) |
| `MCP_URL` | `http://localhost:8000/mcp` | URL of the MCP server the agent connects to |
| `PROVIDER` | `openai` | LLM provider for the agent |
| `MODEL_ID` | `gpt-4o` | Model id for the agent |
| `ENABLE_WEB_UI` | `True` | Serve the AG-UI web interface |

_20 package + 14 inherited variable(s). Auto-generated from `.env.example` + the shared agent-utilities set — do not edit._
<!-- ENV-VARS-TABLE:END -->


The agent's behavior and connections can be fully configured via environment variables.

| Environment Variable | Source Type | Default Value | Description |
|----------------------|-------------|---------------|-------------|
| `HOST` | System / Docker | `0.0.0.0` | IP interface address for the MCP and Agent servers to bind to. |
| `PORT` | System / Docker | `8000` | Port number for HTTP/SSE transports. |
| `TRANSPORT` | System / Docker | `stdio` | MCP transport channel. Supported values: `stdio`, `streamable-http`, `sse`. |
| `MCP_TOOL_MODE` | MCP / Tools | `condensed` | Tool surface: `condensed`, `verbose`, or `both`. |
| `MCP_ENABLED_TOOLS` / `MCP_DISABLED_TOOLS` | MCP / Tools | None | Comma-separated tool allow/deny list. |
| `MCP_ENABLED_TAGS` / `MCP_DISABLED_TAGS` | MCP / Tools | None | Comma-separated tag allow/deny list. |
| `PYTHONUNBUFFERED` | System / Docker | `1` | Unbuffered stdout (recommended in containers). |
| `DEBUG` | System / Docker | `False` | Verbose logging. |
| `UPTIME_KUMA_URL` | App Credential | `http://localhost:3001` | The base URL of your target Uptime Kuma instance. |
| `AUTH_TYPE` | App Credential | None | Type of authentication used. Supported values: `password`, `token`. |
| `UPTIME_KUMA_TOKEN` | App Credential | None | Authentication token (if `AUTH_TYPE` is `token`). |
| `UPTIME_KUMA_USERNAME`| App Credential | None | Login username (if `AUTH_TYPE` is `password`). |
| `UPTIME_KUMA_PASSWORD`| App Credential | None | Login password (if `AUTH_TYPE` is `password`). |
| `MONITORSTOOL` | Toggle switch | `True` | Set to `False` to completely disable the `uptime_kuma_monitors` MCP tool. |
| `STATUSTOOL` | Toggle switch | `True` | Set to `False` to completely disable the `uptime_kuma_status` MCP tool. |
| `CADDYFILE_PATH` | Kuma Sync Skill | `/home/apps/caddy/Caddyfile` | Caddyfile parsed by the `uptime-kuma-sync` skill. |
| `KUMA_DB_PATH` | Kuma Sync Skill | `/home/apps/uptime-kuma/data/kuma.db` | Uptime-Kuma SQLite DB used by the `uptime-kuma-sync` skill. |
| `ENABLE_OTEL` | Tracing Switch| `True` | Enable telemetry exports via OpenTelemetry standards. |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Tracing | `http://langfuse.arpa/api/public/otel` | Core endpoint URL for exporting tracing and span data. |
| `OTEL_EXPORTER_OTLP_PUBLIC_KEY` / `OTEL_EXPORTER_OTLP_SECRET_KEY` | Tracing | None | OTLP exporter auth keys. |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | Tracing | None | OTLP protocol (e.g. `http/protobuf`). |
| `EUNOMIA_TYPE` | Governance | `none` | Policy enforcement style. Options: `none`, `embedded`, `remote`. |
| `EUNOMIA_POLICY_FILE` | Governance | `mcp_policies.json` | Path to your local Eunomia JSON policy parameters. |
| `EUNOMIA_REMOTE_URL` | Governance | None | Remote Eunomia server URL (when `EUNOMIA_TYPE=remote`). |
| `MCP_URL` | Agent (`[agent]`) | `http://localhost:8000/mcp` | URL of the MCP server the agent connects to. |
| `PROVIDER` | Agent (`[agent]`) | `openai` | LLM provider for the integrated agent. |
| `MODEL_ID` | Agent (`[agent]`) | `gpt-4o` | Model id for the integrated agent. |
| `ENABLE_WEB_UI` | Agent (`[agent]`) | `True` | Serve the AG-UI web interface. |

---

## Usage & Quick Start

To bootstrap and run the agent:

1. **Configure Environment:** Create a `.env` file from the provided template:
   ```bash
   cp .env.example .env
   # Add your target Uptime Kuma credentials
   ```

2. **Run MCP Server locally via CLI:**
   ```bash
   uv run uptime-mcp
   ```

3. **Interact with the Pydantic AI Graph Agent CLI:**
   ```bash
   uv run uptime-agent --provider openai --model-id gpt-4o
   ```

---

## MCP

This server utilizes dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

### Available MCP Tools

_Auto-generated from the live MCP server — do not edit by hand._

<!-- MCP-TOOLS-TABLE:START -->

#### Condensed action-routed tools (default — `MCP_TOOL_MODE=condensed`)

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `uptime_kuma_monitors` | `MONITORSTOOL` | Manage uptime kuma monitors operations. |
| `uptime_kuma_status` | `STATUSTOOL` | Manage uptime kuma status operations. |

#### Verbose 1:1 API-mapped tools (`MCP_TOOL_MODE=verbose` or `both`)

<details>
<summary>88 per-operation tools — one per public API method (click to expand)</summary>

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `uptime_kuma_add_api_key` | `UPTIME_KUMA_APITOOL` | Adds a new api key. |
| `uptime_kuma_add_docker_host` | `UPTIME_KUMA_APITOOL` | Add a docker host. |
| `uptime_kuma_add_maintenance` | `UPTIME_KUMA_APITOOL` | Adds a maintenance. |
| `uptime_kuma_add_monitor` | `UPTIME_KUMA_APITOOL` | Adds a new monitor. |
| `uptime_kuma_add_monitor_maintenance` | `UPTIME_KUMA_APITOOL` | Adds monitors to a maintenance. |
| `uptime_kuma_add_monitor_tag` | `UPTIME_KUMA_APITOOL` | Add a tag to a monitor. |
| `uptime_kuma_add_notification` | `UPTIME_KUMA_APITOOL` | Add a notification. |
| `uptime_kuma_add_proxy` | `UPTIME_KUMA_APITOOL` | Add a proxy. |
| `uptime_kuma_add_status_page` | `UPTIME_KUMA_APITOOL` | Add a status page. |
| `uptime_kuma_add_status_page_maintenance` | `UPTIME_KUMA_APITOOL` | Adds status pages to a maintenance. |
| `uptime_kuma_add_tag` | `UPTIME_KUMA_APITOOL` | Add a tag. |
| `uptime_kuma_avg_ping` | `UPTIME_KUMA_APITOOL` | Get average ping. |
| `uptime_kuma_cert_info` | `UPTIME_KUMA_APITOOL` | Get certificate info. |
| `uptime_kuma_change_password` | `UPTIME_KUMA_APITOOL` | Change password. |
| `uptime_kuma_check_apprise` | `UPTIME_KUMA_APITOOL` | Check if apprise exists. |
| `uptime_kuma_clear_events` | `UPTIME_KUMA_APITOOL` | Clear monitor events. |
| `uptime_kuma_clear_heartbeats` | `UPTIME_KUMA_APITOOL` | Clear monitor heartbeats. |
| `uptime_kuma_clear_statistics` | `UPTIME_KUMA_APITOOL` | Clear statistics. |
| `uptime_kuma_connect` | `UPTIME_KUMA_APITOOL` | Connects to Uptime Kuma. |
| `uptime_kuma_delete_api_key` | `UPTIME_KUMA_APITOOL` | Enable an api key. |
| `uptime_kuma_delete_docker_host` | `UPTIME_KUMA_APITOOL` | Delete a docker host. |
| `uptime_kuma_delete_maintenance` | `UPTIME_KUMA_APITOOL` | Deletes a maintenance. |
| `uptime_kuma_delete_monitor` | `UPTIME_KUMA_APITOOL` | Deletes a monitor. |
| `uptime_kuma_delete_monitor_tag` | `UPTIME_KUMA_APITOOL` | Delete a tag from a monitor. |
| `uptime_kuma_delete_notification` | `UPTIME_KUMA_APITOOL` | Delete a notification. |
| `uptime_kuma_delete_proxy` | `UPTIME_KUMA_APITOOL` | Delete a proxy. |
| `uptime_kuma_delete_status_page` | `UPTIME_KUMA_APITOOL` | Delete a status page. |
| `uptime_kuma_delete_tag` | `UPTIME_KUMA_APITOOL` | Delete a tag. |
| `uptime_kuma_disable_2fa` | `UPTIME_KUMA_APITOOL` | Disable 2FA for this user. |
| `uptime_kuma_disable_api_key` | `UPTIME_KUMA_APITOOL` | Disable an api key. |
| `uptime_kuma_disconnect` | `UPTIME_KUMA_APITOOL` | Disconnects from Uptime Kuma. |
| `uptime_kuma_edit_docker_host` | `UPTIME_KUMA_APITOOL` | Edit a docker host. |
| `uptime_kuma_edit_maintenance` | `UPTIME_KUMA_APITOOL` | Edits a maintenance. |
| `uptime_kuma_edit_monitor` | `UPTIME_KUMA_APITOOL` | Edits an existing monitor. |
| `uptime_kuma_edit_notification` | `UPTIME_KUMA_APITOOL` | Edit a notification. |
| `uptime_kuma_edit_proxy` | `UPTIME_KUMA_APITOOL` | Edit a proxy. |
| `uptime_kuma_edit_tag` | `UPTIME_KUMA_APITOOL` | Edits an existing tag. |
| `uptime_kuma_enable_api_key` | `UPTIME_KUMA_APITOOL` | Enable an api key. |
| `uptime_kuma_get_api_key` | `UPTIME_KUMA_APITOOL` | Get an api key. |
| `uptime_kuma_get_api_keys` | `UPTIME_KUMA_APITOOL` | Get all api keys. |
| `uptime_kuma_get_database_size` | `UPTIME_KUMA_APITOOL` | Get database size. |
| `uptime_kuma_get_docker_host` | `UPTIME_KUMA_APITOOL` | Get a docker host. |
| `uptime_kuma_get_docker_hosts` | `UPTIME_KUMA_APITOOL` | Get all docker hosts. |
| `uptime_kuma_get_game_list` | `UPTIME_KUMA_APITOOL` | Get a list of games that are supported by the GameDig monitor type. |
| `uptime_kuma_get_heartbeats` | `UPTIME_KUMA_APITOOL` | Get heartbeats. |
| `uptime_kuma_get_important_heartbeats` | `UPTIME_KUMA_APITOOL` | Get important heartbeats. |
| `uptime_kuma_get_maintenance` | `UPTIME_KUMA_APITOOL` | Get a maintenance. |
| `uptime_kuma_get_maintenances` | `UPTIME_KUMA_APITOOL` | Get all maintenances. |
| `uptime_kuma_get_monitor` | `UPTIME_KUMA_APITOOL` | Get a monitor. |
| `uptime_kuma_get_monitor_beats` | `UPTIME_KUMA_APITOOL` | Get monitor beats for a specific monitor in a time range. |
| `uptime_kuma_get_monitor_maintenance` | `UPTIME_KUMA_APITOOL` | Gets all monitors of a maintenance. |
| `uptime_kuma_get_monitor_status` | `UPTIME_KUMA_APITOOL` | Get the monitor status. |
| `uptime_kuma_get_monitors` | `UPTIME_KUMA_APITOOL` | Get all monitors. |
| `uptime_kuma_get_notification` | `UPTIME_KUMA_APITOOL` | Get a notification. |
| `uptime_kuma_get_notifications` | `UPTIME_KUMA_APITOOL` | Get all notifications. |
| `uptime_kuma_get_proxies` | `UPTIME_KUMA_APITOOL` | Get all proxies. |
| `uptime_kuma_get_proxy` | `UPTIME_KUMA_APITOOL` | Get a proxy. |
| `uptime_kuma_get_settings` | `UPTIME_KUMA_APITOOL` | Get settings. |
| `uptime_kuma_get_status_page` | `UPTIME_KUMA_APITOOL` | Get a status page. |
| `uptime_kuma_get_status_page_maintenance` | `UPTIME_KUMA_APITOOL` | Gets all status pages of a maintenance. |
| `uptime_kuma_get_status_pages` | `UPTIME_KUMA_APITOOL` | Get all status pages. |
| `uptime_kuma_get_tag` | `UPTIME_KUMA_APITOOL` | Get a tag. |
| `uptime_kuma_get_tags` | `UPTIME_KUMA_APITOOL` | Get all tags. |
| `uptime_kuma_info` | `UPTIME_KUMA_APITOOL` | Get server info. |
| `uptime_kuma_login` | `UPTIME_KUMA_APITOOL` | Login. |
| `uptime_kuma_login_by_token` | `UPTIME_KUMA_APITOOL` | Login by token. |
| `uptime_kuma_logout` | `UPTIME_KUMA_APITOOL` | Logout. |
| `uptime_kuma_need_setup` | `UPTIME_KUMA_APITOOL` | Check if the server has already been set up. |
| `uptime_kuma_pause_maintenance` | `UPTIME_KUMA_APITOOL` | Pauses a maintenance. |
| `uptime_kuma_pause_monitor` | `UPTIME_KUMA_APITOOL` | Pauses a monitor. |
| `uptime_kuma_post_incident` | `UPTIME_KUMA_APITOOL` | Post an incident to status page. |
| `uptime_kuma_prepare_2fa` | `UPTIME_KUMA_APITOOL` | Prepare 2FA configuration. |
| `uptime_kuma_resume_maintenance` | `UPTIME_KUMA_APITOOL` | Resumes a maintenance. |
| `uptime_kuma_resume_monitor` | `UPTIME_KUMA_APITOOL` | Resumes a monitor. |
| `uptime_kuma_save_2fa` | `UPTIME_KUMA_APITOOL` | Save the current 2FA configuration. |
| `uptime_kuma_save_status_page` | `UPTIME_KUMA_APITOOL` | Save a status page. |
| `uptime_kuma_set_settings` | `UPTIME_KUMA_APITOOL` | Set settings. |
| `uptime_kuma_setup` | `UPTIME_KUMA_APITOOL` | Set up the server. |
| `uptime_kuma_shrink_database` | `UPTIME_KUMA_APITOOL` | Shrink database. |
| `uptime_kuma_test_chrome` | `UPTIME_KUMA_APITOOL` | Test if the chrome executable is valid and return the version. |
| `uptime_kuma_test_docker_host` | `UPTIME_KUMA_APITOOL` | Test a docker host. |
| `uptime_kuma_test_notification` | `UPTIME_KUMA_APITOOL` | Test a notification. |
| `uptime_kuma_twofa_status` | `UPTIME_KUMA_APITOOL` | Get current 2FA status. |
| `uptime_kuma_unpin_incident` | `UPTIME_KUMA_APITOOL` | Unpin an incident from a status page. |
| `uptime_kuma_upload_backup` | `UPTIME_KUMA_APITOOL` | Import Backup. |
| `uptime_kuma_uptime` | `UPTIME_KUMA_APITOOL` | Get monitor uptime. |
| `uptime_kuma_verify_token` | `UPTIME_KUMA_APITOOL` | Verify the provided 2FA token. |
| `uptime_kuma_wait_for_event` | `UPTIME_KUMA_APITOOL` | Invoke the wait_for_event operation. |

</details>

_2 action-routed tool(s) (default) · 88 verbose 1:1 tool(s). Each is enabled unless its `<DOMAIN>TOOL` toggle is set false; `MCP_TOOL_MODE` selects the surface (`condensed` default · `verbose` 1:1 · `both`). Auto-generated — do not edit._
<!-- MCP-TOOLS-TABLE:END -->

Detailed tool schemas, parameter shapes, and validation constraints are preserved in [docs/index.md](docs/index.md#mcp).

### Detailed Tool Actions Mapping
The action-routed tools wrap complex calls behind a simple, unified parameters scheme:

#### 1. `uptime_kuma_monitors`
Manage uptime kuma monitors operations. Action parameter must be one of:
- `get_monitors`: List all monitors.
- `get_monitor`: Fetch a single monitor details by ID (in `params_json`).
- `add_monitor`: Create a new monitor.
- `edit_monitor`: Modify an existing monitor.
- `delete_monitor`: Delete a monitor by ID.
- `pause_monitor`: Pause monitoring for a specific ID.
- `resume_monitor`: Resume monitoring for a specific ID.

#### 2. `uptime_kuma_status`
Retrieve status and analytics. Action parameter must be one of:
- `get_heartbeats`: Fetch monitor heartbeat records.
- `info`: Retrieve system stats and general status info.

### Dynamic Tool Selection & Visibility

This MCP server supports dynamic toolset selection and visibility filtering at runtime. This allows you to restrict the set of exposed tools in order to prevent blowing up the LLM's context window.

You can configure tool filtering via multiple input channels:

- **CLI Arguments:** Pass `--tools` or `--toolsets` (or their disabled counterparts `--disabled-tools` and `--disabled-toolsets`) during startup.
- **Environment Variables:** Define standard environment variables:
  - `MCP_ENABLED_TOOLS` / `MCP_DISABLED_TOOLS`
  - `MCP_ENABLED_TAGS` / `MCP_DISABLED_TAGS`
- **HTTP SSE Request Headers:** Pass custom headers during transport initialization:
  - `x-mcp-enabled-tools` / `x-mcp-disabled-tools`
  - `x-mcp-enabled-tags` / `x-mcp-disabled-tags`
- **HTTP SSE Request Query Parameters:** Append query parameters directly to your transport connection URL:
  - `?tools=tool1,tool2`
  - `?tags=tag1`

When query strings or parameters are supplied, an LLM-free **Knowledge Graph resolution layer** (using `DynamicToolOrchestrator`) matches query intents against known tool tags, names, or descriptions, with safe fallback and automated 24-hour background cache refreshing.

---

### MCP Configuration Examples

<!-- MCP-CONFIG-EXAMPLES:START -->

> **Install the slim `[mcp]` extra.** All examples install `uptime-kuma-agent[mcp]` — the
> MCP-server extra that pulls only the FastMCP / FastAPI tooling (`agent-utilities[mcp]`).
> It deliberately **excludes** the heavy agent runtime (`pydantic-ai`, the epistemic-graph
> engine, `dspy`, `llama-index`), so `uvx` / container installs are far smaller. Use the
> full `[agent]` extra only when you need the integrated Pydantic AI agent.

#### stdio Transport (local IDEs — Cursor, Claude Desktop, VS Code)

```json
{
  "mcpServers": {
    "uptime-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "uptime-kuma-agent[mcp]",
        "uptime-mcp"
      ],
      "env": {
        "MCP_TOOL_MODE": "condensed",
        "CADDYFILE_PATH": "/home/apps/caddy/Caddyfile",
        "KUMA_DB_PATH": "/home/apps/uptime-kuma/data/kuma.db",
        "MONITORSTOOL": "True",
        "STATUSTOOL": "True",
        "UPTIME_KUMA_PASSWORD": "your_password_here",
        "UPTIME_KUMA_TOKEN": "your_token_here (used if AUTH_TYPE is token)",
        "UPTIME_KUMA_URL": "http://localhost:3001",
        "UPTIME_KUMA_USERNAME": "admin (used if AUTH_TYPE is password)"
      }
    }
  }
}
```

#### Streamable-HTTP Transport (networked / production)

```json
{
  "mcpServers": {
    "uptime-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "uptime-kuma-agent[mcp]",
        "uptime-mcp",
        "--transport",
        "streamable-http",
        "--port",
        "8000"
      ],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "MCP_TOOL_MODE": "condensed",
        "CADDYFILE_PATH": "/home/apps/caddy/Caddyfile",
        "KUMA_DB_PATH": "/home/apps/uptime-kuma/data/kuma.db",
        "MONITORSTOOL": "True",
        "STATUSTOOL": "True",
        "UPTIME_KUMA_PASSWORD": "your_password_here",
        "UPTIME_KUMA_TOKEN": "your_token_here (used if AUTH_TYPE is token)",
        "UPTIME_KUMA_URL": "http://localhost:3001",
        "UPTIME_KUMA_USERNAME": "admin (used if AUTH_TYPE is password)"
      }
    }
  }
}
```

Alternatively, connect to a pre-deployed Streamable-HTTP instance by `url`:

```json
{
  "mcpServers": {
    "uptime-mcp": {
      "url": "http://localhost:8000/uptime-mcp/mcp"
    }
  }
}
```

Deploying the Streamable-HTTP server via Docker:

```bash
docker run -d \
  --name uptime-mcp-mcp \
  -p 8000:8000 \
  -e TRANSPORT=streamable-http \
  -e HOST=0.0.0.0 \
  -e PORT=8000 \
  -e MCP_TOOL_MODE=condensed \
  -e CADDYFILE_PATH=/home/apps/caddy/Caddyfile \
  -e KUMA_DB_PATH=/home/apps/uptime-kuma/data/kuma.db \
  -e MONITORSTOOL=True \
  -e STATUSTOOL=True \
  -e UPTIME_KUMA_PASSWORD=your_password_here \
  -e UPTIME_KUMA_TOKEN="your_token_here (used if AUTH_TYPE is token)" \
  -e UPTIME_KUMA_URL=http://localhost:3001 \
  -e UPTIME_KUMA_USERNAME="admin (used if AUTH_TYPE is password)" \
  knucklessg1/uptime-kuma-agent:mcp
```

_Auto-generated from the code-read env surface (`MCP_TOOL_MODE` + package vars) — do not edit._
<!-- MCP-CONFIG-EXAMPLES:END -->

<!-- BEGIN GENERATED: additional-deployment-options -->
### Additional Deployment Options

`uptime-kuma-agent` can also run as a **local container** (Docker / Podman / `uv`) or be
consumed from a **remote deployment**. The
[Deployment guide](https://knuckles-team.github.io/uptime-kuma-agent/deployment/) has full, copy-paste
`mcp_config.json` for all four transports — **stdio**, **streamable-http**,
**local container / uv**, and **remote URL**:

- **Local container / uv** — launch the server from `mcp_config.json` via `uvx`,
  `docker run`, or `podman run`, or point at a local streamable-http container by `url`.
- **Remote URL** — connect to a server deployed behind Caddy at
  `http://uptime-mcp.arpa/mcp` using the `"url"` key.
<!-- END GENERATED: additional-deployment-options -->

## Agent

This repository features a fully integrated Pydantic AI Graph Agent. It communicates over the **Agent Control Protocol (ACP)** and interacts seamlessly with the **Agent Web UI (AG-UI)** and Terminal interface.

### Running the Agent CLI
To start the interactive command-line agent:

```bash
# Set credentials
export UPTIME_KUMA_URL="http://localhost:3001"
export AUTH_TYPE="password"
export UPTIME_KUMA_USERNAME="admin"
export UPTIME_KUMA_PASSWORD="your-password"

# Run the agent server
uptime-agent --provider openai --model-id gpt-4o
```

### Docker Compose Orchestration
The following `docker/agent.compose.yml` configures the Agent, Web UI, and Terminal Interface together:

```yaml
version: '3.8'

services:
  uptime-kuma-agent-mcp:
    image: knucklessg1/uptime-kuma-agent:mcp
    container_name: uptime-kuma-agent-mcp
    hostname: uptime-kuma-agent-mcp
    restart: always
    env_file:
      - ../.env
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=streamable-http
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  uptime-kuma-agent-agent:
    image: knucklessg1/uptime-kuma-agent:latest
    container_name: uptime-kuma-agent-agent
    hostname: uptime-kuma-agent-agent
    restart: always
    depends_on:
      - uptime-kuma-agent-mcp
    env_file:
      - ../.env
    command: [ "uptime-agent" ]
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=9004
      - MCP_URL=http://uptime-kuma-agent-mcp:8000/mcp
      - PROVIDER=${PROVIDER:-openai}
      - MODEL_ID=${MODEL_ID:-gpt-4o}
      - ENABLE_WEB_UI=True
      - ENABLE_OTEL=True
    ports:
      - "9004:9004"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:9004/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

```

Detailed graph node architecture explanations, custom skill configurations, and agentic trace guides are available in [docs/index.md#agent](docs/index.md#agent).

---

## Security & Governance

Built directly upon the enterprise-ready [`agent-utilities`](https://github.com/Knuckles-Team/agent-utilities) core, standard security parameters are fully supported:

### Access Control & Policy Enforcement
- **Eunomia Policies:** Fine-grained, policy-driven tool authorization. Supports `none`, local `embedded` (`mcp_policies.json`), or centralized `remote` modes.
- **OIDC Token Delegation:** Compliant with RFC 8693 token exchange for flowing authenticating user credentials from Web UI / ACP → Agent → MCP.
- **Scoped Credentials:** Execution context runs restricted to the specific caller identity.

### Runtime Security Grid
| Feature | Functionality | Enablement |
|---------|---------------|------------|
| **Tool Guard** | Sensitivity inspection with human-in-the-loop validation | Enabled by default |
| **Prompt Injection Defense** | Input scanning, repetition monitoring, and recursive loop blocks | Enabled by default |
| **Context Safety Guard** | Stuck-loop detectors and contextual overflow preemptive alerts | Enabled by default |

---

## Installation

Pick the extra that matches what you want to run:

| Extra | Installs | Use when |
|-------|----------|----------|
| `uptime-kuma-agent[mcp]` | Slim MCP server only (`agent-utilities[mcp]` — FastMCP/FastAPI) | You only run the **MCP server** (smallest install / image) |
| `uptime-kuma-agent[agent]` | Full agent runtime (`agent-utilities[agent,logfire]` — Pydantic AI + the epistemic-graph engine) | You run the **integrated agent** |
| `uptime-kuma-agent[all]` | Everything (`mcp` + `agent` + `logfire`) | Development / both surfaces |

```bash
# MCP server only (recommended for tool hosting — slim deps)
uv pip install "uptime-kuma-agent[mcp]"

# Full agent runtime (Pydantic AI + epistemic-graph engine)
uv pip install "uptime-kuma-agent[agent]"

# Everything (development)
uv pip install "uptime-kuma-agent[all]"      # or: python -m pip install "uptime-kuma-agent[all]"
```

### Container images (`:mcp` vs `:agent`)

One multi-stage `docker/Dockerfile` builds two right-sized images, selected by `--target`:

| Image tag | Build target | Contents | Entrypoint |
|-----------|--------------|----------|------------|
| `knucklessg1/uptime-kuma-agent:mcp` | `--target mcp` | `uptime-kuma-agent[mcp]` — **slim**, no engine/`pydantic-ai`/`dspy`/`llama-index`/`tree-sitter` | `uptime-mcp` |
| `knucklessg1/uptime-kuma-agent:latest` | `--target agent` (default) | `uptime-kuma-agent[agent]` — **full** agent runtime + epistemic-graph engine | `uptime-agent` |

```bash
docker build --target mcp   -t knucklessg1/uptime-kuma-agent:mcp    docker/   # slim MCP server
docker build --target agent -t knucklessg1/uptime-kuma-agent:latest docker/   # full agent
```

`docker/mcp.compose.yml` runs the slim `:mcp` server; `docker/agent.compose.yml` runs the
agent (`:latest`) with a co-located `:mcp` sidecar.

### Knowledge-graph database (`epistemic-graph`)

The **full agent** (`[agent]` / `:latest`) embeds the **epistemic-graph** engine (pulled in
transitively via `agent-utilities[agent]`). For production — or to share one knowledge graph
across multiple agents — run **epistemic-graph as its own database container** and point the
agent at it instead of embedding it. Deployment recipes (single-node + Raft HA), connection
config, and the full database architecture (with diagrams) are documented in the
[epistemic-graph deployment guide](https://knuckles-team.github.io/epistemic-graph/deployment/).
The slim `[mcp]` server does **not** require the database.

---

## Documentation

The complete documentation is published as the
[official documentation site](https://knuckles-team.github.io/uptime-kuma-agent/) and
is the recommended reference for installation, deployment, and day-to-day operation.

| Page | Contents |
|---|---|
| [Installation](https://knuckles-team.github.io/uptime-kuma-agent/installation/) | pip, source, extras, prebuilt Docker image |
| [Deployment](https://knuckles-team.github.io/uptime-kuma-agent/deployment/) | run the MCP server and agent, Compose, Caddy + Technitium, env config |
| [Usage](https://knuckles-team.github.io/uptime-kuma-agent/usage/) | the MCP tools, the `UptimeKumaApi` client, the agent CLI |
| [Backing Platform](https://knuckles-team.github.io/uptime-kuma-agent/platform/) | deploy Uptime Kuma with Docker |
| [Overview](https://knuckles-team.github.io/uptime-kuma-agent/overview/) | ecosystem role and enterprise readiness |
| [Concepts](https://knuckles-team.github.io/uptime-kuma-agent/concepts/) | concept registry (`CONCEPT:UKA-*`) |

`AGENTS.md` is the canonical contributor/agent guidance.

---

## Repository Owners

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=Knucklessg1&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/Knucklessg1)
![GitHub User's stars](https://img.shields.io/github/stars/Knucklessg1)

---

## Contribute

Contributions are welcome! Please ensure code quality by executing local checks before submitting pull requests:
- Format code using `ruff format .`
- Lint code using `ruff check .`
- Validate type-safety with `mypy .`
- Execute test suites using `pytest`


<!-- BEGIN agent-os-genesis-deploy (generated; do not edit between markers) -->

## Deploy with `agent-os-genesis`

This package can be provisioned for you — skill-guided — by the **`agent-os-genesis`**
universal skill (its *single-package deploy mode*): it picks your install method, seeds
secrets to OpenBao/Vault (or `.env`), trusts your enterprise CA, registers the MCP
server, and verifies it — the same machinery that stands up the whole Agent OS, narrowed
to just this package. Ask your agent to **"deploy `uptime-kuma-agent` with agent-os-genesis"**.

| Install mode | Command |
|------|---------|
| Bare-metal, prod (PyPI) | `uvx uptime-mcp` · or `uv tool install uptime-kuma-agent` |
| Bare-metal, dev (editable) | `uv pip install -e ".[all]"` · or `pip install -e ".[all]"` |
| Container, prod | deploy `knucklessg1/uptime-kuma-agent:latest` via docker-compose / swarm / podman / podman-compose / kubernetes |
| Container, dev (editable) | deploy `docker/compose.dev.yml` (source-mounted at `/src`; edits live on restart) |

Secrets are read-existing + seeded via `vault_sync` — you are only prompted for what's missing.

<!-- END agent-os-genesis-deploy -->
