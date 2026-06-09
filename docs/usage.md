# Usage — API / CLI / MCP

`uptime-kuma-agent` exposes the same capability three ways: as **MCP tools** an agent
calls, as a **Python API** (`UptimeKumaApi`) you import, and as an **agent CLI**.

## As an MCP server

Once [deployed](deployment.md), the server registers two consolidated, action-routed
tools. Each is togglable through its environment switch.

| Tool | Toggle | Actions |
|---|---|---|
| `uptime_kuma_monitors` | `MONITORSTOOL` | `get_monitors`, `get_monitor`, `add_monitor`, `edit_monitor`, `delete_monitor`, `pause_monitor`, `resume_monitor` |
| `uptime_kuma_status` | `STATUSTOOL` | `get_heartbeats`, `info` |

Each tool takes an `action` and a `params_json` string, so a single tool covers a
whole family of operations without inflating the model's context.

Example agent prompts that map onto these tools:

- *"List all the monitors and tell me which ones are down."* → `uptime_kuma_monitors` (`get_monitors`)
- *"Pause the monitor with ID 7."* → `uptime_kuma_monitors` (`pause_monitor`)
- *"Show the recent heartbeats and the system info."* → `uptime_kuma_status` (`get_heartbeats`, `info`)

## As a Python API

The connector wraps [`uptime-kuma-api`](https://pypi.org/project/uptime-kuma-api/).
Build an authenticated client straight from the environment with `get_client()`:

```python
from uptime_kuma_agent.auth import get_client

# Reads UPTIME_KUMA_URL / UPTIME_KUMA_USERNAME / UPTIME_KUMA_PASSWORD
# (or UPTIME_KUMA_TOKEN) from the environment and logs in.
client = get_client()

# Reads
monitors = client.get_monitors()              # all configured monitors
monitor = client.get_monitor(1)               # a single monitor by id
heartbeats = client.get_heartbeats()          # recent heartbeat records
info = client.info()                          # server stats / general info
```

You can also construct the underlying client directly:

```python
from uptime_kuma_api import UptimeKumaApi

client = UptimeKumaApi("http://localhost:3001")
client.login("admin", "your_password_here")
print(client.get_monitors())
client.disconnect()
```

### Writes

The same client performs monitor mutations once you are authenticated:

```python
client.add_monitor(type="http", name="Example", url="https://example.com")
client.edit_monitor(1, name="Renamed monitor")
client.pause_monitor(1)
client.resume_monitor(1)
client.delete_monitor(1)
```

## As an agent CLI

The integrated Pydantic AI graph agent runs as the `uptime-agent` console script. It
connects to the MCP server and exposes a conversational interface plus a web UI:

```bash
export UPTIME_KUMA_URL=http://localhost:3001
export AUTH_TYPE=password
export UPTIME_KUMA_USERNAME=admin
export UPTIME_KUMA_PASSWORD=your_password_here

uptime-agent --provider openai --model-id gpt-4o
```

When deployed alongside the MCP server (see [Deployment](deployment.md#agent-server)),
the agent reads `MCP_URL` to reach the tool surface and serves its web UI on `:9004`.
