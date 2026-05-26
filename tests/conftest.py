import pytest
from unittest.mock import MagicMock
import uptime_kuma_agent


@pytest.fixture(autouse=True)
def clean_loaded_modules():
    """Resets cache and clears optional modules for complete unit test isolation."""
    uptime_kuma_agent._loaded_optional_modules.clear()
    original_all = list(uptime_kuma_agent.__all__)
    yield
    uptime_kuma_agent._loaded_optional_modules.clear()
    uptime_kuma_agent.__all__ = original_all


@pytest.fixture
def mock_client():
    """Provides a pre-configured mocked Uptime Kuma Api client."""
    client = MagicMock()
    return client
