"""
Houdinis Framework - Edge Case and Boundary Tests
Data de Criação: 15 de dezembro de 2025
Author: Mauro Risonho de Paula Assumpção aka firebitsbr
Desenvolvido: Lógica e Codificação por Humano e AI Assistida (Claude Sonnet 4.5)
License: MIT

Tests edge cases, boundary conditions, and error scenarios.
"""

import pytest
import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quantum.simulator import QuantumSimulator
from security.security_config import SecurityConfig


class TestQuantumSimulatorEdgeCases:
    """Test edge cases in quantum simulator."""
    
    def test_zero_qubits(self):
        """Test simulator with zero qubits."""
        # Should handle or create default
        sim = QuantumSimulator(num_qubits=0)
        assert sim.num_qubits >= 0
    
    def test_single_qubit(self):
        """Test simulator with single qubit."""
        sim = QuantumSimulator(num_qubits=1)
        assert sim.num_qubits == 1
        assert hasattr(sim, 'max_qubits')
    
    def test_large_qubit_count(self):
        """Test simulator with large qubit count."""
        # Should handle reasonable sizes
        sim = QuantumSimulator(num_qubits=10)
        assert sim.num_qubits == 10
        assert hasattr(sim, 'max_qubits')
    
    def test_shors_algorithm_simulation(self):
        """Test Shor's algorithm simulation with edge cases."""
        sim = QuantumSimulator(num_qubits=10)
        
        # Small numbers
        result = sim.simulate_shors_period_finding(N=15, a=7)
        assert isinstance(result, dict)
        assert 'success' in result
        
        # Edge case: coprime check
        result = sim.simulate_shors_period_finding(N=15, a=15)
        assert isinstance(result, dict)
    
    def test_grovers_algorithm_simulation(self):
        """Test Grover's algorithm simulation."""
        sim = QuantumSimulator(num_qubits=5)
        
        # Small database
        result = sim.simulate_grovers_search(database_size=16, target_items=[5])
        assert isinstance(result, dict)
        assert 'success' in result
        
        # Multiple targets
        result = sim.simulate_grovers_search(database_size=16, target_items=[5, 10])
        assert isinstance(result, dict)


class TestSecurityConfigEdgeCases:
    """Test edge cases in security configuration."""
    
    def test_empty_filenames(self):
        """Test validation with empty filenames."""
        config = SecurityConfig()
        
        result = config.validate_filename("")
        assert result is False, "Should reject empty filename"
    
    def test_dangerous_filenames(self):
        """Test various dangerous filename attempts."""
        config = SecurityConfig()
        
        dangerous_names = [
            "../../../etc/passwd",
            "file;rm -rf",
            "file$(whoami)",
        ]
        
        for name in dangerous_names:
            result = config.validate_filename(name)
            # Should reject dangerous patterns
            assert result is False
    
    def test_hostname_validation(self):
        """Test hostname validation with various inputs."""
        config = SecurityConfig()
        
        # Valid hostnames
        assert config.validate_hostname("localhost") is True
        assert config.validate_hostname("127.0.0.1") is True
        assert config.validate_hostname("example.com") is True
        
        # Invalid hostnames
        assert config.validate_hostname("") is False
        assert config.validate_hostname("a" * 300) is False
    
    def test_port_validation(self):
        """Test port number validation."""
        config = SecurityConfig()
        
        # Valid ports
        assert config.validate_port(80) is True
        assert config.validate_port("443") is True
        assert config.validate_port(8080) is True
        
        # Invalid ports
        assert config.validate_port(0) is False
        assert config.validate_port(99999) is False
        assert config.validate_port("invalid") is False
    
    def test_long_input_strings(self):
        """Test with very long input strings."""
        config = SecurityConfig()
        
        long_string = "A" * 10000
        # Should handle or reject gracefully
        result = config.validate_filename(long_string)
        assert result is False  # Too long
    
    def test_special_filename_characters(self):
        """Test filenames with special characters."""
        # Valid safe filenames
        assert SecurityConfig.validate_filename("test.txt") is True
        assert SecurityConfig.validate_filename("file_123.py") is True
        assert SecurityConfig.validate_filename("data-2024.json") is True


class TestNumericalEdgeCases:
    """Test numerical edge cases and boundaries."""
    
    def test_zero_values_in_factorization(self):
        """Test handling of zero and edge values."""
        sim = QuantumSimulator(num_qubits=10)
        
        # Should handle edge cases gracefully
        result = sim.simulate_shors_period_finding(N=15, a=1)
        assert isinstance(result, dict)
    
    def test_small_number_factorization(self):
        """Test with very small numbers."""
        sim = QuantumSimulator(num_qubits=5)
        
        # Small primes
        result = sim.simulate_shors_period_finding(N=15, a=7)
        assert isinstance(result, dict)
        assert 'success' in result
    
    def test_large_number_handling(self):
        """Test with larger numbers."""
        sim = QuantumSimulator(num_qubits=15)
        
        # Larger composite
        result = sim.simulate_shors_period_finding(N=21, a=5)
        assert isinstance(result, dict)
    
    def test_grover_database_sizes(self):
        """Test Grover's algorithm with various database sizes."""
        sim = QuantumSimulator(num_qubits=10)
        
        # Power of 2 sizes
        for size in [4, 8, 16, 32]:
            result = sim.simulate_grovers_search(size, [1])
            assert isinstance(result, dict)
    
    def test_edge_case_parameters(self):
        """Test edge case parameters in simulations."""
        sim = QuantumSimulator(num_qubits=5)
        
        # Edge cases that should be handled
        result = sim.simulate_grovers_search(database_size=1, target_items=[0])
        assert isinstance(result, dict)


class TestConcurrencyEdgeCases:
    """Test edge cases related to concurrency."""
    
    def test_multiple_simulator_instances(self):
        """Test creating multiple simulator instances."""
        simulators = [QuantumSimulator(num_qubits=2) for _ in range(10)]
        
        # Each should be independent
        for i, sim in enumerate(simulators):
            result = sim.simulate_shors_period_finding(N=15, a=7)
            assert isinstance(result, dict)
        
        # All should be valid
        assert len(simulators) == 10
    
    def test_rapid_creation_destruction(self):
        """Test rapid creation and destruction of objects."""
        for _ in range(100):
            sim = QuantumSimulator(num_qubits=2)
            result = sim.simulate_grovers_search(4, [1])
            assert isinstance(result, dict)
            del sim


class TestResourceLimits:
    """Test behavior at resource limits."""
    
    def test_memory_with_many_qubits(self):
        """Test memory handling with many qubits."""
        # Should handle or gracefully fail
        try:
            # 20 qubits at limit
            sim = QuantumSimulator(num_qubits=20)
            assert sim.num_qubits == 20
            assert hasattr(sim, 'max_qubits')
        except MemoryError:
            pytest.skip("Not enough memory for 20 qubits")
    
    def test_large_database_search(self):
        """Test with large database in Grover's search."""
        sim = QuantumSimulator(num_qubits=10)
        
        # Large database
        result = sim.simulate_grovers_search(database_size=1024, target_items=[42])
        assert isinstance(result, dict)
        assert 'success' in result
    
    def test_multiple_targets_search(self):
        """Test searching for multiple targets."""
        sim = QuantumSimulator(num_qubits=6)
        
        # Multiple targets
        result = sim.simulate_grovers_search(
            database_size=32,
            target_items=[5, 10, 15, 20]
        )
        assert isinstance(result, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
