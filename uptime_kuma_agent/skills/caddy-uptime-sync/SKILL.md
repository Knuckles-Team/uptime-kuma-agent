---
name: caddy-uptime-sync
skill_type: skill
description: >-
  Synchronizes DNS entries from Caddy to Uptime Kuma monitors. Use when the user asks to sync Caddy domains to Uptime Kuma, add missing caddy entries to uptime kuma, or compare Caddy config with Uptime Kuma.
license: MIT
tags: [caddy, uptime-kuma, sync, monitors, networking, ops]
metadata:
  author: Repository Maintainers
  version: '0.1.21'
---
# Caddy to Uptime Kuma Sync

This skill orchestrates the synchronization of domain entries from a Caddy configuration into Uptime Kuma monitors.

## Steps

1. Read the Caddy routes with the Caddy MCP tool `get_routes`(), or `get_config`() when routes are unavailable. Verify the response lists at least one host matcher or upstream.
2. List the current monitors with `uptime_kuma_get_monitors`(). Verify the response is a list whose URLs or hostnames can be compared with the Caddy hosts.
3. Compare the two lists with `diff <(sort caddy_hosts.txt) <(sort kuma_hosts.txt)` into "missing from Uptime Kuma" and "missing from Caddy". Verify each domain appears in exactly one of the two lists, or in neither when it is already synchronized.
4. Show both lists to the user and ask for approval with the question `Add, remove, or both?`. Verify an explicit reply naming the items to add and the items to remove before any change.
5. Create approved monitors with `uptime_kuma_add_monitor`(config), and delete approved orphans with `uptime_kuma_delete_monitor`(id_). Verify a second `uptime_kuma_get_monitors`() call lists every added URL and none of the removed ones.

## Failure recovery

| Failure | Cause | Recovery |
|---------|-------|----------|
| `get_routes` returns no hosts | Caddy MCP server not connected or config has no host matchers | Connect the `caddy-mcp` server, call `get_config`() and read host matchers from the returned JSON |
| `uptime_kuma_get_monitors` is rejected | No active Uptime Kuma session | Call `uptime_kuma_login`(username, password) or `uptime_kuma_connect`(), then fetch the monitors again |
| Added monitor shows the wrong scheme | Scheme guessed instead of read from Caddy TLS settings | Edit it with `uptime_kuma_edit_monitor`(id_, config) using the scheme from the Caddy config |

## Workflow

1. **Retrieve Caddy Configuration**
   - Connect to the Caddy MCP server (typically `caddy-mcp`).
   - Use the available Caddy MCP tools (e.g., `get_config` or `get_routes`) to extract the current Caddy configuration.
   - Parse the configuration to compile a comprehensive list of all configured domain names (host matchers or upstream servers).

2. **Retrieve Uptime Kuma Monitors**
   - Connect to the Uptime Kuma MCP server (typically `uptime-kuma-mcp` or `uptime-mcp`).
   - Use the available Uptime Kuma MCP tools to fetch the list of all currently configured monitors.
   - Extract the URLs or domains being monitored by Uptime Kuma.

3. **Compare and Identify Deltas**
   - Identify domains present in Caddy but **missing** from Uptime Kuma.
   - Identify domains present in Uptime Kuma but **missing** from Caddy.

4. **Request User Confirmation**
   - Present a clearly formatted Markdown list to the user showing:
     - **To be added to Uptime Kuma**: [List of domains]
     - **Missing from Caddy (potentially to be removed from Uptime Kuma)**: [List of domains]
   - **WAIT** for the user's explicit confirmation before making any modifications. Ask the user if they want to add the missing items, remove the orphaned items, or both.

5. **Execute Synchronization**
   - Ask the user for their preferred default monitor interval and any other specific Uptime Kuma settings they would like applied to the new monitors.
   - Upon receiving user approval, use the Uptime Kuma MCP tools to create new monitors for the approved domains.
   - Infer whether the site is HTTP or HTTPS based directly on the Caddy configuration (e.g., if it has TLS configured or is explicitly listening on a secure port). Do NOT blindly assume HTTPS.
   - If the user approved removing orphaned monitors, use the appropriate Uptime Kuma tool to delete them.
   - Provide a final summary of the operations completed.
