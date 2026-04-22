import os

from uptime_kuma_api import UptimeKumaApi

_client = None


def get_client() -> UptimeKumaApi:
    global _client
    if _client is None:
        base_url = os.getenv("UPTIME_KUMA_URL", "http://localhost:3001")

        token = os.getenv("UPTIME_KUMA_TOKEN", "")

        username = os.getenv("UPTIME_KUMA_USERNAME", "")
        password = os.getenv("UPTIME_KUMA_PASSWORD", "")

        try:
            _client = UptimeKumaApi(base_url)

            if token and not username and not password:
                if ":" in token:
                    parts = token.split(":", 1)
                    username = parts[0]
                    password = parts[1]
                else:
                    username = "admin"
                    password = token

            if username and password:
                _client.login(username, password)

        except Exception as e:
            _client = None
            raise RuntimeError(
                f"Failed to authenticate with Uptime Kuma at {base_url}: {e}"
            ) from e

    return _client
