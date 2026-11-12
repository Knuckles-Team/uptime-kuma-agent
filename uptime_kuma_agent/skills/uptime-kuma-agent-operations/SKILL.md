---
name: uptime-kuma-agent-operations
skill_type: skill
description: >-
  Operate uptime-kuma-agent through its governed MCP and Arbora capabilities, including caddy uptime sync, uptime kuma sync. Use when a request requires this provider's read, change, automation, ingestion, troubleshooting, or evidence workflows.
---

# Uptime Kuma Agent Operations

Use the provider's governed MCP tools through Arbora delegation.

## Workflow

1. Establish the verified GraphSession and tenant before discovery or retrieval.
2. Discover the current condensed tool surface; never assume a stale tool name or schema.
3. Prefer read-only inspection first. For changes, present impact and use the provider's
   dry-run or preview mode when available.
4. Execute mutations as fenced WorkItems so retries remain idempotent and auditable.
5. Ingest source data only through the signed connector preset and ChangeEnvelope path.
6. Verify the durable result and its trace/evidence before reporting completion.

## Safety contract

- Never persist credentials, endpoints, raw personal identifiers, hostnames, or local paths.
- Resolve TLS trust and verification from environment/configuration; never hardcode bypasses.
- Treat unknown ACL, tenant, schema, or tool-contract state as a hard failure.
- Require explicit approval for destructive, externally visible, or irreversible actions.
- Keep runtime traces policy-scoped and privacy-sanitized.

## Specialized workflows

Read [the workflow catalog](references/catalog.md) only when the request needs a
provider-specific procedure, parameter map, script, or reference asset.

## Tools by task

Every served tool is named below under the task it serves. Pass each argument by name.

- **triage-monitor-health**: Read monitor state and recent heartbeats to tell a flapping monitor from a sustained outage. `uptime_kuma_service_health`, `uptime_kuma_get_monitors`, `uptime_kuma_get_monitor`, `uptime_kuma_get_monitor_status`, `uptime_kuma_get_heartbeats`, `uptime_kuma_get_important_heartbeats`, `uptime_kuma_get_monitor_beats`, `uptime_kuma_uptime`, `uptime_kuma_avg_ping`, `uptime_kuma_cert_info`
- **manage-monitors**: Add, change, pause, resume and retire monitors. `uptime_kuma_add_monitor`, `uptime_kuma_edit_monitor`, `uptime_kuma_pause_monitor`, `uptime_kuma_resume_monitor`, `uptime_kuma_delete_monitor`
- **organise-monitors-with-tags**: Create tags and apply them to monitors. `uptime_kuma_get_tags`, `uptime_kuma_get_tag`, `uptime_kuma_add_tag`, `uptime_kuma_edit_tag`, `uptime_kuma_delete_tag`, `uptime_kuma_add_monitor_tag`, `uptime_kuma_delete_monitor_tag`
- **schedule-maintenance**: Open a maintenance window, attach monitors and status pages, and pause or resume it. `uptime_kuma_get_maintenances`, `uptime_kuma_get_maintenance`, `uptime_kuma_add_maintenance`, `uptime_kuma_edit_maintenance`, `uptime_kuma_pause_maintenance`, `uptime_kuma_resume_maintenance`, `uptime_kuma_delete_maintenance`, `uptime_kuma_get_monitor_maintenance`, `uptime_kuma_add_monitor_maintenance`, `uptime_kuma_get_status_page_maintenance`, `uptime_kuma_add_status_page_maintenance`
- **publish-status-page**: Create and save a public status page and post or unpin an incident on it. `uptime_kuma_get_status_pages`, `uptime_kuma_get_status_page`, `uptime_kuma_add_status_page`, `uptime_kuma_save_status_page`, `uptime_kuma_delete_status_page`, `uptime_kuma_post_incident`, `uptime_kuma_unpin_incident`
- **configure-notifications**: Create, test and remove the notification providers that alert on state changes. `uptime_kuma_check_apprise`, `uptime_kuma_get_notifications`, `uptime_kuma_get_notification`, `uptime_kuma_add_notification`, `uptime_kuma_edit_notification`, `uptime_kuma_test_notification`, `uptime_kuma_delete_notification`
- **configure-proxies-and-docker-hosts**: Manage the proxies and Docker hosts that monitors reach their targets through. `uptime_kuma_get_proxies`, `uptime_kuma_get_proxy`, `uptime_kuma_add_proxy`, `uptime_kuma_edit_proxy`, `uptime_kuma_delete_proxy`, `uptime_kuma_get_docker_hosts`, `uptime_kuma_get_docker_host`, `uptime_kuma_add_docker_host`, `uptime_kuma_edit_docker_host`, `uptime_kuma_test_docker_host`, `uptime_kuma_delete_docker_host`
- **administer-server**: Read server info and settings and run database housekeeping. `uptime_kuma_info`, `uptime_kuma_get_settings`, `uptime_kuma_set_settings`, `uptime_kuma_get_database_size`, `uptime_kuma_shrink_database`, `uptime_kuma_clear_events`, `uptime_kuma_clear_heartbeats`, `uptime_kuma_clear_statistics`, `uptime_kuma_test_chrome`, `uptime_kuma_get_game_list`, `uptime_kuma_upload_backup`, `uptime_kuma_wait_for_event`
- **manage-access**: Manage the session, credentials, two-factor setup and API keys of the server. `uptime_kuma_connect`, `uptime_kuma_disconnect`, `uptime_kuma_need_setup`, `uptime_kuma_setup`, `uptime_kuma_login`, `uptime_kuma_login_by_token`, `uptime_kuma_logout`, `uptime_kuma_change_password`, `uptime_kuma_twofa_status`, `uptime_kuma_prepare_2fa`, `uptime_kuma_verify_token`, `uptime_kuma_save_2fa`, `uptime_kuma_disable_2fa`, `uptime_kuma_get_api_keys`, `uptime_kuma_get_api_key`, `uptime_kuma_add_api_key`, `uptime_kuma_enable_api_key`, `uptime_kuma_disable_api_key`, `uptime_kuma_delete_api_key`
- **ingest-monitors**: Push the monitors and optional heartbeat samples into the knowledge graph. `uptime_ingest_monitors`
