import pytest
from uptime_kuma_agent.uptime_kuma_models import (
    UptimeKumaMonitor,
    UptimeKumaMonitorStatus,
)


@pytest.mark.concept("CONCEPT:UK-OS.config.uka")
def test_uptime_kuma_monitor_defaults():
    monitor = UptimeKumaMonitor(name="test_mon", type="http")
    assert monitor.id is None
    assert monitor.name == "test_mon"
    assert monitor.type == "http"
    assert monitor.url is None
    assert monitor.interval == 60
    assert monitor.active is True
    assert monitor.accepted_statuscodes == ["200-299"]


@pytest.mark.concept("CONCEPT:UK-OS.config.uka")
def test_uptime_kuma_monitor_custom():
    monitor = UptimeKumaMonitor(
        id=123,
        name="custom_mon",
        type="ping",
        url="http://test.com",
        interval=30,
        active=False,
        accepted_statuscodes=["200", "301"],
    )
    assert monitor.id == 123
    assert monitor.name == "custom_mon"
    assert monitor.type == "ping"
    assert monitor.url == "http://test.com"
    assert monitor.interval == 30
    assert monitor.active is False
    assert monitor.accepted_statuscodes == ["200", "301"]


@pytest.mark.concept("CONCEPT:UK-OS.config.uka")
def test_uptime_kuma_monitor_status():
    status = UptimeKumaMonitorStatus(
        id=456,
        name="status_mon",
        type="http",
        url="http://status.com",
        status="up",
    )
    assert status.id == 456
    assert status.name == "status_mon"
    assert status.type == "http"
    assert status.url == "http://status.com"
    assert status.status == "up"
