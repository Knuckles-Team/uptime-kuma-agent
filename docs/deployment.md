# Deployment

<!-- BEGIN GENERATED: deployment-options -->
## Deployment Options

`uptime-kuma-agent` supports local stdio, a loopback-only development listener, a
least-privilege stdio container, and a remote authenticated HTTPS boundary.
Provider endpoint, credential, selector, identity, and trust material are supplied
at runtime through `AgentConfig`; none is stored in this repository.

### Installed stdio process

```json
{
  "mcpServers": {
    "uptime": {
      "command": "uptime-mcp",
      "args": [],
      "env": {"MCP_TOOL_MODE": "intent"}
    }
  }
}
```

### Loopback development listener

```bash
uptime-mcp --transport streamable-http --host 127.0.0.1 --port 8000
```

Do not expose this listener beyond loopback. Network deployments require direct TLS
or an explicitly trusted TLS-terminating ingress, configured authentication, exact
`MCP_ALLOWED_HOSTS`, and an exact trusted-proxy CIDR policy.

### Least-privilege local container

```bash
docker run -i --rm \
  --read-only \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --pids-limit=256 \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m \
  -e TRANSPORT=stdio \
  registry.example.invalid/uptime-kuma-agent@sha256:<digest> uptime-mcp
```

The operator projects the selected AgentConfig profile into the process at runtime;
the image remains immutable and contains no environment connection profile.

### Remote authenticated HTTPS endpoint

```json
{
  "mcpServers": {
    "uptime": {"url": "https://service.example.invalid/mcp"}
  }
}
```

Store the real remote URL, outbound identity reference, and TLS-profile reference in
`AgentConfig`, not in MCP client JSON or documentation.
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
    image: example/uptime-kuma-agent@sha256:<digest>
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
    image: example/uptime-kuma-agent@sha256:<digest>
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
# Internal (self-signed) — homelab .example.invalid zone
uptime-kuma-agent.example.invalid {
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
curl -s "http://technitium.example.invalid:5380/api/zones/records/add" \
  --data-urlencode "token=$TECHNITIUM_DNS_TOKEN" \
  --data-urlencode "domain=uptime-kuma-agent.example.invalid" \
  --data-urlencode "zone=arpa" \
  --data-urlencode "type=A" \
  --data-urlencode "ipAddress=192.0.2.10" \
  --data-urlencode "ttl=3600"
```

…or add an **A record** `uptime-kuma-agent.example.invalid → <caddy-host-ip>` in the Technitium
web console (`http://technitium.example.invalid:5380`). The ecosystem
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

For a remote HTTP server, point the client at `http://uptime-kuma-agent.example.invalid/mcp`
instead.
