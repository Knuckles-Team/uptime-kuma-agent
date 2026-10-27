"""Privacy-safe projection of Uptime Kuma monitor and heartbeat data."""

from datetime import UTC, datetime
from typing import Any

MAX_MONITORS = 1000
MAX_HEARTBEATS = 100_000


def _timestamp(value: Any) -> datetime:
    if not isinstance(value, str) or not value or len(value) > 64:
        raise ValueError("invalid heartbeat time")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise ValueError("invalid heartbeat time") from None
    return (
        parsed.replace(tzinfo=UTC) if parsed.tzinfo is None else parsed.astimezone(UTC)
    )


def service_health(monitors: Any, heartbeats: Any) -> list[dict[str, Any]]:
    """Return source-observed health, refusing ambiguous or oversized data."""
    if not isinstance(monitors, list) or len(monitors) > MAX_MONITORS:
        raise ValueError("invalid monitor list")
    if not isinstance(heartbeats, dict):
        raise ValueError("invalid heartbeat list")
    by_id: dict[str, list[Any]] = {}
    inspected = 0
    for raw_id, beats in heartbeats.items():
        if isinstance(raw_id, bool) or not isinstance(raw_id, int | str):
            raise ValueError("invalid heartbeat identity")
        key = str(raw_id)
        if not key or len(key) > 128 or key in by_id or not isinstance(beats, list):
            raise ValueError("invalid heartbeat list")
        inspected += len(beats)
        if inspected > MAX_HEARTBEATS:
            raise ValueError("heartbeat limit exceeded")
        by_id[key] = beats
    rows = []
    seen: set[str] = set()
    for monitor in monitors:
        if not isinstance(monitor, dict):
            raise ValueError("invalid monitor")
        identifier, name = monitor.get("id"), monitor.get("name")
        if isinstance(identifier, bool) or not isinstance(identifier, int | str):
            raise ValueError("invalid monitor identity")
        key = str(identifier)
        if (
            not key
            or len(key) > 128
            or key in seen
            or not isinstance(name, str)
            or not name.strip()
            or len(name) > 1024
        ):
            raise ValueError("invalid monitor identity")
        seen.add(key)
        beats = by_id.get(key, [])
        latest = None
        for beat in beats:
            if not isinstance(beat, dict):
                raise ValueError("invalid heartbeat")
            when = _timestamp(beat.get("time"))
            status = beat.get("status")
            if (
                isinstance(status, bool)
                or not isinstance(status, int)
                or status not in (0, 1, 2, 3)
            ):
                raise ValueError("invalid heartbeat status")
            candidate = (when, int(status))
            if latest is None or when > latest[0]:
                latest = candidate
            elif when == latest[0] and candidate[1] != latest[1]:
                raise ValueError("ambiguous heartbeat")
        rows.append(
            {
                "id": key,
                "name": name,
                "status": latest[1] if latest else None,
                "last_check": latest[0].isoformat() if latest else None,
            }
        )
    return rows
