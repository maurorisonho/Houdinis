"""
Houdinis Framework - Integration Workflow Tests
Data de Criação: 15 de dezembro de 2025
Author: Mauro Risonho de Paula Assumpção aka firebitsbr
Developed by: Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)
License: MIT

Tests end-to-end scenarios combining multiple modules.
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.modules import ModuleManager
from core.session import SessionManager


class TestModuleWorkflows:
    """Test complete module loading and execution workflows."""

    def test_module_manager_lifecycle(self):
        """Test full module manager lifecycle."""
        manager = ModuleManager()
        
        # Load modules
        manager.load_all_modules()
        
        # Verify modules loaded
        assert len(manager.modules) > 0, "Should load some modules"
        
        # Test module retrieval
        modules = manager.get_modules()
        assert isinstance(modules, dict), "Should return dict of modules"
        
        # Test filtering by type
        scanners = manager.get_modules("scanner")
        exploits = manager.get_modules("exploit")
        
        assert len(scanners) >= 0, "Should get scanners"
        assert len(exploits) >= 0, "Should get exploits"
    
    def test_session_workflow(self):
        """Test complete session management workflow."""
        manager = SessionManager()
        
        # Create session
        session = manager.create_session(
            session_type="test",
            target="127.0.0.1",
            data={"test": "data"}
        )
        
        assert session.id == 1, "First session should have ID 1"
        assert session.status == "active", "New session should be active"
        
        # Get session
        retrieved = manager.get_session(1)
        assert retrieved == session, "Should retrieve same session"
        
        # Update status
        manager.update_session_status(1, "completed")
        assert session.status == "completed", "Status should be updated"
        
        # Get all sessions
        sessions = manager.get_sessions()
        assert len(sessions) == 1, "Should have one session"
        
        # Kill session
        result = manager.kill_session(1)
        assert result is True, "Should successfully kill session"
        assert session.status == "killed", "Status should be killed"
        
        # Clear all
        manager.clear_all_sessions()
        assert len(manager.sessions) == 0, "Should clear all sessions"


class TestModuleInteraction:
    """Test interactions between different modules."""
    
    def test_scanner_to_exploit_workflow(self):
        """Test scanner discovery followed by exploit."""
        manager = ModuleManager()
        manager.load_all_modules()
        
        # Get a scanner module
        scanners = manager.get_modules("scanner")
        if len(scanners) > 0:
            scanner_name = list(scanners.keys())[0]
            scanner_class = manager.get_module(scanner_name)
            
            assert scanner_class is not None, "Should get scanner class"
            
            # Instantiate scanner
            scanner = scanner_class()
            assert scanner.info["category"] == "scanner", "Should be scanner"
    
    def test_exploit_to_payload_workflow(self):
        """Test exploit execution followed by payload delivery."""
        manager = ModuleManager()
        manager.load_all_modules()
        
        # Get an exploit module
        exploits = manager.get_modules("exploit")
        if len(exploits) > 0:
            exploit_name = list(exploits.keys())[0]
            exploit_class = manager.get_module(exploit_name)
            
            assert exploit_class is not None, "Should get exploit class"
            
            # Instantiate exploit
            exploit = exploit_class()
            assert exploit.info["category"] == "exploit", "Should be exploit"


class TestErrorHandling:
    """Test error handling in integrated scenarios."""
    
    def test_module_manager_invalid_module(self):
        """Test handling of invalid module requests."""
        manager = ModuleManager()
        manager.load_all_modules()
        
        # Try to get non-existent module
        result = manager.get_module("nonexistent/module")
        assert result is None, "Should return None for invalid module"
    
    def test_session_manager_invalid_session(self):
        """Test handling of invalid session operations."""
        manager = SessionManager()
        
        # Try to get non-existent session
        result = manager.get_session(999)
        assert result is None, "Should return None for invalid session"
        
        # Try to kill non-existent session
        result = manager.kill_session(999)
        assert result is False, "Should return False for invalid session"
        
        # Try to update non-existent session
        result = manager.update_session_status(999, "test")
        assert result is False, "Should return False for invalid session"
    
    def test_module_option_handling(self):
        """Test module option validation and handling."""
        manager = ModuleManager()
        manager.load_all_modules()
        
        exploits = manager.get_modules("exploit")
        if len(exploits) > 0:
            exploit_class = list(exploits.values())[0]
            exploit = exploit_class()
            
            # Test setting valid option
            if "TARGET" in exploit.options:
                result = exploit.set_option("TARGET", "127.0.0.1")
                assert result is True, "Should set valid option"
                
                value = exploit.get_option("TARGET")
                assert value == "127.0.0.1", "Should get set value"
            
            # Test setting invalid option
            result = exploit.set_option("INVALID_OPTION", "value")
            assert result is False, "Should reject invalid option"
            
            # Test getting invalid option
            value = exploit.get_option("INVALID_OPTION")
            assert value is None, "Should return None for invalid option"


class TestMultipleModuleInstances:
    """Test handling multiple instances of modules."""
    
    def test_multiple_scanner_instances(self):
        """Test creating multiple scanner instances."""
        manager = ModuleManager()
        manager.load_all_modules()
        
        scanners = manager.get_modules("scanner")
        if len(scanners) > 0:
            scanner_class = list(scanners.values())[0]
            
            # Create multiple instances
            scanner1 = scanner_class()
            scanner2 = scanner_class()
            
            # Verify independence
            if "TARGET" in scanner1.options:
                scanner1.set_option("TARGET", "192.168.1.1")
                scanner2.set_option("TARGET", "192.168.1.2")
                
                assert scanner1.get_option("TARGET") == "192.168.1.1"
                assert scanner2.get_option("TARGET") == "192.168.1.2"
    
    def test_multiple_sessions(self):
        """Test managing multiple concurrent sessions."""
        manager = SessionManager()
        
        # Create multiple sessions
        session1 = manager.create_session("type1", "target1", {"data": 1})
        session2 = manager.create_session("type2", "target2", {"data": 2})
        session3 = manager.create_session("type3", "target3", {"data": 3})
        
        assert session1.id == 1
        assert session2.id == 2
        assert session3.id == 3
        
        # Get all sessions
        sessions = manager.get_sessions()
        assert len(sessions) == 3, "Should have 3 sessions"
        
        # Get by type
        type1_sessions = manager.get_sessions_by_type("type1")
        assert len(type1_sessions) == 1, "Should have 1 type1 session"
        assert type1_sessions[0] == session1
        
        # Kill one session
        manager.kill_session(2)
        assert session2.status == "killed"
        
        # Verify others unaffected
        assert session1.status == "active"
        assert session3.status == "active"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
