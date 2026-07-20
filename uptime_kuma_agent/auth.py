from __future__ import annotations

from typing import TYPE_CHECKING, Any

from agent_utilities.core.config import setting

if TYPE_CHECKING:
    from uptime_kuma_api import UptimeKumaApi

_client: Any = None


def get_client() -> UptimeKumaApi:
    """Connect + authenticate to Uptime Kuma, caching the client.

    Fails with actionable, privacy-safe diagnostics: the socket.io client otherwise surfaces opaque
    ``Timed out while waiting for event Event.INFO`` on a bad URL and a bare
    ``Incorrect username or password`` on bad creds — neither says which step
    failed or how to fix it. We distinguish CONNECT vs LOGIN vs UNCONFIGURED and
    include a remediation hint without echoing endpoint or identity values. A generous connect ``timeout``
    (default 30s, overridable via ``UPTIME_KUMA_TIMEOUT``) absorbs
    cluster/ingress latency that makes the library's short default time out.
    """
    global _client
    if _client is not None:
        return _client

    from uptime_kuma_api import UptimeKumaApi

    base_url = setting("UPTIME_KUMA_URL", "http://localhost:3001")
    # Accept several credential env names. SUPERTOKEN is the name the deployed
    # stack injects; UPTIME_KUMA_TOKEN is the documented one. Either may be
    # "user:pass" or a bare password (username defaults to admin).
    token = setting("UPTIME_KUMA_TOKEN", "") or setting("SUPERTOKEN", "")
    username = setting("UPTIME_KUMA_USERNAME", "")
    password = setting("UPTIME_KUMA_PASSWORD", "")
    timeout = int(setting("UPTIME_KUMA_TIMEOUT", "30"))

    if token and not (username and password):
        if ":" in token:
            username, password = token.split(":", 1)
        else:
            username, password = (username or "admin"), token

    try:
        client = UptimeKumaApi(base_url, timeout=timeout)
    except Exception as e:
        raise RuntimeError(
            f"Uptime Kuma CONNECT failed ({type(e).__name__}). Verify UPTIME_KUMA_URL "
            "points at a reachable socket.io endpoint."
        ) from None

    if not (username and password):
        try:
            client.disconnect()
        except Exception:
            pass
        raise RuntimeError(
            "Uptime Kuma auth is not configured: set UPTIME_KUMA_USERNAME and "
            "UPTIME_KUMA_PASSWORD, or configure a supported token reference."
        )

    try:
        client.login(username, password)
    except Exception as e:
        try:
            client.disconnect()
        except Exception:
            pass
        raise RuntimeError(
            f"Uptime Kuma LOGIN failed ({type(e).__name__}). Check the configured credentials."
        ) from None

    _client = client
    return _client
