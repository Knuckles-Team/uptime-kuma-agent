# Provider workflow catalog

Load only the workflow relevant to the current request.

- [caddy-uptime-sync](../../caddy-uptime-sync/WORKFLOW.md): Synchronizes DNS entries from Caddy to Uptime Kuma monitors. Use when the user asks to sync Caddy domains to Uptime Kuma, add missing caddy entries to uptime kuma, or compare Caddy config with Uptime Kuma.
- [uptime-kuma-sync](../../uptime-kuma-sync/WORKFLOW.md): Synchronize Caddy reverse-proxy routes into Uptime Kuma as HTTP monitors. It discovers configured host suffixes, deduplicates them, and applies service health paths without embedding environment-specific domains or filesystem locations.
