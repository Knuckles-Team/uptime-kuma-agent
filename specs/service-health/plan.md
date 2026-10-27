# Service health implementation plan

Read monitors and heartbeat lists from the existing Uptime Kuma client. Select
the latest valid heartbeat by its timestamp and return only the four declared
fields. Bound the number of monitors and inspected heartbeats. The SDK access
contract names the served operation. A synthetic provider exercises the real
MCP call. The connector does not claim an approved engine virtual mapping.
