# MCP_AGENTS.md - Dynamic Agent Registry

This file tracks the generated agents from MCP servers. You can manually modify the 'Tools' list to customize agent expertise.

## Agent Mapping Table

| Name | Description | System Prompt | Tools | Tag | Source MCP |
|------|-------------|---------------|-------|-----|------------|
| Uptime Monitors Specialist | Expert specialist for monitors domain tasks. | You are a Uptime Monitors specialist. Help users manage and interact with Monitors functionality using the available tools. | uptime_monitors_toolset | monitors | uptime |
| Uptime Status Specialist | Expert specialist for status domain tasks. | You are a Uptime Status specialist. Help users manage and interact with Status functionality using the available tools. | uptime_status_toolset | status | uptime |

## Tool Inventory Table

| Tool Name | Description | Tag | Source |
|-----------|-------------|-----|--------|
| uptime_monitors_toolset | Static hint toolset for monitors based on config env. | monitors | uptime |
| uptime_status_toolset | Static hint toolset for status based on config env. | status | uptime |
