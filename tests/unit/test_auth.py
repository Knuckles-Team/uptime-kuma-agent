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


def _connected_client() -> MagicMock:
    client = MagicMock()
    client.sio.connected = True
    client.sio.namespaces = {"/": "connected"}
    return client


@pytest.mark.concept("CONCEPT:UK-OS.identity.uka")
@patch("uptime_kuma_agent.auth._new_client")
@patch.dict(
    "os.environ",
    {"UPTIME_KUMA_USERNAME": "testuser", "UPTIME_KUMA_PASSWORD": "testpassword"},
    clear=True,
)
def test_get_client_caching(mock_new_client):
    mock_api_instance = _connected_client()
    mock_new_client.return_value = mock_api_instance

    assert get_client() is mock_api_instance
    assert get_client() is mock_api_instance

    mock_new_client.assert_called_once_with("http://localhost:3001", timeout=30)


@pytest.mark.concept("CONCEPT:UK-OS.identity.uka")
@patch("uptime_kuma_agent.auth._new_client")
@patch.dict(
    "os.environ",
    {"UPTIME_KUMA_USERNAME": "testuser", "UPTIME_KUMA_PASSWORD": "testpassword"},
    clear=True,
)
def test_get_client_user_pass(mock_new_client):
    mock_api_instance = _connected_client()
    mock_new_client.return_value = mock_api_instance

    client = get_client()
    assert client is mock_api_instance
    mock_api_instance.login.assert_called_once_with("testuser", "testpassword")
    assert get_client() is mock_api_instance
    mock_new_client.assert_called_once_with("http://localhost:3001", timeout=30)


@pytest.mark.concept("CONCEPT:UK-OS.identity.uka")
@patch("uptime_kuma_agent.auth._new_client")
@patch.dict("os.environ", {"UPTIME_KUMA_TOKEN": "myuser:mytoken"}, clear=True)
def test_get_client_token_split(mock_new_client):
    mock_api_instance = _connected_client()
    mock_new_client.return_value = mock_api_instance

    client = get_client()
    assert client is mock_api_instance
    mock_api_instance.login.assert_called_once_with("myuser", "mytoken")


@pytest.mark.concept("CONCEPT:UK-OS.identity.uka")
@patch("uptime_kuma_agent.auth._new_client")
@patch.dict("os.environ", {"UPTIME_KUMA_TOKEN": "justatoken"}, clear=True)
def test_get_client_token_no_split(mock_new_client):
    mock_api_instance = _connected_client()
    mock_new_client.return_value = mock_api_instance

    client = get_client()
    assert client is mock_api_instance
    mock_api_instance.login.assert_called_once_with("admin", "justatoken")


@pytest.mark.concept("CONCEPT:UK-OS.identity.uka")
@patch("uptime_kuma_agent.auth._new_client")
@patch.dict("os.environ", {}, clear=True)
def test_get_client_failure(mock_new_client):
    mock_new_client.side_effect = Exception("Connection Refused")

    with pytest.raises(RuntimeError) as exc_info:
        get_client()

    assert "Uptime Kuma CONNECT failed (Exception)" in str(exc_info.value)
    assert auth._client is None


@pytest.mark.concept("CONCEPT:UK-OS.identity.uka")
@patch("uptime_kuma_agent.auth._new_client")
@patch.dict(
    "os.environ",
    {"UPTIME_KUMA_USERNAME": "testuser", "UPTIME_KUMA_PASSWORD": "testpassword"},
    clear=True,
)
def test_get_client_replaces_stale_socket(mock_new_client):
    stale = MagicMock()
    stale.sio.connected = True
    stale.sio.namespaces = {}
    fresh = _connected_client()
    auth._client = stale
    mock_new_client.return_value = fresh

    assert get_client() is fresh

    stale.disconnect.assert_called_once_with()
    fresh.login.assert_called_once_with("testuser", "testpassword")
    assert auth._client is fresh
