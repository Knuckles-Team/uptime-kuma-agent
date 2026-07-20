# Uptime Kuma Sync

Synchronize Caddy reverse proxy routes into Uptime Kuma as HTTP monitors. Parses the Caddyfile for configured host suffixes, deduplicates them, appends `/health` suffixes for MCP service endpoints, and inserts missing monitors directly into the Uptime Kuma SQLite database. Use when the user says "sync monitors", "register uptime monitors", "update kuma", "add missing monitors", "sync caddy to uptime kuma", or after deploying a new service that needs health monitoring. Do not use this workflow to query existing monitor status.

# Uptime Kuma Sync Skill

Atomic operation to discover all Caddy-fronted service routes and ensure each has a corresponding HTTP monitor in Uptime Kuma.

## Prerequisites

- **Caddyfile** accessible on the host filesystem (default: `[REDACTED_POSIX_USER_PATH]
- **Uptime Kuma SQLite database** accessible on the host filesystem (default: `[REDACTED_POSIX_USER_PATH]
- Python 3.10+ with `sqlite3` (stdlib) and `re` (stdlib) — no external dependencies.

## Configuration

| Variable | Default | Description |
|---|---|---|
| `CADDYFILE_PATH` | `[REDACTED_POSIX_USER_PATH] | Absolute path to the Caddy server block configuration |
| `KUMA_DB_PATH` | `[REDACTED_POSIX_USER_PATH] | Absolute path to the Uptime Kuma SQLite database |

Override these by passing `--caddyfile` and `--db` CLI arguments to the script.

## Steps

### Step 1: Parse Caddy Routes

Execute the sync script to parse the Caddyfile and discover all reverse-proxied hostnames:

```bash
python scripts/sync_kuma_monitors.py
```

The script:
1. Reads every line of the Caddyfile.
2. Extracts server-block hostnames, optionally filtered by the comma-separated `MONITOR_HOST_SUFFIXES` environment variable.
3. Uses preceding `# comment` lines as human-readable monitor names (falls back to domain prefix).
4. Deduplicates by URL.
5. Appends `/health` suffix to any URL containing `-mcp` (standard MCP health endpoint).

### Step 2: Insert Missing Monitors

The script connects to the Uptime Kuma SQLite database and:
1. Queries all existing `monitor.url` values.
2. Skips any monitor whose URL already exists.
3. Inserts new monitors with these defaults:
   - **Type**: `http`
   - **Interval**: `30` seconds
   - **Max Retries**: `3`
   - **Accepted Status Codes**: `200-299`
4. Commits the transaction and prints a summary.

### Step 3: Verify

After execution, confirm the output line:
```
Successfully registered N new monitors in Uptime Kuma.
```

If `N` is `0`, all monitors were already present. Optionally verify in the Uptime Kuma dashboard at `[configured-endpoint]`.

## Customization

To add monitors for additional TLDs or custom domains, edit the hostname matching logic in `scripts/sync_kuma_monitors.py` at the line:
```python
elif "{" in line:
```

## Error Handling

- **Caddyfile not found**: Script exits with a clear error message. Verify `CADDYFILE_PATH`.
- **Database locked**: Uptime Kuma may lock its SQLite database during writes. Retry after a few seconds, or stop the Uptime Kuma container temporarily.
- **Duplicate URL constraint**: The script checks existing URLs before insertion; no duplicates will be created.
