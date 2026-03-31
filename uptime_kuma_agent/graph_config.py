import os
from pydantic import BaseModel, ConfigDict
from agent_utilities.base_utilities import to_boolean

class GraphConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    mcp_url: str | None = None
    mcp_config: str | None = None
    custom_skills_directory: str | None = None

TAG_PROMPTS: dict[str, str] = {
    "monitors": "You are an Uptime Kuma Monitoring specialist. Help users manage, create, delete, list, pause, and resume monitors.",
    "status": "You are an Uptime Kuma Status specialist. Check monitor status, test host reachability, and check overall uptime metrics.",
    "notifications": "Manage Uptime Kuma notification providers and settings.",
    "proxies": "Manage Uptime Kuma proxies.",
    "status_pages": "Manage public Uptime Kuma status pages.",
    "maintenance": "Manage Uptime Kuma maintenance windows.",
}

TAG_ENV_VARS: dict[str, str] = {
    "monitors": "MONITORSTOOL",
    "status": "STATUSTOOL",
    "notifications": "NOTIFICATIONSTOOL",
    "proxies": "PROXYTOOL",
    "status_pages": "STATUSPAGETOOL",
    "maintenance": "MAINTENANCETOOL",
}

def get_sys_prompt(raw_query: str) -> str:
    active_prompts = []
    has_active_tags = False

    for tag, env_var in TAG_ENV_VARS.items():
        if to_boolean(os.getenv(env_var, "True")):
            has_active_tags = True
            if tag in TAG_PROMPTS:
                active_prompts.append(TAG_PROMPTS[tag])

                                                        
    if not active_prompts and has_active_tags:
        active_prompts.append("You are an Uptime Kuma Agent specialist.")

    domain_sys_prompt = " ".join(active_prompts)

    return f"""
You are the Uptime Kuma Agent, a specialized AI assistant designed to manage Uptime Kuma servers.
{domain_sys_prompt}

Your task is to answer the following query:
{raw_query}
"""
