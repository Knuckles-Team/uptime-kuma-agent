# Installation

`uptime-kuma-agent` is a standard Python package and a prebuilt container image. Pick
the path that matches how you want to run it.

## Requirements

- **Python 3.11 – 3.14**.
- A reachable **Uptime Kuma** instance — see [Backing Platform](platform.md) to
  deploy one locally.

## From PyPI (recommended)

```bash
pip install uptime-kuma-agent
```

### Optional extras

The base install ships the MCP server runtime. Install the extra for what you need:

| Extra | Install | Pulls in |
|---|---|---|
| (base) | `pip install uptime-kuma-agent` | MCP-server runtime (`agent-utilities[mcp]`) + `uptime-kuma-api` |
| `agent` | `pip install "uptime-kuma-agent[agent]"` | Pydantic-AI agent + Logfire tracing |
| `all` | `pip install "uptime-kuma-agent[all]"` | MCP server, agent, and Logfire tracing |
| `test` | `pip install "uptime-kuma-agent[test]"` | `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-xdist` |

```bash
# Typical: run both the MCP server and the agent
pip install "uptime-kuma-agent[all]"
```

## From source

```bash
git clone https://github.com/Knuckles-Team/uptime-kuma-agent.git
cd uptime-kuma-agent
pip install -e ".[all]"          # editable install with every extra
```

With [`uv`](https://docs.astral.sh/uv/):

```bash
uv pip install -e ".[all]"
uv run uptime-mcp
```

## Prebuilt Docker image

A multi-stage, slim image is published on every release (entrypoint `uptime-mcp`):

```bash
docker pull knucklessg1/uptime-kuma-agent:latest

docker run --rm -i \
  -e UPTIME_KUMA_URL=http://your-kuma:3001 \
  -e UPTIME_KUMA_USERNAME=admin \
  -e UPTIME_KUMA_PASSWORD=your_password_here \
  knucklessg1/uptime-kuma-agent:latest        # stdio transport (default)
```

For an HTTP server with a published port and the agent service, see
[Deployment](deployment.md).

## Verify the install

```bash
uptime-mcp --help
python -c "import uptime_kuma_agent; print(uptime_kuma_agent.__version__)"
```

## Next steps

- **[Deployment](deployment.md)** — run it as a long-lived MCP server and agent behind Caddy + DNS.
- **[Usage](usage.md)** — call the tools, the API, and the agent CLI.
- **[Configuration](deployment.md#configuration-environment)** — every environment variable.
