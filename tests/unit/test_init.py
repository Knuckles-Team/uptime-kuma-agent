"""Tests for initialization functions."""

from unittest.mock import MagicMock

import pytest


class TestInitialization:
    @pytest.fixture
    def mock_client(self):
        client = MagicMock()
        return client

    @pytest.mark.concept("CONCEPT:UK-OS.config.uka")
    def test_mcp_instance_creation(self, mock_client):
        from uptime_kuma_agent.mcp_server import get_mcp_instance

        mcp, args, middlewares = get_mcp_instance(
            command_args=["--transport", "stdio", "--auth-type", "none"]
        )
        assert mcp is not None
        assert args.transport == "stdio"
        assert middlewares == list(mcp.middleware)
