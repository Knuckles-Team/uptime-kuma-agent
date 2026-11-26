---
name: uptime-kuma-sync
skill_type: skill
description: >-
  Synchronize Caddy reverse proxy routes into Uptime Kuma as HTTP monitors. Use when the user says "sync monitors", "register uptime monitors", "update kuma", "add missing monitors", "sync caddy to uptime kuma", or after deploying a new service that needs health monitoring. Do NOT use for querying existing monitor status — use uptime-kuma-agent or the Uptime Kuma dashboard directly.
license: MIT
tags: [uptime-kuma, monitoring, caddy, health-checks, sync, infrastructure]
metadata:
  author: Repository Maintainers
  version: '0.17.0'
---

# Uptime Kuma Sync Skill

Scope: Synchronize Caddy reverse proxy routes into Uptime Kuma as HTTP monitors. Parses the Caddyfile for all .arpa hostnames, deduplicates them, appends /health suffixes for MCP service endpoints, and inserts missing monitors directly into the Uptime Kuma SQLite database. Use when the user says "sync monitors", "register uptime monitors", "update kuma", "add missing monitors", "sync caddy to uptime kuma", or after deploying a new service that needs health monitoring. Do NOT use for querying existing monitor status — use uptime-kuma-agent or the Uptime Kuma dashboard directly.

Atomic operation to discover all Caddy-fronted service routes and ensure each has a corresponding HTTP monitor in Uptime Kuma.

## Prerequisites

- **Caddyfile** accessible on the host filesystem (default: `/etc/caddy/Caddyfile`).
- **Uptime Kuma SQLite database** accessible on the host filesystem (default: `/var/lib/uptime-kuma/data/kuma.db`).
- Python 3.10+ with `sqlite3` (stdlib) and `re` (stdlib) — no external dependencies.

## Configuration

| Variable | Default | Description |
|---|---|---|
| `CADDYFILE_PATH` | `/etc/caddy/Caddyfile` | Absolute path to the Caddy server block configuration |
| `KUMA_DB_PATH` | `/var/lib/uptime-kuma/data/kuma.db` | Absolute path to the Uptime Kuma SQLite database |

Override these by passing `--caddyfile` and `--db` CLI arguments to the script.

## Steps

1. Confirm the inputs exist with `ls -l "$CADDYFILE_PATH" "$KUMA_DB_PATH"`. Verify both paths are listed.
2. Run `python scripts/sync_kuma_monitors.py` (add `--caddyfile` and `--db` to override paths). Verify the script exits with status 0 and prints no traceback.
3. Read the summary line of the script output. Verify it matches `Successfully registered N new monitors in Uptime Kuma.`, where `N` is 0 when every route already had a monitor.
4. Re-run `python scripts/sync_kuma_monitors.py`. Verify it now reports 0 new monitors, which proves no duplicates are created.

## Failure recovery

| Failure | Cause | Recovery |
|---------|-------|----------|
| Script exits with a Caddyfile error | `CADDYFILE_PATH` points to a missing file | Set `CADDYFILE_PATH` to the real file or pass `--caddyfile <path>` |
| `database is locked` | Uptime Kuma holds a write lock on the SQLite file | Stop the Uptime Kuma container, run `python scripts/sync_kuma_monitors.py`, then start the container again |
| Summary reports 0 monitors for new hosts | Hostnames do not match the TLD filter in the script | Edit the hostname match line in `scripts/sync_kuma_monitors.py` as shown under Customization and run it again |

## Script behavior

### Parse Parse Caddy Routes

Execute the sync script to parse the Caddyfile and discover all reverse-proxied hostnames:

```bash
python scripts/sync_kuma_monitors.py
```

The script:
1. Reads every line of the Caddyfile.
2. Extracts hostnames matching `.arpa` or other configured TLDs from server block declarations.
3. Uses preceding `# comment` lines as human-readable monitor names (falls back to domain prefix).
4. Deduplicates by URL.
5. Appends `/health` suffix to any URL containing `-mcp` (standard MCP health endpoint).

### Insert Insert Missing Monitors

The script connects to the Uptime Kuma SQLite database and:
1. Queries all existing `monitor.url` values.
2. Skips any monitor whose URL already exists.
3. Inserts new monitors with these defaults:
   - **Type**: `http`
   - **Interval**: `30` seconds
   - **Max Retries**: `3`
   - **Accepted Status Codes**: `200-299`
4. Commits the transaction and prints a summary.

### Verify output

After execution, confirm the output line:
```
Successfully registered N new monitors in Uptime Kuma.
```

If `N` is `0`, all monitors were already present. Optionally verify in the Uptime Kuma dashboard at `https://uptime.example.invalid`.

## Customization

To add monitors for additional TLDs or custom domains, edit the hostname matching logic in `scripts/sync_kuma_monitors.py` at the line:
```python
elif (".arpa" in line or "your-domain.com" in line) and "{" in line:
```

## Error Handling

- **Caddyfile not found**: Script exits with a clear error message. Verify `CADDYFILE_PATH`.
- **Database locked**: Uptime Kuma may lock its SQLite database during writes. Retry after a few seconds, or stop the Uptime Kuma container temporarily.
- **Duplicate URL constraint**: The script checks existing URLs before insertion; no duplicates will be created.
