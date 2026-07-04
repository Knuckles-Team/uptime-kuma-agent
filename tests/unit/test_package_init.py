import importlib
import sys
from unittest.mock import MagicMock, patch
import pytest

import uptime_kuma_agent
from uptime_kuma_agent import _expose_members, _import_module_safely


@pytest.mark.concept("CONCEPT:UK-OS.governance.uka")
def test_expose_members():
    # Test exposing classes/functions from a dummy module
    mock_module = MagicMock()

    # Use actual class and function to satisfy inspect.isclass and inspect.isfunction
    class MyClass:
        pass

    def my_function():
        pass

    mock_module.MyClass = MyClass
    mock_module.my_function = my_function
    mock_module._private_var = "private"

    # Mock inspect.getmembers
    with patch("inspect.getmembers") as mock_getmembers:
        mock_getmembers.return_value = [
            ("MyClass", MyClass),
            ("my_function", my_function),
            ("_private_var", "private"),
        ]

        # Call the internal expose function
        _expose_members(mock_module)

        # Verify they are added to module attributes and __all__
        assert hasattr(uptime_kuma_agent, "MyClass")
        assert hasattr(uptime_kuma_agent, "my_function")
        assert "MyClass" in uptime_kuma_agent.__all__


@pytest.mark.concept("CONCEPT:UK-OS.governance.uka")
def test_import_module_safely_success():
    with patch("importlib.import_module") as mock_import:
        mock_import.return_value = "success"
        res = _import_module_safely("some_module")
        assert res == "success"
        mock_import.assert_called_once_with("some_module")


@pytest.mark.concept("CONCEPT:UK-OS.governance.uka")
def test_import_module_safely_failure():
    with patch("importlib.import_module", side_effect=ImportError("Not found")):
        res = _import_module_safely("non_existent_module")
        assert res is None


@pytest.mark.concept("CONCEPT:UK-OS.governance.uka")
@pytest.mark.parametrize(
    "import_result, mcp_avail, agent_avail",
    [
        (MagicMock(), True, True),
        (None, False, False),
    ],
)
def test_getattr_availability_flags_parametrized(import_result, mcp_avail, agent_avail):
    # Test _MCP_AVAILABLE and _AGENT_AVAILABLE dynamic checks
    with patch("uptime_kuma_agent._import_module_safely", return_value=import_result):
        assert uptime_kuma_agent._MCP_AVAILABLE is mcp_avail
        assert uptime_kuma_agent._AGENT_AVAILABLE is agent_avail


@pytest.mark.concept("CONCEPT:UK-OS.governance.uka")
def test_getattr_availability_flags_fallback():
    # Test the fallback lines (52 and 57) when keys are not found in OPTIONAL_MODULES
    with patch("uptime_kuma_agent.OPTIONAL_MODULES", {}):
        assert not uptime_kuma_agent._MCP_AVAILABLE
        assert not uptime_kuma_agent._AGENT_AVAILABLE


@pytest.mark.concept("CONCEPT:UK-OS.governance.uka")
def test_getattr_optional_modules_success():
    # Mock dynamic import of an optional module
    mock_mod = MagicMock()
    mock_mod.dummy_attribute = "found_it"

    with patch("uptime_kuma_agent._import_module_safely") as mock_safe_import:
        mock_safe_import.return_value = mock_mod

        # Clear cache first to force reload
        uptime_kuma_agent._loaded_optional_modules.clear()

        val = uptime_kuma_agent.dummy_attribute
        assert val == "found_it"


@pytest.mark.concept("CONCEPT:UK-OS.governance.uka")
def test_getattr_attribute_error():
    # Attribute doesn't exist on any modules
    with patch("uptime_kuma_agent._import_module_safely", return_value=None):
        with pytest.raises(AttributeError):
            _ = uptime_kuma_agent.non_existent_attribute_name


@pytest.mark.concept("CONCEPT:UK-OS.governance.uka")
def test_dir():
    items = dir(uptime_kuma_agent)
    assert len(items) > 0
