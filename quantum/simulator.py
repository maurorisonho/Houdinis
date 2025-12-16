#!/usr/bin/env python3
"""
# Houdinis Framework - Quantum Cryptography Testing Platform
# Author: Mauro Risonho de Paula Assumpção aka firebitsbr
# Developed by: Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)
# License: MIT

Supports: IBM Quantum, NVIDIA cuQuantum, CUDA-Q, Amazon Braket,
         Azure Quantum, Google Cirq, and other quantum platforms.

"""

import math
import random
from typing import Dict, Any, List, Tuple, Optional


class QuantumSimulator:
    """
    Classical quantum circuit simulator for basic quantum algorithms.
    
    This simulator provides a fallback implementation when hardware quantum
    simulators (Qiskit, Cirq, etc.) are not available. It uses classical
    algorithms to approximate quantum algorithm behavior.
    
    Attributes:
        num_qubits (int): Number of qubits to simulate (default 10)
        max_qubits (int): Maximum qubits for classical simulation (20)
    
    Example:
        >>> sim = QuantumSimulator(num_qubits=12)
        >>> result = sim.simulate_shors_period_finding(N=15, a=7)
        >>> print(result['period'])
    """

    def __init__(self, num_qubits: int = 10) -> None:
        self.num_qubits = num_qubits
        self.max_qubits = 20  # Practical limit for classical simulation

    def simulate_shors_period_finding(self, N: int, a: int) -> Dict[str, Any]:
        """
        Simulate the period finding part of Shor's algorithm.
        
        Finds the period r such that a^r ≡ 1 (mod N), which is the quantum
        component of Shor's factorization algorithm.

        Args:
            N (int): Composite number to factor (must be odd, > 2)
            a (int): Random integer coprime to N, 1 < a < N

        Returns:
            Dict[str, Any]: Results containing:
                - success (bool): Whether period was found
                - period (int): The computed period r
                - measurements (Dict[int, int]): Simulated measurement counts
                - method (str): Simulation method used
                - qubits_used (int): Number of qubits required
                - shots (int): Number of simulated measurements
        
        Example:
            >>> sim = QuantumSimulator()
            >>> result = sim.simulate_shors_period_finding(N=15, a=7)
            >>> print(f"Period: {result['period']}")
        """
        print(f"[*] Simulating quantum period finding for a={a}, N={N}")

        # Classical period finding for demonstration
        period = self._find_period_classical(a, N)

        if period:
            # Simulate quantum measurement results
            # In real quantum computer, we'd get probabilistic results
            simulated_measurements = self._simulate_period_measurements(period, N)

            return {
                "success": True,
                "period": period,
                "measurements": simulated_measurements,
                "method": "classical_simulation",
                "qubits_used": math.ceil(math.log2(N)) * 2,
                "shots": 1024,
            }
        else:
            return {
                "success": False,
                "error": "Period not found",
                "method": "classical_simulation",
            }

    def simulate_grovers_search(
        self, database_size: int, target_items: List[int]
    ) -> Dict[str, Any]:
        """
        Simulate Grover's quantum search algorithm for unstructured search.
        
        Provides quadratic speedup over classical search: O(√N) vs O(N).
        Optimal for searching unsorted databases and breaking symmetric crypto.

        Args:
            database_size (int): Total size of the search space (N)
            target_items (List[int]): List of target item indices to find

        Returns:
            Dict[str, Any]: Results containing:
                - success (bool): Whether search succeeded
                - iterations (int): Optimal Grover iterations used
                - qubits_used (int): Number of qubits required
                - measurements (Dict[int, int]): Measurement histogram
                - target_items (List[int]): Target items searched
                - speedup (str): Quantum vs classical speedup
                - method (str): Algorithm name
        
        Raises:
            Returns error dict if database_size exceeds simulation capacity.
        
        Example:
            >>> sim = QuantumSimulator()
            >>> result = sim.simulate_grovers_search(256, [42, 123])
            >>> print(f"Iterations: {result['iterations']}")
        """
        print(f"[*] Simulating Grover's search in database of size {database_size}")

        if database_size > 2**self.max_qubits:
            return {
                "success": False,
                "error": f"Database too large for simulation (max: 2^{self.max_qubits})",
            }

        # Calculate optimal iterations
        optimal_iterations = math.floor(
            math.pi / 4 * math.sqrt(database_size / len(target_items))
        )

        # Simulate quantum search
        qubits_needed = math.ceil(math.log2(database_size))

        # Simulate measurement results with high probability for target items
        results = {}
        for _ in range(1024):  # Simulate 1024 shots
            if random.random() < 0.85:  # 85% chance to find target (ideal case)
                result = random.choice(target_items)
            else:
                result = random.randint(0, database_size - 1)

            results[result] = results.get(result, 0) + 1

        return {
            "success": True,
            "iterations": optimal_iterations,
            "qubits_used": qubits_needed,
            "measurements": results,
            "target_items": target_items,
            "speedup": f"√{database_size} vs {database_size}",
            "method": "grover_simulation",
        }

    def simulate_quantum_key_search(self, key_size: int) -> Dict[str, Any]:
        """
        Simulate quantum exhaustive key search using Grover's algorithm.
        
        Demonstrates the security impact of Grover's algorithm on symmetric
        cryptography. A k-bit key requires only √(2^k) = 2^(k/2) quantum steps,
        effectively halving the security level.

        Args:
            key_size (int): Size of the cryptographic key in bits (e.g., 128, 256)

        Returns:
            Dict[str, Any]: Results containing:
                - success (bool): Always True for simulation
                - key_size (int): Input key size
                - effective_security (int): Quantum-safe security level (key_size/2)
                - search_space (int): Total key space (2^key_size)
                - iterations_needed (int): Grover iterations required
                - speedup (str): Speedup explanation
                - method (str): Algorithm name
        
        Example:
            >>> sim = QuantumSimulator()
            >>> result = sim.simulate_quantum_key_search(128)
            >>> print(f"Effective security: {result['effective_security']} bits")
        """
        search_space = 2**key_size
        effective_bits = key_size // 2  # Grover's quadratic speedup

        print(f"[*] Simulating quantum key search")
        print(f"[*] Key size: {key_size} bits")
        print(f"[*] Search space: 2^{key_size}")
        print(f"[*] Quantum effective security: {effective_bits} bits")

        # Calculate iterations needed
        iterations = math.floor(math.pi / 4 * math.sqrt(search_space))

        return {
            "success": True,
            "key_size": key_size,
            "effective_security": effective_bits,
            "search_space": search_space,
            "iterations_needed": iterations,
            "speedup": f"√(2^{key_size}) = 2^{effective_bits}",
            "method": "grover_key_search",
        }

    def _find_period_classical(self, a: int, N: int) -> Optional[int]:
        """
        Classical brute-force period finding for Shor's algorithm simulation.
        
        Computes the multiplicative order r of a modulo N, where a^r ≡ 1 (mod N).
        This is exponentially slow compared to quantum period finding.

        Args:
            a (int): Base integer, must be coprime to N
            N (int): Modulus, the number to factor

        Returns:
            Optional[int]: The period r, or None if not found within N iterations
        
        Note:
            This classical method is only practical for small N (< 10^6).
            Quantum period finding provides exponential speedup.
        """
        current = 1
        for r in range(1, N):
            current = (current * a) % N
            if current == 1:
                return r
        return None

    def _simulate_period_measurements(self, period: int, N: int) -> Dict[int, int]:
        """
        Simulate quantum measurements for period finding.

        Args:
            period: The actual period
            N: Modulus

        Returns:
            Simulated measurement counts
        """
        measurements = {}

        # Simulate 1024 measurements
        for _ in range(1024):
            # In ideal case, we'd measure multiples of (2^n)/period
            # For simulation, add some noise but bias toward correct values
            if random.random() < 0.7:  # 70% chance of good measurement
                # Simulate good measurement
                n_qubits = math.ceil(math.log2(N)) * 2
                measured_value = random.randint(0, 2**n_qubits - 1)
                # Bias toward values that would give the correct period
                if period > 1:
                    measured_value = (measured_value // period) * (
                        2**n_qubits // period
                    )
            else:
                # Random noise
                n_qubits = math.ceil(math.log2(N)) * 2
                measured_value = random.randint(0, 2**n_qubits - 1)

            measurements[measured_value] = measurements.get(measured_value, 0) + 1

        return measurements

    def estimate_quantum_advantage(
        self, algorithm: str, problem_size: int
    ) -> Dict[str, Any]:
        """
        Estimate quantum advantage for different algorithms.

        Args:
            algorithm: Algorithm name (shor, grover, etc.)
            problem_size: Size of the problem

        Returns:
            Quantum advantage estimation
        """
        if algorithm.lower() == "shor":
            # Shor's algorithm: exponential speedup
            classical_time = 2 ** (problem_size / 2)  # Best known classical
            quantum_time = problem_size**3  # Polynomial quantum

            return {
                "algorithm": "Shor",
                "problem_size": problem_size,
                "classical_complexity": f"O(2^{problem_size/2})",
                "quantum_complexity": f"O({problem_size}³)",
                "speedup": "Exponential",
                "quantum_advantage": (
                    classical_time / quantum_time if quantum_time > 0 else float("inf")
                ),
            }

        elif algorithm.lower() == "grover":
            # Grover's algorithm: quadratic speedup
            search_space = 2**problem_size
            classical_time = search_space / 2  # Average case
            quantum_time = math.sqrt(search_space)

            return {
                "algorithm": "Grover",
                "problem_size": problem_size,
                "classical_complexity": f"O(2^{problem_size})",
                "quantum_complexity": f"O(2^{problem_size/2})",
                "speedup": "Quadratic",
                "quantum_advantage": classical_time / quantum_time,
            }

        else:
            return {
                "algorithm": algorithm,
                "error": "Unknown algorithm for advantage estimation",
            }


class QuantumCircuitBuilder:
    """
    Simple quantum circuit builder for simulation purposes.
    """

    def __init__(self, num_qubits: int):
        self.num_qubits = num_qubits
        self.gates = []
        self.measurements = []

    def h(self, qubit: int):
        """Add Hadamard gate."""
        self.gates.append(("H", qubit))
        return self

    def x(self, qubit: int):
        """Add Pauli-X gate."""
        self.gates.append(("X", qubit))
        return self

    def cx(self, control: int, target: int):
        """Add CNOT gate."""
        self.gates.append(("CNOT", control, target))
        return self

    def measure(self, qubit: int, classical_bit: int):
        """Add measurement."""
        self.measurements.append((qubit, classical_bit))
        return self

    def simulate(self, shots: int = 1024) -> Dict[str, int]:
        """
        Simulate the circuit execution.

        Args:
            shots: Number of simulation runs

        Returns:
            Measurement counts
        """
        # Simple simulation - for demo purposes
        results = {}

        for _ in range(shots):
            # Simulate random measurement outcomes
            # In real implementation, this would track quantum state
            outcome = ""
            for _ in range(len(self.measurements)):
                outcome += str(random.randint(0, 1))

            results[outcome] = results.get(outcome, 0) + 1

        return results


# Global simulator instance
quantum_simulator = QuantumSimulator()


def demo_quantum_simulation():
    """
    Demonstrate quantum simulation capabilities.
    """
    print("=== Houdinis Quantum Simulation Demo ===\n")

    # Demo Shor's algorithm simulation
    print("1. Shor's Algorithm Simulation:")
    result = quantum_simulator.simulate_shors_period_finding(15, 7)
    if result["success"]:
        print(f"   Period found: {result['period']}")
        print(f"   Qubits used: {result['qubits_used']}")

    print()

    # Demo Grover's algorithm simulation
    print("2. Grover's Search Simulation:")
    result = quantum_simulator.simulate_grovers_search(16, [5, 10])
    if result["success"]:
        print(f"   Optimal iterations: {result['iterations']}")
        print(f"   Qubits needed: {result['qubits_used']}")
        print(f"   Speedup: {result['speedup']}")

    print()

    # Demo quantum advantage estimation
    print("3. Quantum Advantage Estimation:")
    advantage = quantum_simulator.estimate_quantum_advantage("shor", 1024)
    print(f"   Algorithm: {advantage['algorithm']}")
    print(f"   Classical: {advantage['classical_complexity']}")
    print(f"   Quantum: {advantage['quantum_complexity']}")
    print(f"   Speedup: {advantage['speedup']}")


if __name__ == "__main__":
    demo_quantum_simulation()
