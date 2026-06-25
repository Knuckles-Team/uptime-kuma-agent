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

*Version: 0.33.0*

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
| `SUPERTOKEN` | `your_supertoken_here` |  |
| `UPTIME_KUMA_URL` | `http://localhost:3001` |  |
| `UPTIME_KUMA_TOKEN` | `your_token_here (used if AUTH_TYPE is token)` |  |
| `UPTIME_KUMA_USERNAME` | `admin (used if AUTH_TYPE is password)` |  |
| `UPTIME_KUMA_PASSWORD` | `your_password_here` |  |
| `AUTH_TYPE` | `password` | options: password, token |
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

_19 package + 14 inherited variable(s). Auto-generated from `.env.example` + the shared agent-utilities set — do not edit._
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
| `SUPERTOKEN` | Auth / Security | None | Optional master bearer token for client request validation. |
| `UPTIME_KUMA_URL` | App Credential | `http://localhost:3001` | The base URL of your target Uptime Kuma instance. |
| `AUTH_TYPE` | App Credential | None | Type of authentication used. Supported values: `password`, `token`. |
| `UPTIME_KUMA_TOKEN` | App Credential | None | Authentication token (if `AUTH_TYPE` is `token`). |
| `UPTIME_KUMA_USERNAME`| App Credential | None | Login username (if `AUTH_TYPE` is `password`). |
| `UPTIME_KUMA_PASSWORD`| App Credential | None | Login password (if `AUTH_TYPE` is `password`). |
| `MONITORSTOOL` | Toggle switch | `True` | Set to `False` to completely disable the `uptime_kuma_monitors` MCP tool. |
| `STATUSTOOL` | Toggle switch | `True` | Set to `False` to completely disable the `uptime_kuma_status` MCP tool. |
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

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `uptime_kuma_monitors` | `MONITORSTOOL` | Manage uptime kuma monitors operations. |
| `uptime_kuma_status` | `STATUSTOOL` | Manage uptime kuma status operations. |

_2 action-routed tools (default `MCP_TOOL_MODE=condensed`). Each is enabled unless its toggle is set false; set `MCP_TOOL_MODE=verbose` (or `both`) for the 1:1 per-operation surface. Auto-generated — do not edit._
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

> **Install the slim `[mcp]` extra.** All examples below install
> `uptime-kuma-agent[mcp]` — the MCP-server extra that pulls only the FastMCP /
> FastAPI tooling (`agent-utilities[mcp]`). It deliberately **excludes** the heavy
> agent runtime (the epistemic-graph engine, `pydantic-ai`, `dspy`, `llama-index`,
> `tree-sitter`), so `uvx`/container installs are dramatically smaller and faster.
> Use the full `[agent]` extra only when you need the integrated Pydantic AI agent
> (see [Installation](#installation)).

#### stdio Transport (Recommended for local IDEs e.g., Cursor, Claude Desktop)
Configure your IDE's `mcp.json` to launch the MCP server via `uvx`:

```json
{
  "mcpServers": {
    "uptime-kuma-agent": {
      "command": "uvx",
      "args": [
        "--from",
        "uptime-kuma-agent[mcp]",
        "uptime-mcp"
      ],
      "env": {
        "UPTIME_KUMA_URL": "http://localhost:3001",
        "AUTH_TYPE": "password",
        "UPTIME_KUMA_USERNAME": "admin",
        "UPTIME_KUMA_PASSWORD": "your_password_here"
      }
    }
  }
}
```

#### Streamable-HTTP Transport (Recommended for production deployments)
Configure your client's `mcp.json` to launch the Streamable-HTTP server via `uvx` with explicit host and port definition:

```json
{
  "mcpServers": {
    "uptime-kuma-agent": {
      "command": "uvx",
      "args": [
        "--from",
        "uptime-kuma-agent[mcp]",
        "uptime-mcp"
      ],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "UPTIME_KUMA_URL": "http://localhost:3001",
        "AUTH_TYPE": "password",
        "UPTIME_KUMA_USERNAME": "admin",
        "UPTIME_KUMA_PASSWORD": "your_password_here"
      }
    }
  }
}
```

Alternatively, connect to a pre-deployed remote or local Streamable-HTTP instance:

```json
{
  "mcpServers": {
    "uptime-kuma-agent": {
      "url": "http://localhost:8000/uptime-kuma-agent/mcp"
    }
  }
}
```

Deploying the Streamable-HTTP server via Docker:

```bash
docker run -d \
  --name uptime-kuma-agent-mcp \
  -p 8000:8000 \
  -e TRANSPORT=streamable-http \
  -e PORT=8000 \
  -e UPTIME_KUMA_URL="http://your-kuma:3001" \
  -e AUTH_TYPE="password" \
  -e UPTIME_KUMA_USERNAME="admin" \
  -e UPTIME_KUMA_PASSWORD="your-password" \
  knucklessg1/uptime-kuma-agent:mcp
```

> The `:mcp` tag is the **slim MCP-server image** (built from
> `docker/Dockerfile --target mcp`, installing `uptime-kuma-agent[mcp]`). The default
> `:latest` tag is the **full agent image** (`--target agent`, `uptime-kuma-agent[agent]`)
> which also bundles the Pydantic AI agent and the epistemic-graph engine — use it
> when you run `uptime-agent` (the agent), not just the MCP server. See
> [Container images](#container-images-mcp-vs-agent).

---

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
