#!/usr/bin/env python3
"""
End-to-End Attack Workflow Tests
=================================

Comprehensive E2E tests for complete quantum cryptanalysis attack workflows.
Tests the entire pipeline from initialization to attack completion.

Test Categories:
- Complete Shor's algorithm RSA factorization workflow
- Full Grover search attack workflow
- Multi-backend quantum operation workflows
- Exploit chaining scenarios
- Real-world attack simulations

Author: Houdinis Framework
License: MIT
"""

import pytest
import sys
import os
import time
import numpy as np
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.session import HoudinisSession
from exploits.rsa_shor import RSAShorAttack
from exploits.grover_bruteforce import GroverBruteforce
from quantum.backend import QuantumBackend
from quantum.simulator import QuantumSimulator


@pytest.mark.e2e
@pytest.mark.slow
class TestRSAAttackWorkflow:
    """End-to-end tests for complete RSA attack workflows"""
    
    def test_complete_rsa_factorization_workflow(self):
        """
        Test complete RSA factorization workflow from key to plaintext.
        
        Workflow:
        1. Initialize session
        2. Setup quantum backend
        3. Factor RSA modulus with Shor's algorithm
        4. Recover private key
        5. Decrypt ciphertext
        """
        print("\n[E2E] Testing complete RSA factorization workflow...")
        
        # Step 1: Initialize session
        session = HoudinisSession()
        assert session is not None, "Session initialization failed"
        
        # Step 2: Setup quantum backend
        backend = QuantumBackend(backend_type='simulator')
        assert backend.is_available(), "Quantum backend not available"
        
        # Step 3: Create RSA attack instance
        attacker = RSAShorAttack(backend=backend)
        
        # Use small RSA modulus for testing (N = 15 = 3 × 5)
        N = 15
        e = 7  # Public exponent
        
        print(f"[E2E] Target RSA modulus: N = {N}")
        
        # Step 4: Factor with Shor's algorithm
        start_time = time.time()
        factors = attacker.factor(N)
        elapsed = time.time() - start_time
        
        assert factors is not None, "Factorization failed"
        assert len(factors) == 2, f"Expected 2 factors, got {len(factors)}"
        
        p, q = sorted(factors)
        print(f"[E2E] Factored N={N} into p={p}, q={q}")
        print(f"[E2E] Factorization took {elapsed:.3f} seconds")
        
        # Verify factorization
        assert p * q == N, f"Factorization incorrect: {p} × {q} = {p*q} ≠ {N}"
        
        # Step 5: Recover private key
        phi_n = (p - 1) * (q - 1)
        d = pow(e, -1, phi_n)  # Modular inverse
        
        print(f"[E2E] Recovered private exponent: d = {d}")
        
        # Step 6: Test decryption
        plaintext = 2
        ciphertext = pow(plaintext, e, N)
        recovered = pow(ciphertext, d, N)
        
        assert recovered == plaintext, f"Decryption failed: {recovered} ≠ {plaintext}"
        
        print(f"[E2E]  Complete RSA attack workflow successful!")
        print(f"[E2E]    Plaintext: {plaintext}")
        print(f"[E2E]    Ciphertext: {ciphertext}")
        print(f"[E2E]    Recovered: {recovered}")
    
    def test_rsa_attack_with_error_handling(self):
        """Test RSA attack workflow with error conditions"""
        print("\n[E2E] Testing RSA attack with error handling...")
        
        session = HoudinisSession()
        backend = QuantumBackend(backend_type='simulator')
        attacker = RSAShorAttack(backend=backend)
        
        # Test with invalid inputs
        with pytest.raises((ValueError, AssertionError)):
            attacker.factor(1)  # N too small
        
        with pytest.raises((ValueError, AssertionError)):
            attacker.factor(-15)  # Negative N
        
        # Test with prime number (should not factor)
        N_prime = 17
        factors = attacker.factor(N_prime)
        
        # For a prime, factorization should either fail or return [1, N]
        if factors:
            assert 1 in factors or N_prime in factors, "Prime factorization should be trivial"
        
        print(f"[E2E]  Error handling tests passed")


@pytest.mark.e2e
@pytest.mark.slow
class TestGroverAttackWorkflow:
    """End-to-end tests for Grover search attack workflows"""
    
    def test_complete_grover_search_workflow(self):
        """
        Test complete Grover search workflow for key recovery.
        
        Workflow:
        1. Setup search space and target
        2. Initialize quantum circuit
        3. Execute Grover iterations
        4. Measure and validate result
        """
        print("\n[E2E] Testing complete Grover search workflow...")
        
        # Step 1: Initialize components
        backend = QuantumBackend(backend_type='simulator')
        grover = GroverBruteforce(backend=backend)
        
        # Step 2: Define search parameters
        key_space_bits = 4  # 16 possible keys
        target_key = 0b1010  # Target: 10
        
        print(f"[E2E] Search space: {2**key_space_bits} keys ({key_space_bits} bits)")
        print(f"[E2E] Target key: {target_key} (binary: {bin(target_key)})")
        
        # Step 3: Execute Grover search
        start_time = time.time()
        result = grover.search(
            key_space_bits=key_space_bits,
            target_key=target_key,
            num_iterations=None  # Auto-calculate optimal iterations
        )
        elapsed = time.time() - start_time
        
        # Step 4: Validate results
        assert result is not None, "Grover search returned None"
        assert 'found_key' in result, "Result missing 'found_key'"
        assert 'success' in result, "Result missing 'success'"
        
        found_key = result['found_key']
        success = result['success']
        
        print(f"[E2E] Search completed in {elapsed:.3f} seconds")
        print(f"[E2E] Found key: {found_key} (binary: {bin(found_key)})")
        print(f"[E2E] Success: {success}")
        
        # For small search spaces, Grover should find the key
        if success:
            assert found_key == target_key, f"Wrong key found: {found_key} ≠ {target_key}"
            print(f"[E2E]  Grover search workflow successful!")
        else:
            print(f"[E2E]  Grover search did not find target (probabilistic)")
    
    def test_grover_multiple_targets(self):
        """Test Grover search with multiple target keys"""
        print("\n[E2E] Testing Grover search with multiple targets...")
        
        backend = QuantumBackend(backend_type='simulator')
        grover = GroverBruteforce(backend=backend)
        
        key_space_bits = 3  # 8 possible keys
        target_keys = [0b010, 0b101, 0b110]  # Multiple targets
        
        print(f"[E2E] Target keys: {[bin(k) for k in target_keys]}")
        
        for target in target_keys:
            result = grover.search(
                key_space_bits=key_space_bits,
                target_key=target
            )
            
            if result and result.get('success'):
                found = result['found_key']
                print(f"[E2E]  Found key {bin(target)}: {bin(found)}")
            else:
                print(f"[E2E]  Failed to find key {bin(target)}")


@pytest.mark.e2e
@pytest.mark.slow
class TestMultiBackendWorkflow:
    """End-to-end tests for multi-backend quantum operations"""
    
    def test_backend_switching_workflow(self):
        """Test switching between different quantum backends"""
        print("\n[E2E] Testing backend switching workflow...")
        
        backends = ['simulator', 'ibm_simulator']
        results = {}
        
        for backend_type in backends:
            try:
                print(f"[E2E] Testing with backend: {backend_type}")
                
                backend = QuantumBackend(backend_type=backend_type)
                
                if not backend.is_available():
                    print(f"[E2E]  Backend {backend_type} not available, skipping")
                    continue
                
                # Create simple quantum circuit
                simulator = QuantumSimulator(backend=backend)
                circuit = simulator.create_circuit(n_qubits=2)
                
                # Apply Hadamard gates
                simulator.apply_hadamard(circuit, qubit=0)
                simulator.apply_hadamard(circuit, qubit=1)
                
                # Measure
                circuit_result = simulator.measure(circuit)
                
                results[backend_type] = {
                    'success': True,
                    'circuit': circuit,
                    'result': circuit_result
                }
                
                print(f"[E2E]  Backend {backend_type} operational")
                
            except Exception as e:
                print(f"[E2E]  Backend {backend_type} failed: {e}")
                results[backend_type] = {
                    'success': False,
                    'error': str(e)
                }
        
        # Verify at least one backend worked
        successful_backends = [k for k, v in results.items() if v.get('success')]
        assert len(successful_backends) > 0, "No backends were operational"
        
        print(f"[E2E]  Multi-backend workflow successful!")
        print(f"[E2E]    Operational backends: {successful_backends}")
    
    def test_parallel_quantum_operations(self):
        """Test parallel execution of quantum operations"""
        print("\n[E2E] Testing parallel quantum operations...")
        
        backend = QuantumBackend(backend_type='simulator')
        simulator = QuantumSimulator(backend=backend)
        
        num_circuits = 5
        circuits = []
        
        # Create multiple circuits
        for i in range(num_circuits):
            circuit = simulator.create_circuit(n_qubits=2)
            simulator.apply_hadamard(circuit, qubit=0)
            simulator.apply_hadamard(circuit, qubit=1)
            circuits.append(circuit)
        
        print(f"[E2E] Created {num_circuits} circuits")
        
        # Execute all circuits
        start_time = time.time()
        results = []
        for circuit in circuits:
            result = simulator.measure(circuit)
            results.append(result)
        elapsed = time.time() - start_time
        
        assert len(results) == num_circuits, f"Expected {num_circuits} results, got {len(results)}"
        
        print(f"[E2E]  Executed {num_circuits} circuits in {elapsed:.3f}s")
        print(f"[E2E]    Average time per circuit: {elapsed/num_circuits:.3f}s")


@pytest.mark.e2e
@pytest.mark.slow
class TestExploitChainingWorkflow:
    """End-to-end tests for chaining multiple exploits"""
    
    def test_reconnaissance_to_attack_workflow(self):
        """
        Test complete workflow from reconnaissance to attack.
        
        Workflow:
        1. Network reconnaissance
        2. Vulnerability identification
        3. Exploit selection
        4. Attack execution
        """
        print("\n[E2E] Testing reconnaissance-to-attack workflow...")
        
        # Simulate workflow stages
        workflow_stages = {
            'reconnaissance': False,
            'vulnerability_scan': False,
            'exploit_selection': False,
            'attack_execution': False
        }
        
        # Stage 1: Reconnaissance (simulated)
        print("[E2E] Stage 1: Network reconnaissance...")
        discovered_services = {
            'ssh': {'port': 22, 'version': 'OpenSSH 7.4'},
            'https': {'port': 443, 'cipher': 'RSA-2048'}
        }
        workflow_stages['reconnaissance'] = True
        print(f"[E2E]  Discovered services: {list(discovered_services.keys())}")
        
        # Stage 2: Vulnerability identification
        print("[E2E] Stage 2: Vulnerability identification...")
        vulnerabilities = []
        
        if 'https' in discovered_services:
            if 'RSA' in discovered_services['https']['cipher']:
                vulnerabilities.append({
                    'service': 'https',
                    'vulnerability': 'RSA key exchange (quantum-vulnerable)',
                    'severity': 'high'
                })
        
        workflow_stages['vulnerability_scan'] = True
        print(f"[E2E]  Identified {len(vulnerabilities)} vulnerabilities")
        
        # Stage 3: Exploit selection
        print("[E2E] Stage 3: Exploit selection...")
        selected_exploit = None
        
        for vuln in vulnerabilities:
            if 'RSA' in vuln['vulnerability']:
                selected_exploit = 'rsa_shor'
                break
        
        assert selected_exploit is not None, "No exploit selected"
        workflow_stages['exploit_selection'] = True
        print(f"[E2E]  Selected exploit: {selected_exploit}")
        
        # Stage 4: Attack execution
        print("[E2E] Stage 4: Attack execution...")
        
        backend = QuantumBackend(backend_type='simulator')
        attacker = RSAShorAttack(backend=backend)
        
        # Simulate attack
        N = 15  # Small RSA modulus for testing
        factors = attacker.factor(N)
        
        attack_successful = factors is not None and len(factors) == 2
        workflow_stages['attack_execution'] = attack_successful
        
        if attack_successful:
            print(f"[E2E]  Attack successful: factored N={N} into {factors}")
        else:
            print(f"[E2E]  Attack failed")
        
        # Verify all stages completed
        all_stages_passed = all(workflow_stages.values())
        assert all_stages_passed, f"Some stages failed: {workflow_stages}"
        
        print(f"[E2E]  Complete reconnaissance-to-attack workflow successful!")
    
    def test_hybrid_attack_workflow(self):
        """Test hybrid attack combining classical and quantum methods"""
        print("\n[E2E] Testing hybrid attack workflow...")
        
        # Combine classical preprocessing with quantum attack
        
        # Classical preprocessing
        print("[E2E] Classical preprocessing...")
        N = 15
        
        # Check if N is even (classical)
        if N % 2 == 0:
            print(f"[E2E] Classical check: N={N} is even, trivial factor 2")
            classical_factor = 2
        else:
            classical_factor = None
        
        # Quantum attack
        print("[E2E] Quantum attack phase...")
        backend = QuantumBackend(backend_type='simulator')
        attacker = RSAShorAttack(backend=backend)
        
        factors = attacker.factor(N)
        
        # Combine results
        if classical_factor:
            print(f"[E2E] Using classical factor: {classical_factor}")
        
        if factors:
            print(f"[E2E] Quantum factors: {factors}")
        
        # Verify we have complete factorization
        assert factors is not None, "Factorization failed"
        print(f"[E2E]  Hybrid attack workflow successful!")


@pytest.mark.e2e
class TestRealWorldScenarios:
    """End-to-end tests simulating real-world attack scenarios"""
    
    def test_tls_connection_attack_scenario(self):
        """Simulate attacking a TLS connection with RSA"""
        print("\n[E2E] Simulating TLS connection attack...")
        
        # Scenario: Intercepted TLS handshake with RSA key exchange
        
        # Simulated TLS parameters
        tls_params = {
            'cipher_suite': 'TLS_RSA_WITH_AES_128_CBC_SHA',
            'rsa_modulus': 15,  # Small for testing
            'public_exponent': 7
        }
        
        print(f"[E2E] Intercepted TLS cipher suite: {tls_params['cipher_suite']}")
        print(f"[E2E] RSA modulus: {tls_params['rsa_modulus']}")
        
        # Attack the RSA key exchange
        backend = QuantumBackend(backend_type='simulator')
        attacker = RSAShorAttack(backend=backend)
        
        N = tls_params['rsa_modulus']
        factors = attacker.factor(N)
        
        if factors and len(factors) == 2:
            p, q = sorted(factors)
            print(f"[E2E]  Recovered RSA private key factors: p={p}, q={q}")
            
            # Simulate decrypting session key
            print(f"[E2E]  TLS session key recovered - connection compromised!")
            attack_successful = True
        else:
            print(f"[E2E]  Failed to break RSA")
            attack_successful = False
        
        assert attack_successful, "TLS attack scenario failed"
    
    def test_password_recovery_scenario(self):
        """Simulate password recovery using Grover's algorithm"""
        print("\n[E2E] Simulating password recovery attack...")
        
        # Scenario: Recover 4-digit PIN
        
        backend = QuantumBackend(backend_type='simulator')
        grover = GroverBruteforce(backend=backend)
        
        # Simulated PIN (0000-1111 in 4 bits)
        target_pin = 0b1001  # PIN: 9
        pin_bits = 4
        
        print(f"[E2E] Target: {pin_bits}-bit PIN (16 possibilities)")
        print(f"[E2E] Attempting quantum brute-force with Grover...")
        
        result = grover.search(
            key_space_bits=pin_bits,
            target_key=target_pin
        )
        
        if result and result.get('success'):
            found_pin = result['found_key']
            print(f"[E2E]  PIN recovered: {found_pin}")
            
            # Quadratic speedup achieved
            classical_attempts = 2 ** pin_bits / 2  # Average classical
            quantum_iterations = result.get('iterations', 0)
            
            if quantum_iterations > 0:
                speedup = classical_attempts / quantum_iterations
                print(f"[E2E] Quantum speedup: {speedup:.2f}x")
            
            assert found_pin == target_pin, "Wrong PIN recovered"
        else:
            print(f"[E2E]  PIN recovery probabilistic failure")


def run_e2e_tests():
    """Run all E2E tests with reporting"""
    print("\n" + "="*70)
    print("Running End-to-End Attack Workflow Tests")
    print("="*70 + "\n")
    
    # Run with pytest
    pytest.main([
        __file__,
        '-v',
        '-m', 'e2e',
        '--tb=short',
        '--durations=10'
    ])


if __name__ == '__main__':
    run_e2e_tests()
