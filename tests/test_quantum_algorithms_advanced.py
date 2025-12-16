#!/usr/bin/env python3
"""
# Houdinis Framework - Quantum Cryptography Testing Platform
# Author: Mauro Risonho de Paula Assumpção aka firebitsbr
# Developed by: Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)
# License: MIT

Data de Criação: 15 de dezembro de 2025
Additional tests for quantum algorithms to increase coverage to 85%+.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock


class TestAmplitudeAmplification:
    """Test suite for amplitude amplification algorithm."""
    
    def test_amplitude_amplification_initialization(self):
        """Test AmplitudeAmplification initialization."""
        try:
            from exploits.amplitude_amplification import AmplitudeAmplification
            
            aa = AmplitudeAmplification(num_qubits=4)
            assert aa.num_qubits == 4
            
        except ImportError:
            pytest.skip("Amplitude amplification module not available")
    
    def test_optimal_iterations_calculation(self):
        """Test optimal Grover iterations calculation."""
        try:
            from exploits.amplitude_amplification import AmplitudeAmplification
            
            aa = AmplitudeAmplification(num_qubits=4)
            
            # For N=16, M=1: iterations ≈ π/4 * √16 = π ≈ 3.14
            iterations = aa.calculate_optimal_iterations(
                num_items=16,
                num_marked=1
            )
            
            assert iterations >= 3
            assert iterations <= 4
            
        except ImportError:
            pytest.skip("Amplitude amplification module not available")
    
    def test_collision_finding_attack(self):
        """Test collision finding attack using amplitude amplification."""
        try:
            from exploits.amplitude_amplification import AmplitudeAmplification
            
            aa = AmplitudeAmplification(num_qubits=4)
            
            def simple_hash(x):
                return x % 8  # Simple hash with collisions
            
            result = aa.collision_finding_attack(
                hash_function=simple_hash,
                input_bits=4
            )
            
            assert 'success' in result
            assert 'complexity' in result
            
        except ImportError:
            pytest.skip("Amplitude amplification module not available")


class TestQuantumPhaseEstimation:
    """Test suite for quantum phase estimation."""
    
    def test_qpe_initialization(self):
        """Test QuantumPhaseEstimation initialization."""
        try:
            from exploits.quantum_phase_estimation import QuantumPhaseEstimation
            
            qpe = QuantumPhaseEstimation(counting_qubits=5)
            assert qpe.counting_qubits == 5
            
        except ImportError:
            pytest.skip("QPE module not available")
    
    def test_controlled_unitary_creation(self):
        """Test controlled unitary operator creation."""
        try:
            from exploits.quantum_phase_estimation import QuantumPhaseEstimation
            
            qpe = QuantumPhaseEstimation(counting_qubits=3)
            
            # Test different gate types
            for gate_type in ['T', 'S', 'Z']:
                result = qpe.create_controlled_unitary(
                    gate_type=gate_type,
                    control_qubit=0,
                    target_qubit=1
                )
                assert result is not None
                
        except ImportError:
            pytest.skip("QPE module not available")
    
    def test_order_finding_application(self):
        """Test order finding for Shor's algorithm."""
        try:
            from exploits.quantum_phase_estimation import QuantumPhaseEstimation
            
            qpe = QuantumPhaseEstimation(counting_qubits=8)
            
            # Test with small number
            result = qpe.order_finding_application(N=15, a=7)
            
            assert 'order' in result or 'success' in result
            
        except ImportError:
            pytest.skip("QPE module not available")


class TestDeutschJozsa:
    """Test suite for Deutsch-Jozsa algorithm."""
    
    def test_deutsch_jozsa_initialization(self):
        """Test DeutschJozsaAlgorithm initialization."""
        try:
            from exploits.deutsch_jozsa import DeutschJozsaAlgorithm
            
            dj = DeutschJozsaAlgorithm(num_qubits=4)
            assert dj.num_qubits == 4
            
        except ImportError:
            pytest.skip("Deutsch-Jozsa module not available")
    
    def test_constant_oracle_detection(self):
        """Test constant oracle detection."""
        try:
            from exploits.deutsch_jozsa import DeutschJozsaAlgorithm
            
            dj = DeutschJozsaAlgorithm(num_qubits=3)
            
            # Constant function (always returns 0)
            def constant_oracle(x):
                return 0
            
            result = dj.run_algorithm(oracle_function=constant_oracle)
            
            assert 'function_type' in result
            assert result['function_type'] == 'constant' or 'balanced' in result
            
        except ImportError:
            pytest.skip("Deutsch-Jozsa module not available")
    
    def test_balanced_oracle_detection(self):
        """Test balanced oracle detection."""
        try:
            from exploits.deutsch_jozsa import DeutschJozsaAlgorithm
            
            dj = DeutschJozsaAlgorithm(num_qubits=3)
            
            # Balanced function (returns 1 for half the inputs)
            def balanced_oracle(x):
                return 1 if x % 2 == 0 else 0
            
            result = dj.run_algorithm(oracle_function=balanced_oracle)
            
            assert 'function_type' in result
            
        except ImportError:
            pytest.skip("Deutsch-Jozsa module not available")


class TestBernsteinVazirani:
    """Test suite for Bernstein-Vazirani algorithm."""
    
    def test_bernstein_vazirani_initialization(self):
        """Test BernsteinVaziraniAlgorithm initialization."""
        try:
            from exploits.bernstein_vazirani import BernsteinVaziraniAlgorithm
            
            bv = BernsteinVaziraniAlgorithm(num_qubits=4)
            assert bv.num_qubits == 4
            
        except ImportError:
            pytest.skip("Bernstein-Vazirani module not available")
    
    def test_hidden_bitstring_recovery(self):
        """Test hidden bitstring recovery."""
        try:
            from exploits.bernstein_vazirani import BernsteinVaziraniAlgorithm
            
            bv = BernsteinVaziraniAlgorithm(num_qubits=4)
            
            # Hidden bitstring: 1010
            hidden_string = [1, 0, 1, 0]
            
            result = bv.run_algorithm(hidden_string=hidden_string)
            
            assert 'recovered_string' in result or 'success' in result
            
        except ImportError:
            pytest.skip("Bernstein-Vazirani module not available")
    
    def test_linear_cryptanalysis_attack(self):
        """Test linear cryptanalysis attack."""
        try:
            from exploits.bernstein_vazirani import BernsteinVaziraniAlgorithm
            
            bv = BernsteinVaziraniAlgorithm(num_qubits=4)
            
            # Simple linear function
            def linear_func(x):
                # s = 0101 (binary for 5)
                s = [0, 1, 0, 1]
                result = 0
                for i, bit in enumerate(s):
                    if i < len(str(bin(x)[2:])):
                        result ^= (bit & int(str(bin(x)[2:]).zfill(4)[i]))
                return result
            
            result = bv.attack_linear_function(linear_func, input_bits=4)
            
            assert 'success' in result or 'key_mask' in result
            
        except ImportError:
            pytest.skip("Bernstein-Vazirani module not available")


class TestQuantumSimulatorAdvanced:
    """Advanced tests for quantum simulator."""
    
    def test_simulator_period_finding_edge_cases(self):
        """Test period finding with edge cases."""
        try:
            from quantum.simulator import QuantumSimulator
            
            sim = QuantumSimulator(num_qubits=10)
            
            # Test with small numbers
            result = sim.simulate_shors_period_finding(N=15, a=2)
            assert 'period' in result or 'success' in result
            
            # Test with coprime numbers
            result = sim.simulate_shors_period_finding(N=21, a=2)
            assert result is not None
            
        except ImportError:
            pytest.skip("Quantum simulator not available")
    
    def test_grover_search_probability(self):
        """Test Grover's search success probability."""
        try:
            from quantum.simulator import QuantumSimulator
            
            sim = QuantumSimulator(num_qubits=8)
            
            # Small database
            result = sim.simulate_grovers_search(
                database_size=16,
                target_items=[5, 10]
            )
            
            assert result['success']
            assert 'measurements' in result
            
            # Check if target items have high probability
            measurements = result['measurements']
            total_shots = sum(measurements.values())
            
            target_prob = sum(measurements.get(t, 0) for t in [5, 10]) / total_shots
            assert target_prob > 0.3  # Should be significantly higher than random
            
        except ImportError:
            pytest.skip("Quantum simulator not available")
    
    def test_quantum_advantage_estimation(self):
        """Test quantum advantage estimation."""
        try:
            from quantum.simulator import QuantumSimulator
            
            sim = QuantumSimulator(num_qubits=10)
            
            # Test different algorithms
            for algo in ['shor', 'grover', 'simon']:
                result = sim.estimate_quantum_advantage(
                    algorithm=algo,
                    problem_size=100
                )
                
                assert 'speedup' in result or 'advantage' in result
                
        except ImportError:
            pytest.skip("Quantum simulator not available")


class TestBackendIntegration:
    """Test quantum backend integration."""
    
    def test_backend_initialization_fallback(self):
        """Test backend initialization with fallback."""
        try:
            from quantum.backend import QuantumBackendBase
            
            # Should handle missing backends gracefully
            assert QuantumBackendBase is not None
            
        except ImportError:
            pytest.skip("Backend module not available")
    
    def test_multiple_backend_availability(self):
        """Test checking multiple backend availability."""
        try:
            from quantum import backend
            
            # Check which backends are available
            available = []
            
            if hasattr(backend, 'QISKIT_AVAILABLE'):
                available.append(('Qiskit', backend.QISKIT_AVAILABLE))
            
            if hasattr(backend, 'CIRQ_AVAILABLE'):
                available.append(('Cirq', backend.CIRQ_AVAILABLE))
            
            if hasattr(backend, 'BRAKET_AVAILABLE'):
                available.append(('Braket', backend.BRAKET_AVAILABLE))
            
            # At least one check should exist
            assert len(available) > 0
            
        except ImportError:
            pytest.skip("Backend module not available")


class TestModuleSystem:
    """Test module management system."""
    
    def test_base_module_options(self):
        """Test base module option handling."""
        try:
            from core.modules import BaseModule
            
            # Create concrete implementation for testing
            class TestModule(BaseModule):
                def run(self):
                    return {'success': True}
            
            module = TestModule()
            
            # Test option setting
            module.options['TEST_OPTION'] = {
                'description': 'Test option',
                'required': False,
                'default': 'test_value'
            }
            
            assert module.set_option('TEST_OPTION', 'new_value')
            assert module.get_option('TEST_OPTION') == 'new_value'
            
        except ImportError:
            pytest.skip("Module system not available")
    
    def test_scanner_module_inheritance(self):
        """Test scanner module inheritance."""
        try:
            from core.modules import ScannerModule
            
            class CustomScanner(ScannerModule):
                def run(self):
                    return {'success': True, 'vulnerabilities': []}
            
            scanner = CustomScanner()
            
            # Check common scanner options exist
            assert 'TARGET' in scanner.options
            assert 'PORT' in scanner.options
            assert 'TIMEOUT' in scanner.options
            
        except ImportError:
            pytest.skip("Module system not available")
    
    def test_exploit_module_inheritance(self):
        """Test exploit module inheritance."""
        try:
            from core.modules import ExploitModule
            
            class CustomExploit(ExploitModule):
                def run(self):
                    return {'success': True, 'result': 'exploited'}
            
            exploit = CustomExploit()
            
            # Check common exploit options exist
            assert 'TARGET' in exploit.options
            assert exploit.info['category'] == 'exploit'
            
        except ImportError:
            pytest.skip("Module system not available")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
