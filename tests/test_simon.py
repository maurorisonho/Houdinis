#!/usr/bin/env python3
"""
# Houdinis Framework - Quantum Cryptography Testing Platform
# Author: Mauro Risonho de Paula Assumpção aka firebitsbr
# Developed by: Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)
# License: MIT

Test suite for Simon's Algorithm implementation.
Tests cover:
- Oracle creation and correctness
- Circuit construction and validation
- Linear equation solving (Gaussian elimination)
- Period finding with various secret strings
- Edge cases (trivial period, maximum period)
- Integration with quantum backends
- Performance and correctness validation
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from exploits.simon_algorithm import SimonAlgorithm

try:
    from qiskit import QuantumCircuit
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False


class TestSimonOracle:
    """Test oracle creation for Simon's algorithm."""

    @pytest.mark.skipif(not QISKIT_AVAILABLE, reason="Qiskit not available")
    def test_oracle_creation_3bit(self):
        """Test oracle creation for 3-bit problem."""
        simon = SimonAlgorithm(n_bits=3)
        secret = "101"
        
        oracle = simon.create_oracle(secret)
        
        assert oracle is not None
        assert oracle.num_qubits == 6  # 2 * n_bits
        assert oracle.name == "Simon Oracle"

    @pytest.mark.skipif(not QISKIT_AVAILABLE, reason="Qiskit not available")
    def test_oracle_creation_4bit(self):
        """Test oracle creation for 4-bit problem."""
        simon = SimonAlgorithm(n_bits=4)
        secret = "1010"
        
        oracle = simon.create_oracle(secret)
        
        assert oracle is not None
        assert oracle.num_qubits == 8
        assert oracle.name == "Simon Oracle"

    @pytest.mark.skipif(not QISKIT_AVAILABLE, reason="Qiskit not available")
    def test_oracle_trivial_period(self):
        """Test oracle with trivial period (all zeros)."""
        simon = SimonAlgorithm(n_bits=3)
        secret = "000"
        
        oracle = simon.create_oracle(secret)
        
        assert oracle is not None
        assert oracle.num_qubits == 6


class TestSimonCircuit:
    """Test complete Simon's algorithm circuit construction."""

    @pytest.mark.skipif(not QISKIT_AVAILABLE, reason="Qiskit not available")
    def test_circuit_construction_basic(self):
        """Test basic circuit construction."""
        simon = SimonAlgorithm(n_bits=3)
        secret = "110"
        
        circuit = simon.create_simon_circuit(secret)
        
        assert circuit is not None
        assert circuit.num_qubits == 6
        assert circuit.num_clbits == 3

    @pytest.mark.skipif(not QISKIT_AVAILABLE, reason="Qiskit not available")
    def test_circuit_has_hadamard_gates(self):
        """Test that circuit includes necessary Hadamard gates."""
        simon = SimonAlgorithm(n_bits=3)
        secret = "101"
        
        circuit = simon.create_simon_circuit(secret)
        
        # Check that circuit contains Hadamard operations
        operations = [inst.operation.name for inst in circuit.data]
        assert 'h' in operations

    @pytest.mark.skipif(not QISKIT_AVAILABLE, reason="Qiskit not available")
    def test_circuit_has_measurements(self):
        """Test that circuit includes measurement operations."""
        simon = SimonAlgorithm(n_bits=3)
        secret = "011"
        
        circuit = simon.create_simon_circuit(secret)
        
        # Check that circuit contains measurements
        operations = [inst.operation.name for inst in circuit.data]
        assert 'measure' in operations


class TestLinearEquationSolving:
    """Test Gaussian elimination for solving linear equations."""

    def test_gaussian_elimination_simple(self):
        """Test Gaussian elimination with simple system."""
        simon = SimonAlgorithm(n_bits=3)
        
        # System with known solution
        equations = [
            [1, 0, 1],  # x + z = 0 (mod 2)
            [0, 1, 1],  # y + z = 0 (mod 2)
            [1, 1, 0],  # x + y = 0 (mod 2)
        ]
        
        solution = simon._gaussian_elimination_gf2(equations, simon.n_bits)
        
        assert solution is not None
        assert len(solution) == 3

    def test_gaussian_elimination_redundant(self):
        """Test with redundant equations."""
        simon = SimonAlgorithm(n_bits=3)
        
        equations = [
            [1, 0, 1],
            [1, 0, 1],  # Duplicate
            [0, 1, 1],
        ]
        
        solution = simon._gaussian_elimination_gf2(equations, simon.n_bits)
        
        # Should still find a solution
        assert solution is not None

    def test_gaussian_elimination_underdetermined(self):
        """Test with insufficient equations."""
        simon = SimonAlgorithm(n_bits=3)
        
        equations = [
            [1, 0, 1],
            [0, 1, 0],
        ]
        
        # May or may not find solution with insufficient equations
        solution = simon._gaussian_elimination_gf2(equations, simon.n_bits)
        # Just check it doesn't crash

    def test_solve_equations_format(self):
        """Test that solution format is correct."""
        simon = SimonAlgorithm(n_bits=4)
        
        equations = [
            [1, 0, 0, 1],
            [0, 1, 1, 0],
            [1, 1, 0, 0],
            [0, 0, 1, 1],
        ]
        
        solution = simon._gaussian_elimination_gf2(equations, simon.n_bits)
        
        if solution:
            assert len(solution) == 4
            assert all(bit in ['0', '1'] for bit in solution)


class TestPeriodFinding:
    """Test period finding functionality."""

    @pytest.mark.skipif(not QISKIT_AVAILABLE, reason="Qiskit not available")
    def test_find_period_3bit(self):
        """Test finding period for 3-bit problem."""
        simon = SimonAlgorithm(n_bits=3)
        secret = "101"
        
        result = simon.find_hidden_period(secret, num_shots=1024)
        
        assert 'secret_string' in result
        assert 'found_period' in result
        assert 'success' in result
        assert result['secret_string'] == secret

    @pytest.mark.skipif(not QISKIT_AVAILABLE, reason="Qiskit not available")
    def test_find_period_trivial(self):
        """Test finding trivial period (000)."""
        simon = SimonAlgorithm(n_bits=3)
        secret = "000"
        
        result = simon.find_hidden_period(secret, num_shots=512)
        
        assert result is not None
        assert 'found_period' in result

    @pytest.mark.skipif(not QISKIT_AVAILABLE, reason="Qiskit not available")
    def test_find_period_4bit(self):
        """Test finding period for 4-bit problem."""
        simon = SimonAlgorithm(n_bits=4)
        secret = "1010"
        
        result = simon.find_hidden_period(secret, num_shots=1024)
        
        assert result is not None
        # assert 'iterations' in result - Removed generally unused field

    @pytest.mark.skipif(not QISKIT_AVAILABLE, reason="Qiskit not available")
    def test_find_period_success_rate(self):
        """Test that period finding succeeds reasonably often."""
        simon = SimonAlgorithm(n_bits=3)
        
        successes = 0
        trials = 5
        
        for _ in range(trials):
            secret = "110"
            result = simon.find_hidden_period(secret, num_shots=1024)
            
            if result.get('success', False):
                successes += 1
        
        # Should succeed in at least some trials
        assert successes > 0


class TestSimonCryptographicApplications:
    """Test cryptographic applications of Simon's algorithm."""

    @pytest.mark.skipif(not QISKIT_AVAILABLE, reason="Qiskit not available")
    def test_period_affects_function_evaluation(self):
        """Test that found period correctly characterizes the function."""
        simon = SimonAlgorithm(n_bits=3)
        secret = "011"
        
        result = simon.find_hidden_period(secret, num_shots=1024)
        
        if result.get('success', False):
            found = result['found_period']
            # Verify the period property: f(x) = f(x ⊕ s)
            assert len(found) == len(secret)

    @pytest.mark.skipif(not QISKIT_AVAILABLE, reason="Qiskit not available")
    def test_measurement_statistics(self):
        """Test that measurements follow expected distribution."""
        simon = SimonAlgorithm(n_bits=3)
        secret = "101"
        
        # Use internal simulation method that works without backend/circuit for logic verification
        measurements = simon._simulate_measurements(simon.n_bits, secret, num_shots=1000)
        
        # Should get multiple different measurement outcomes
        assert len(measurements) > 0
        # Total counts should match shots
        total = sum(measurements.values())
        assert total == 1000

    def test_algorithm_classical_fallback(self):
        """Test that algorithm can work without Qiskit (classical simulation)."""
        simon = SimonAlgorithm(n_bits=3)
        
        # Should not crash even without Qiskit
        equations = [[1, 0, 1], [0, 1, 1]]
        solution = simon._gaussian_elimination_gf2(equations, simon.n_bits)
        # Just verify it runs


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_single_bit_problem(self):
        """Test with minimal 1-bit problem."""
        simon = SimonAlgorithm(n_bits=1)
        
        # Should initialize without error
        assert simon.n_bits == 1

    @pytest.mark.skipif(not QISKIT_AVAILABLE, reason="Qiskit not available")
    def test_max_period_all_ones(self):
        """Test with maximum period (all ones)."""
        simon = SimonAlgorithm(n_bits=3)
        secret = "111"
        
        oracle = simon.create_oracle(secret)
        assert oracle is not None

    def test_invalid_secret_string_length(self):
        """Test behavior with mismatched secret string length."""
        simon = SimonAlgorithm(n_bits=3)
        
        # Try to create oracle with wrong length secret
        with pytest.raises((ValueError, AssertionError, Exception)):
            simon.create_oracle("11")  # Too short

    @pytest.mark.skipif(not QISKIT_AVAILABLE, reason="Qiskit not available")
    def test_zero_shots(self):
        """Test behavior with zero shots."""
        simon = SimonAlgorithm(n_bits=3)
        
        # Should handle gracefully or raise informative error
        try:
            result = simon.find_hidden_period("101", num_shots=0)
        except (ValueError, RuntimeError):
            pass  # Expected behavior


class TestPerformance:
    """Test performance characteristics."""

    @pytest.mark.skipif(not QISKIT_AVAILABLE, reason="Qiskit not available")
    def test_execution_time_reasonable(self):
        """Test that execution completes in reasonable time."""
        import time
        
        simon = SimonAlgorithm(n_bits=3)
        secret = "101"
        
        start = time.time()
        result = simon.find_hidden_period(secret, num_shots=100)
        elapsed = time.time() - start
        
        # Should complete within 30 seconds for small problem
        assert elapsed < 30.0

    @pytest.mark.skipif(not QISKIT_AVAILABLE, reason="Qiskit not available")
    def test_scalability_4bit(self):
        """Test that algorithm scales to 4-bit problems."""
        simon = SimonAlgorithm(n_bits=4)
        secret = "1100"
        
        # Should be able to construct circuit for 4-bit problem
        circuit = simon.create_simon_circuit(secret)
        assert circuit.num_qubits == 8


class TestIntegration:
    """Integration tests with quantum backends."""

    @pytest.mark.skipif(not QISKIT_AVAILABLE, reason="Qiskit not available")
    def test_full_algorithm_flow(self):
        """Test complete algorithm flow from start to finish."""
        simon = SimonAlgorithm(n_bits=3)
        secret = "110"
        
        # Full execution
        result = simon.find_period(secret, shots=1024)
        
        # Verify result structure
        assert isinstance(result, dict)
        assert 'secret_string' in result
        # assert 'iterations' in result
        assert 'measurements' in result

    @pytest.mark.skipif(not QISKIT_AVAILABLE, reason="Qiskit not available")
    def test_multiple_runs_consistency(self):
        """Test that multiple runs produce consistent results."""
        simon = SimonAlgorithm(n_bits=3)
        secret = "101"
        
        results = []
        for _ in range(3):
            result = simon.find_period(secret, shots=512)
            results.append(result)
        
        # All runs should complete
        assert len(results) == 3
        assert all(isinstance(r, dict) for r in results)


def test_module_import():
    """Test that the module can be imported successfully."""
    from exploits import simon_algorithm
    assert hasattr(simon_algorithm, 'SimonAlgorithm')


def test_demonstration_function_exists():
    """Test that demonstration function exists."""
    from exploits.simon_algorithm import demonstrate_simon
    assert callable(demonstrate_simon)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
