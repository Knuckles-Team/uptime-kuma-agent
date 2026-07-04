import logging
import sys
import runpy
from unittest.mock import MagicMock, patch
import pytest

from uptime_kuma_agent.agent_server import agent_server


@pytest.mark.concept("CONCEPT:UK-OS.config.uka-4")
@patch("agent_utilities.initialize_workspace")
@patch("agent_utilities.load_identity")
@patch("agent_utilities.build_system_prompt_from_workspace")
@patch("agent_utilities.create_agent_parser")
@patch("agent_utilities.create_agent_server")
def test_agent_server_normal(
    mock_create_agent_server,
    mock_create_agent_parser,
    mock_build_prompt,
    mock_load_identity,
    mock_init_workspace,
):
    # Mock parser behavior
    mock_parser = MagicMock()
    mock_args = MagicMock()

    mock_args.mcp_url = "http://localhost:8000"
    mock_args.mcp_config = "custom_config.json"
    mock_args.host = "127.0.0.1"
    mock_args.port = 9000
    mock_args.provider = "openai"
    mock_args.model_id = "gpt-4"
    mock_args.base_url = "https://api.openai.com"
    mock_args.api_key = "secret_key"
    mock_args.custom_skills_directory = "/skills"
    mock_args.web = True
    mock_args.otel = True
    mock_args.otel_endpoint = "http://otel"
    mock_args.otel_headers = "header1"
    mock_args.otel_public_key = "pub"
    mock_args.otel_secret_key = "sec"
    mock_args.otel_protocol = "grpc"
    mock_args.debug = False

    mock_parser.parse_args.return_value = mock_args
    mock_create_agent_parser.return_value = mock_parser

    # Mock identity content
    mock_load_identity.return_value = {
        "name": "Mock Uptime Agent",
        "description": "Mocked Description",
        "content": "Mock System Prompt",
    }

    # Execute server
    agent_server()

    # Verify initializations
    mock_init_workspace.assert_called_once()
    mock_load_identity.assert_called_once()

    # Verify create_agent_server called with args
    mock_create_agent_server.assert_called_once_with(
        mcp_url="http://localhost:8000",
        mcp_config="custom_config.json",
        host="127.0.0.1",
        port=9000,
        provider="openai",
        model_id="gpt-4",
        router_model="gpt-4",
        agent_model="gpt-4",
        base_url="https://api.openai.com",
        api_key="secret_key",
        custom_skills_directory="/skills",
        enable_web_ui=True,
        enable_otel=True,
        otel_endpoint="http://otel",
        otel_headers="header1",
        otel_public_key="pub",
        otel_secret_key="sec",
        otel_protocol="grpc",
        debug=False,
    )


@pytest.mark.concept("CONCEPT:UK-OS.config.uka-4")
@patch("agent_utilities.initialize_workspace")
@patch("agent_utilities.load_identity")
@patch("agent_utilities.build_system_prompt_from_workspace")
@patch("agent_utilities.create_agent_parser")
@patch("agent_utilities.create_agent_server")
def test_agent_server_debug_mode(
    mock_create_agent_server,
    mock_create_agent_parser,
    mock_build_prompt,
    mock_load_identity,
    mock_init_workspace,
):
    mock_parser = MagicMock()
    mock_args = MagicMock()
    mock_args.debug = True
    mock_args.mcp_config = None  # Check coverage of config fallback
    mock_parser.parse_args.return_value = mock_args
    mock_create_agent_parser.return_value = mock_parser

    mock_load_identity.return_value = {}  # Return empty to check defaults
    mock_build_prompt.return_value = "System prompt fallback"

    # Set logger to high level to check it gets modified
    logging.getLogger().setLevel(logging.WARNING)

    agent_server()

    # Assert logger changed to DEBUG
    assert logging.getLogger().getEffectiveLevel() == logging.DEBUG

    # Assert build prompt was called because identity doesn't have "content"
    mock_build_prompt.assert_called_once()


@pytest.mark.concept("CONCEPT:UK-OS.config.uka-4")
@patch("agent_utilities.initialize_workspace")
@patch("agent_utilities.load_identity")
@patch("agent_utilities.build_system_prompt_from_workspace")
@patch("agent_utilities.create_agent_parser")
@patch("agent_utilities.create_agent_server")
def test_agent_server_main_block(
    mock_create_agent_server,
    mock_create_agent_parser,
    mock_build_prompt,
    mock_load_identity,
    mock_init_workspace,
):
    # Mock parser behavior
    mock_parser = MagicMock()
    mock_args = MagicMock()
    mock_args.debug = False
    mock_parser.parse_args.return_value = mock_args
    mock_create_agent_parser.return_value = mock_parser

    mock_load_identity.return_value = {}

    with patch("sys.argv", ["agent_server.py"]):
        runpy.run_module("uptime_kuma_agent.agent_server", run_name="__main__")

    mock_init_workspace.assert_called_once()
    mock_create_agent_server.assert_called_once()
