from agent_utilities.core.config import setting
from uptime_kuma_api import UptimeKumaApi

_client = None


def get_client() -> UptimeKumaApi:
    """Connect + authenticate to Uptime Kuma, caching the client.

    Fails VERBOSELY: the socket.io client otherwise surfaces opaque
    ``Timed out while waiting for event Event.INFO`` on a bad URL and a bare
    ``Incorrect username or password`` on bad creds — neither says which step
    failed or how to fix it. We distinguish CONNECT vs LOGIN vs UNCONFIGURED and
    include the target URL + a remediation hint. A generous connect ``timeout``
    (default 30s, overridable via ``UPTIME_KUMA_TIMEOUT``) absorbs
    cluster/ingress latency that makes the library's short default time out.
    """
    global _client
    if _client is not None:
        return _client

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
            f"Uptime Kuma CONNECT failed to {base_url!r} (timeout={timeout}s): "
            f"{type(e).__name__}: {e}. Verify UPTIME_KUMA_URL points at the reachable "
            f"Uptime Kuma socket.io endpoint (a Service DNS name, not a stale host)."
        ) from e

    if not (username and password):
        try:
            client.disconnect()
        except Exception:
            pass
        raise RuntimeError(
            f"Uptime Kuma auth is NOT configured for {base_url!r}: set "
            f"UPTIME_KUMA_USERNAME + UPTIME_KUMA_PASSWORD (or UPTIME_KUMA_TOKEN / "
            f"SUPERTOKEN as 'user:pass' or a bare password) to valid admin credentials."
        )

    try:
        client.login(username, password)
    except Exception as e:
        try:
            client.disconnect()
        except Exception:
            pass
        raise RuntimeError(
            f"Uptime Kuma LOGIN failed for user {username!r} at {base_url!r}: "
            f"{type(e).__name__}: {e}. Check the credentials (UPTIME_KUMA_USERNAME/"
            f"UPTIME_KUMA_PASSWORD); reset the admin password if unknown."
        ) from e

    _client = client
    return _client
