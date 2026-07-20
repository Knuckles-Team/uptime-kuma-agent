# Backing Platform — Uptime Kuma

`uptime-kuma-agent` is a **client** of an [Uptime Kuma](https://github.com/louislam/uptime-kuma)
monitoring instance. This page provides a Docker recipe for deploying one locally to
serve as the target of `UPTIME_KUMA_URL`. For production topologies, follow the
upstream [Uptime Kuma documentation](https://github.com/louislam/uptime-kuma/wiki).

!!! note "Backing-system recipe"
    Each connector in the ecosystem follows the same convention — a
    `docs/platform.md` recipe for the system it integrates with, accompanied by a
    sample Compose stack that mirrors [`services/`](https://github.com/Knuckles-Team).
    Systems offered only as a managed service have no local recipe.

## Single-node deployment (Compose)

Uptime Kuma publishes the `louislam/uptime-kuma` image. The following stack runs one
instance on `:3001` with a persistent data volume:

```yaml
# docker/uptime-kuma.compose.yml
services:
  uptime-kuma:
    image: louislam/uptime-kuma:1
    container_name: uptime-kuma
    hostname: uptime-kuma
    restart: unless-stopped
    ports:
      - "3001:3001"
    volumes:
      - uptime_data:/app/data
    healthcheck:
      test: ["CMD", "extra/healthcheck"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 40s

volumes:
  uptime_data:
```

```bash
docker compose -f docker/uptime-kuma.compose.yml up -d

# Open the dashboard and complete first-run setup (create the admin user)
# http://localhost:3001
```

On first launch, browse to `http://localhost:3001` and create the administrator
account; those credentials become `UPTIME_KUMA_USERNAME` / `UPTIME_KUMA_PASSWORD`.

## Connect uptime-kuma-agent

```bash
export UPTIME_KUMA_URL=http://localhost:3001
export AUTH_TYPE=password
export UPTIME_KUMA_USERNAME=admin
export UPTIME_KUMA_PASSWORD=your_password_here

uptime-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

## Combined deployment

A combined stack places Uptime Kuma and the MCP server on one Docker network, so the
server reaches Uptime Kuma by container name:

```yaml
# docker/stack.compose.yml
services:
  uptime-kuma:
    image: louislam/uptime-kuma:1
    hostname: uptime-kuma
    ports: ["3001:3001"]
    volumes: ["uptime_data:/app/data"]

  uptime-kuma-agent-mcp:
    image: example/uptime-kuma-agent@sha256:<digest>
    depends_on: [uptime-kuma]
    environment:
      - UPTIME_KUMA_URL=http://uptime-kuma:3001
      - AUTH_TYPE=password
      - UPTIME_KUMA_USERNAME=admin
      - UPTIME_KUMA_PASSWORD=your_password_here
      - TRANSPORT=streamable-http
      - HOST=0.0.0.0
      - PORT=8000
    ports: ["8000:8000"]

volumes:
  uptime_data:
```

```bash
docker compose -f docker/stack.compose.yml up -d
```

Once the dashboard's first-run setup is complete and the credentials are configured,
the [MCP tools and agent](usage.md) can read monitors, heartbeats, and status from
the running instance.
