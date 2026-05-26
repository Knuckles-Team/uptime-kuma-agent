import runpy
from unittest.mock import patch
import pytest


@pytest.mark.concept("CONCEPT:UKA-006")
@patch("uptime_kuma_agent.agent_server.agent_server")
def test_main_execution(mock_agent_server):
    # Use runpy to execute the __main__.py file, mocking the actual server function
    runpy.run_module("uptime_kuma_agent.__main__", run_name="__main__")
    mock_agent_server.assert_called_once()
