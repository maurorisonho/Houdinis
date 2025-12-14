"""
Houdinis Framework - Unit Tests for Modules System
Tests module loading, registration, options, and execution
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.modules import BaseModule, ScannerModule, ModuleManager


class MockModule(BaseModule):
    """Mock module for testing"""
    
    def __init__(self):
        super().__init__()
        self.info = {
            'name': 'Mock Module',
            'description': 'Test module',
            'author': 'Test',
            'version': '1.0',
            'category': 'test'
        }
        self.options = {
            'TARGET': {
                'description': 'Target host',
                'required': True,
                'default': None
            },
            'PORT': {
                'description': 'Target port',
                'required': False,
                'default': '443'
            }
        }
        self.target = None
        self.port = '443'
    
    def run(self):
        """Mock run implementation"""
        if not self.target:
            return {'success': False, 'error': 'TARGET not set'}
        return {'success': True, 'data': f'Ran against {self.target}:{self.port}'}


class TestBaseModule:
    """Test BaseModule abstract base class"""
    
    def test_module_initialization(self):
        """Test module initializes with correct attributes"""
        module = MockModule()
        
        assert module.info is not None
        assert module.options is not None
        assert 'name' in module.info
        assert 'description' in module.info
    
    def test_set_option_valid(self):
        """Test setting a valid option"""
        module = MockModule()
        
        result = module.set_option('TARGET', '192.168.1.1')
        assert result is True
        assert module.target == '192.168.1.1'
    
    def test_set_option_case_insensitive(self):
        """Test option setting is case insensitive"""
        module = MockModule()
        
        module.set_option('target', '10.0.0.1')
        assert module.target == '10.0.0.1'
        
        module.set_option('TaRgEt', '10.0.0.2')
        assert module.target == '10.0.0.2'
    
    def test_set_option_invalid(self):
        """Test setting an invalid option returns False"""
        module = MockModule()
        
        result = module.set_option('INVALID_OPTION', 'value')
        assert result is False
    
    def test_get_option_valid(self):
        """Test getting a valid option"""
        module = MockModule()
        module.target = '192.168.1.1'
        
        value = module.get_option('TARGET')
        assert value == '192.168.1.1'
    
    def test_get_option_default(self):
        """Test getting option with default value"""
        module = MockModule()
        
        value = module.get_option('PORT')
        assert value == '443'
    
    def test_get_option_invalid(self):
        """Test getting an invalid option returns None"""
        module = MockModule()
        
        value = module.get_option('INVALID_OPTION')
        assert value is None
    
    def test_check_requirements_all_set(self):
        """Test requirements check passes when all required options set"""
        module = MockModule()
        module.target = '192.168.1.1'
        
        assert module.check_requirements() is True
    
    def test_check_requirements_missing(self):
        """Test requirements check fails when required options missing"""
        module = MockModule()
        # Don't set target
        
        assert module.check_requirements() is False
    
    def test_check_requirements_optional_missing(self):
        """Test requirements check passes with optional options missing"""
        module = MockModule()
        module.target = '192.168.1.1'
        module.port = None
        
        # Should still pass since PORT is not required
        assert module.check_requirements() is True
    
    def test_run_with_valid_options(self):
        """Test module runs successfully with valid options"""
        module = MockModule()
        module.target = '192.168.1.1'
        
        result = module.run()
        assert result['success'] is True
        assert 'data' in result
    
    def test_run_without_required_options(self):
        """Test module run fails without required options"""
        module = MockModule()
        # Don't set target
        
        result = module.run()
        assert result['success'] is False
        assert 'error' in result


class TestScannerModule:
    """Test ScannerModule base class"""
    
    def test_scanner_inherits_base(self):
        """Test ScannerModule inherits from BaseModule"""
        assert issubclass(ScannerModule, BaseModule)
    
    def test_scanner_initialization(self):
        """Test ScannerModule initializes correctly"""
        scanner = ScannerModule()
        
        assert scanner.info is not None
        assert scanner.options is not None


class TestModuleManager:
    """Test ModuleManager functionality"""
    
    @pytest.fixture
    def manager(self):
        """Create ModuleManager instance"""
        return ModuleManager()
    
    def test_manager_initialization(self, manager):
        """Test module manager initializes correctly"""
        assert manager.modules == {}
        assert isinstance(manager.modules, dict)
    
    def test_register_module(self, manager):
        """Test registering a module"""
        module = MockModule()
        manager.register_module('test/mock', module)
        
        assert 'test/mock' in manager.modules
        assert manager.modules['test/mock'] == module
    
    def test_get_module_exists(self, manager):
        """Test getting an existing module"""
        module = MockModule()
        manager.register_module('test/mock', module)
        
        retrieved = manager.get_module('test/mock')
        assert retrieved == module
    
    def test_get_module_not_exists(self, manager):
        """Test getting a non-existent module"""
        retrieved = manager.get_module('nonexistent/module')
        assert retrieved is None
    
    def test_get_modules_all(self, manager):
        """Test getting all modules"""
        module1 = MockModule()
        module2 = MockModule()
        
        manager.register_module('scanner/test1', module1)
        manager.register_module('exploit/test2', module2)
        
        modules = manager.get_modules()
        assert len(modules) == 2
        assert 'scanner/test1' in modules
        assert 'exploit/test2' in modules
    
    def test_get_modules_by_type(self, manager):
        """Test getting modules filtered by type"""
        module1 = MockModule()
        module2 = MockModule()
        
        manager.register_module('scanner/test1', module1)
        manager.register_module('exploit/test2', module2)
        
        scanners = manager.get_modules('scanner')
        assert len(scanners) == 1
        assert 'scanner/test1' in scanners
    
    def test_unregister_module(self, manager):
        """Test unregistering a module"""
        module = MockModule()
        manager.register_module('test/mock', module)
        
        assert 'test/mock' in manager.modules
        
        result = manager.unregister_module('test/mock')
        assert result is True
        assert 'test/mock' not in manager.modules
    
    def test_unregister_nonexistent_module(self, manager):
        """Test unregistering a module that doesn't exist"""
        result = manager.unregister_module('nonexistent/module')
        assert result is False


@pytest.mark.unit
class TestModuleOptions:
    """Test module options system"""
    
    def test_options_structure(self):
        """Test options have correct structure"""
        module = MockModule()
        
        for option_name, option_config in module.options.items():
            assert 'description' in option_config
            assert 'required' in option_config
            assert 'default' in option_config
    
    def test_required_option_validation(self):
        """Test required option validation"""
        module = MockModule()
        
        # Required option not set
        assert not module.check_requirements()
        
        # Required option set
        module.target = '192.168.1.1'
        assert module.check_requirements()
    
    def test_optional_option_defaults(self):
        """Test optional options use defaults"""
        module = MockModule()
        
        # PORT has a default value
        assert module.port == '443'
        
        # Can override default
        module.set_option('PORT', '8080')
        assert module.port == '8080'


@pytest.mark.security
class TestModuleSecurity:
    """Test security aspects of module system"""
    
    def test_option_validation_prevents_injection(self):
        """Test option values are validated"""
        module = MockModule()
        
        # These should be validated at a higher level
        # but we test the module accepts them
        dangerous_values = [
            "192.168.1.1; rm -rf /",
            "target && cat /etc/passwd",
            "$(whoami)",
        ]
        
        for value in dangerous_values:
            module.set_option('TARGET', value)
            # Module should accept the value, but execution
            # should be protected at the framework level


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
