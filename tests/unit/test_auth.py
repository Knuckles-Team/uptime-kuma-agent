import os
from unittest.mock import MagicMock, patch
import pytest

import uptime_kuma_agent.auth as auth
from uptime_kuma_agent.auth import get_client


@pytest.fixture(autouse=True)
def reset_global_client():
    # Reset global _client before each test to ensure they are isolated
    auth._client = None
    yield
    auth._client = None


@pytest.mark.concept("CONCEPT:UK-OS.identity.uka")
@patch("uptime_kuma_agent.auth.UptimeKumaApi")
def test_get_client_caching(mock_api_class):
    mock_api_instance = MagicMock()
    mock_api_class.return_value = mock_api_instance

    client1 = get_client()
    client2 = get_client()

    assert client1 is mock_api_instance
    assert client2 is mock_api_instance
    # UptimeKumaApi should only be instantiated once
    mock_api_class.assert_called_once_with("http://localhost:3001")


@pytest.mark.concept("CONCEPT:UK-OS.identity.uka")
@patch("uptime_kuma_agent.auth.UptimeKumaApi")
@patch.dict(
    os.environ,
    {"UPTIME_KUMA_USERNAME": "testuser", "UPTIME_KUMA_PASSWORD": "testpassword"},
)
def test_get_client_user_pass(mock_api_class):
    mock_api_instance = MagicMock()
    mock_api_class.return_value = mock_api_instance

    client = get_client()
    assert client is mock_api_instance
    mock_api_instance.login.assert_called_once_with("testuser", "testpassword")


@pytest.mark.concept("CONCEPT:UK-OS.identity.uka")
@patch("uptime_kuma_agent.auth.UptimeKumaApi")
@patch.dict(os.environ, {"UPTIME_KUMA_TOKEN": "myuser:mytoken"})
def test_get_client_token_split(mock_api_class):
    mock_api_instance = MagicMock()
    mock_api_class.return_value = mock_api_instance

    client = get_client()
    assert client is mock_api_instance
    mock_api_instance.login.assert_called_once_with("myuser", "mytoken")


@pytest.mark.concept("CONCEPT:UK-OS.identity.uka")
@patch("uptime_kuma_agent.auth.UptimeKumaApi")
@patch.dict(os.environ, {"UPTIME_KUMA_TOKEN": "justatoken"})
def test_get_client_token_no_split(mock_api_class):
    mock_api_instance = MagicMock()
    mock_api_class.return_value = mock_api_instance

    client = get_client()
    assert client is mock_api_instance
    mock_api_instance.login.assert_called_once_with("admin", "justatoken")


@pytest.mark.concept("CONCEPT:UK-OS.identity.uka")
@patch("uptime_kuma_agent.auth.UptimeKumaApi")
def test_get_client_failure(mock_api_class):
    mock_api_class.side_effect = Exception("Connection Refused")

    with pytest.raises(RuntimeError) as exc_info:
        get_client()

    assert "Failed to authenticate with Uptime Kuma at http://localhost:3001" in str(
        exc_info.value
    )
    assert auth._client is None
