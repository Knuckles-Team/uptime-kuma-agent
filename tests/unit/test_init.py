"""Tests for initialization functions."""

from unittest.mock import MagicMock, patch

import pytest


class TestInitialization:
    @pytest.fixture
    def mock_client(self):
        client = MagicMock()
        return client

    @pytest.mark.concept("CONCEPT:UK-OS.config.uka")
    def test_mcp_instance_creation(self, mock_client):
        from uptime_kuma_agent.mcp_server import get_mcp_instance

        with patch("uptime_kuma_agent.mcp_server.get_client", return_value=mock_client):
            with patch("uptime_kuma_agent.mcp_server.create_mcp_server") as mock_create:
                mock_create.return_value = (MagicMock(), MagicMock(), [MagicMock()])
                mcp, args, middlewares = get_mcp_instance()

                assert mcp is not None
                assert args is not None
