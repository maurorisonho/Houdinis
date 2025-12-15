#!/usr/bin/env python3
"""
End-to-End Attack Workflow Tests
================================

Tests complete attack workflows from start to finish, simulating real-world usage.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from exploits.rsa_shor import RsaShorModule
from exploits.grover_bruteforce import GroverBruteForceExploit
from quantum.backend import QuantumBackendManager
# Check if QuantumSimulator exists in quantum.simulator
try:
    from quantum.simulator import QuantumSimulator
except ImportError:
    QuantumSimulator = None


class TestRSAAttackWorkflow:
    """Test RSA factorization attack workflow"""

    def test_shor_factorization_workflow(self):
        """Test Shor's algorithm factorization workflow"""
        print("\n[*] Testing RSA Shor's Algorithm Workflow")
        
        # Initialize attacker
        attacker = RsaShorModule()
        
        # Configure target parameters directly (simulating option setting)
        attacker.target = "localhost" # Required by RsaShorModule check_requirements
        attacker.rsa_modulus = "15"  # Small number for testing
        attacker.rsa_exponent = "7"
        attacker.quantum_backend = "aer_simulator"
        attacker.auto_extract = "false" # Don't try to connect to real network
        
        # Run exploit
        # RsaShorModule.run() calls exploit()
        result = attacker.run()
        
        # Verify success
        if not result['success']:
             print(f"DEBUG: RSA Exploit failed: {result.get('error')}")

        assert result['success'] is True
        assert 'factors' in result
        factors = sorted(result['factors'])
        assert factors == [3, 5]
        
        print(f"[+] RSA Workflow successful: factored 15 into {factors}")

    def test_rsa_key_reconstruction(self):
        """Test reconstruction of private key from factors"""
        attacker = RsaShorModule()
        
        # Setup inputs
        N = 15
        e = 7
        factors = [3, 5]
        
        # Use internal method to analyze impact
        impact = attacker._analyze_security_impact(N, factors, e)
        
        assert impact['impact'] == "COMPLETE COMPROMISE"
        assert 'private_exponent_d' in impact
        
        # Verify private key works: (m^e)^d % N == m
        m = 2
        d = impact['private_exponent_d']
        encrypted = pow(m, e, N)
        decrypted = pow(encrypted, d, N)
        assert decrypted == m


class TestGroverAttackWorkflow:
    """Test Grover's search attack workflow"""

    def test_grover_search_workflow(self):
        """Test Grover's algorithm search workflow"""
        print("\n[*] Testing Grover's Search Workflow")
        
        grover = GroverBruteForceExploit()
        
        # Use a short string "hi" which is feasible for limited brute force
        # md5("hi") = 49f68a5c8493ec2c0bf489821c21fc3b
        target_hash = "49f68a5c8493ec2c0bf489821c21fc3b" 
        
        # run(target_hash, hash_type, max_length)
        result = grover.run(
            target_hash=target_hash,
            hash_type="md5",
            max_length=3, # Enough for 2 chars
            backend_type="simulator"
        )
        
        # Verify result
        # Note: Might fail if qiskit not installed/configured or if stochastic nature fails
        # But for 'hi' it should just work via classical fallback
        
        assert result['success'] is True
        assert result['target_hash'] == target_hash
        if 'result' in result:
             assert result['result'] == "hi"
             
        print(f"[+] Grover Workflow result: {result.get('result')}")


class TestMultiBackendWorkflow:
    """Test backend selection and routing"""

    def test_backend_manager(self):
        """Test QuantumBackendManager features"""
        print("\n[*] Testing Quantum Backend Manager")
        
        manager = QuantumBackendManager()
        
        # List devices (should be consistent)
        devices = manager.list_all_devices()
        assert isinstance(devices, dict)
        
        # Check that we can initialize a backend (at least simulators)
        # Assuming Qiskit is available in environment
        # If not, manager handles it gracefully
        
        status = manager.get_backend_status()
        assert 'active_backends' in status


class TestQuantumSimulatorWorkflow:
    """Test implementation of quantum simulation fallback"""

    def test_classical_shor_simulation(self):
        """Test classical simulation of Shor's algorithm"""
        if QuantumSimulator is None:
            pytest.skip("QuantumSimulator not available")
            
        simulator = QuantumSimulator()
        
        # Simulate factoring 15
        result = simulator.simulate_shors_period_finding(15, 7)
        
        assert result['success'] is True
        assert result['period'] == 4 # 7^4 = 2401 = 1 mod 15
        
        print(f"[+] Simulator Workflow successful: found period {result['period']}")


def run_e2e_tests():
    pytest.main([__file__, "-v", "--tb=short"])

if __name__ == "__main__":
    run_e2e_tests()
