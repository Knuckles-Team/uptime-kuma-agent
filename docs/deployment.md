# Deployment

<!-- BEGIN GENERATED: deployment-options -->
## Deployment Options

`uptime-kuma-agent` exposes its MCP server (console script `uptime-mcp`) four ways. Pick the row that
matches where the server runs relative to your MCP client, then copy the matching
`mcp_config.json` below. Replace the `<your-…>` placeholders with the values from the **Configuration / Environment Variables** section.

| # | Option | Transport | Where it runs | `mcp_config.json` key |
|---|--------|-----------|---------------|------------------------|
| 1 | stdio | `stdio` | client launches a subprocess | `command` |
| 2 | Streamable-HTTP (local) | `streamable-http` | a local network port | `command` or `url` |
| 3 | Local container / uv | `stdio` or `streamable-http` | Docker / Podman / uv on this host | `command` or `url` |
| 4 | Remote URL | `streamable-http` | a remote host behind Caddy | `url` |

### 1. stdio (local subprocess)

The client launches the server over stdio via `uvx` — best for local IDEs
(Cursor, Claude Desktop, VS Code):

```json
{
  "mcpServers": {
    "uptime-mcp": {
      "command": "uvx",
      "args": ["--from", "uptime-kuma-agent", "uptime-mcp"],
      "env": {
        "UPTIME_KUMA_URL": "<your-uptime_kuma_url>"
      }
    }
  }
}
```

### 2. Streamable-HTTP (local process)

Run the server as a long-lived HTTP process:

```bash
uvx --from uptime-kuma-agent uptime-mcp --transport streamable-http --host 0.0.0.0 --port 8000
curl -s http://localhost:8000/health        # {"status":"OK"}
```

Then either let the client launch it:

```json
{
  "mcpServers": {
    "uptime-mcp": {
      "command": "uvx",
      "args": ["--from", "uptime-kuma-agent", "uptime-mcp", "--transport", "streamable-http", "--port", "8000"],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "UPTIME_KUMA_URL": "<your-uptime_kuma_url>"
      }
    }
  }
}
```

…or connect to the already-running process by URL:

```json
{
  "mcpServers": {
    "uptime-mcp": { "url": "http://localhost:8000/mcp" }
  }
}
```

### 3. Local container / uv

**(a) Launch a container directly from `mcp_config.json`** (stdio over the container —
no ports to manage). Swap `docker` for `podman` for a daemonless runtime:

```json
{
  "mcpServers": {
    "uptime-mcp": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "TRANSPORT=stdio",
        "-e", "UPTIME_KUMA_URL=<your-uptime_kuma_url>",
        "knucklessg1/uptime-kuma-agent:latest"
      ]
    }
  }
}
```

**(b) Run a local streamable-http container, then connect by URL:**

```bash
docker run -d --name uptime-mcp -p 8000:8000 \
  -e TRANSPORT=streamable-http \
  -e PORT=8000 \
  -e UPTIME_KUMA_URL="<your-uptime_kuma_url>" \
  knucklessg1/uptime-kuma-agent:latest
# or, from a clone of this repo:
docker compose -f docker/mcp.compose.yml up -d
```

```json
{
  "mcpServers": {
    "uptime-mcp": { "url": "http://localhost:8000/mcp" }
  }
}
```

**(c) From a local checkout with `uv`:**

```bash
uv run uptime-mcp --transport streamable-http --port 8000
```

### 4. Remote URL (deployed behind Caddy)

When the server is deployed remotely (e.g. as a Docker service) and published through
Caddy on the internal `*.arpa` zone, connect with the `"url"` key — no local process or
image required:

```json
{
  "mcpServers": {
    "uptime-mcp": { "url": "http://uptime-mcp.arpa/mcp" }
  }
}
```

Caddy reverse-proxies `http://uptime-mcp.arpa` to the container's `:8000`
streamable-http listener; `http://uptime-mcp.arpa/health` returns
`{"status":"OK"}` when the service is live.
<!-- END GENERATED: deployment-options -->

This page covers running `uptime-kuma-agent` as a long-lived service: the transports,
a Docker Compose stack, the optional A2A agent server, putting it behind a Caddy
reverse proxy, and giving it a DNS name with Technitium. To provision the **Uptime
Kuma** instance it connects to, see [Backing Platform](platform.md).

> `uptime-kuma-agent` ships **two** console scripts: the MCP server (`uptime-mcp`) and
> a Pydantic AI agent server (`uptime-agent`). The MCP server is a typed,
> deterministic tool surface a policy router / agent calls; the agent server adds a
> conversational graph agent and web UI on top of it.

## Run the MCP server

The transport is selected with `--transport` (or the `TRANSPORT` env var):

=== "stdio (default)"

    ```bash
    uptime-mcp
    ```
    For IDE / desktop MCP clients that launch the server as a subprocess.

=== "streamable-http"

    ```bash
    uptime-mcp --transport streamable-http --host 0.0.0.0 --port 8000
    ```
    A network server with a `/health` endpoint and `/mcp` route.

=== "sse"

    ```bash
    uptime-mcp --transport sse --host 0.0.0.0 --port 8000
    ```

Health check (HTTP transports):

```bash
curl -s http://localhost:8000/health        # {"status":"OK"}
```

## Configuration (environment)

`uptime-kuma-agent` is configured entirely from the environment. The **required**
connection set:

| Var | Default | Meaning |
|---|---|---|
| `UPTIME_KUMA_URL` | `http://localhost:3001` | Base URL of the Uptime Kuma instance |
| `AUTH_TYPE` | (unset) | `password` or `token` |
| `UPTIME_KUMA_USERNAME` | (unset) | Login user (when `AUTH_TYPE=password`) |
| `UPTIME_KUMA_PASSWORD` | (unset) | Login password (when `AUTH_TYPE=password`) |
| `UPTIME_KUMA_TOKEN` | (unset) | Access token (when `AUTH_TYPE=token`) |
| `HOST` | `0.0.0.0` | Bind address for HTTP transports |
| `PORT` | `8000` | Bind port for HTTP transports |
| `TRANSPORT` | `stdio` | `stdio`, `streamable-http`, or `sse` |
| `MONITORSTOOL` | `True` | Register the `uptime_kuma_monitors` tool |
| `STATUSTOOL` | `True` | Register the `uptime_kuma_status` tool |
| `ENABLE_OTEL` | `True` | Export traces via OpenTelemetry |
| `EUNOMIA_TYPE` | `none` | Policy enforcement: `none`, `embedded`, `remote` |

The complete set, including the OpenTelemetry and Eunomia options, is documented in
[`.env.example`](https://github.com/Knuckles-Team/uptime-kuma-agent/blob/main/.env.example).
Copy it to `.env` and populate only what you use.

## Docker Compose

The repo ships [`docker/mcp.compose.yml`](https://github.com/Knuckles-Team/uptime-kuma-agent/blob/main/docker/mcp.compose.yml).
It reads a sibling `.env` and publishes the HTTP server on `:8000`:

```yaml
services:
  uptime-kuma-agent-mcp:
    image: knucklessg1/uptime-kuma-agent:latest
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
```

```bash
cp .env.example .env          # then edit UPTIME_KUMA_* values
docker compose -f docker/mcp.compose.yml up -d
docker compose -f docker/mcp.compose.yml logs -f
```

## Agent server

For the conversational A2A experience, the repo ships
[`docker/agent.compose.yml`](https://github.com/Knuckles-Team/uptime-kuma-agent/blob/main/docker/agent.compose.yml),
which deploys the MCP server **and** the `uptime-agent` graph agent together. The
agent serves its web UI on `:9004` and is wired to the MCP server through `MCP_URL`:

```yaml
services:
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
    ports:
      - "9004:9004"
```

```bash
docker compose -f docker/agent.compose.yml up -d
```

Run the agent directly from the command line for interactive use:

```bash
uptime-agent --provider openai --model-id gpt-4o
```

## Behind a Caddy reverse proxy

Expose the HTTP server on a hostname with automatic TLS. Add to your `Caddyfile`:

```caddy
# Internal (self-signed) — homelab .arpa zone
uptime-kuma-agent.arpa {
    tls internal
    reverse_proxy uptime-kuma-agent-mcp:8000
}
```

```caddy
# Public — automatic Let's Encrypt
uptime-kuma-agent.example.com {
    reverse_proxy uptime-kuma-agent-mcp:8000
}
```

Reload Caddy:

```bash
docker compose -f services/caddy/compose.yml exec caddy caddy reload --config /etc/caddy/Caddyfile
```

## DNS with Technitium

Point the hostname at the host running Caddy. Via the Technitium API:

```bash
curl -s "http://technitium.arpa:5380/api/zones/records/add" \
  --data-urlencode "token=$TECHNITIUM_DNS_TOKEN" \
  --data-urlencode "domain=uptime-kuma-agent.arpa" \
  --data-urlencode "zone=arpa" \
  --data-urlencode "type=A" \
  --data-urlencode "ipAddress=10.0.0.10" \
  --data-urlencode "ttl=3600"
```

…or add an **A record** `uptime-kuma-agent.arpa → <caddy-host-ip>` in the Technitium
web console (`http://technitium.arpa:5380`). The ecosystem
[`technitium-dns-mcp`](https://knuckles-team.github.io/technitium-dns-mcp/) automates
this as a tool.

## Register with an MCP client

Add to your client's `mcp_config.json`:

```json
{
  "mcpServers": {
    "uptime-kuma-agent": {
      "command": "uv",
      "args": ["run", "uptime-mcp"],
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

For a remote HTTP server, point the client at `http://uptime-kuma-agent.arpa/mcp`
instead.
