"""Typed operation surface over the upstream ``uptime_kuma_api`` client.

Eight upstream methods take only ``**kwargs``, which an MCP input schema cannot
describe. ``operations_class`` returns a subclass whose versions take one typed
``config`` object (the same fields the upstream method accepts) and still accept
keyword arguments, so programmatic callers are unaffected.
"""

from __future__ import annotations

from typing import Any

_CONFIG_METHODS = (
    "add_docker_host",
    "add_maintenance",
    "add_monitor",
    "add_notification",
    "add_proxy",
    "add_tag",
    "test_docker_host",
    "test_notification",
)

_cached: type[Any] | None = None


def _config_method(name: str):
    def method(self: Any, config: dict[str, Any] | None = None, **kwargs: Any) -> dict:
        upstream = getattr(super(type(self), self), name)
        return upstream(**{**(config or {}), **kwargs})

    method.__name__ = name
    method.__doc__ = (
        f"{name.replace('_', ' ').capitalize()}: ``config`` carries the upstream "
        "keyword arguments (see the Uptime Kuma API for the fields)."
    )
    return method


def operations_class() -> type[Any]:
    """The upstream client class with typed signatures for the kwargs-only methods."""
    global _cached
    if _cached is None:
        from uptime_kuma_api import UptimeKumaApi

        _cached = type(
            "UptimeKumaOperations",
            (UptimeKumaApi,),
            {name: _config_method(name) for name in _CONFIG_METHODS},
        )
    return _cached
