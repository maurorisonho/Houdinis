#!/usr/bin/env python3
"""
Continuous Benchmarking System
===============================

Automated performance benchmarking and regression detection for Houdinis.
Tracks performance metrics across all attack frameworks and quantum operations.

Features:
- Quantum operation benchmarks
- Attack framework performance tracking
- Performance regression detection
- Automated reporting and visualization
- Historical performance database

Author: Houdinis Framework
Desenvolvido: Lógica e Codificação por Humano e AI Assistida (Claude Sonnet 4.5)
License: MIT
"""

import pytest
import time
import json
import statistics
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from exploits.rsa_shor import RSAShorAttack
from exploits.grover_bruteforce import GroverBruteforce
from exploits.kyber_attack import KyberAttack
from exploits.dilithium_attack import DilithiumAttack
from quantum.backend import QuantumBackend


@dataclass
class BenchmarkResult:
    """Benchmark result data structure"""

    name: str
    category: str
    execution_time: float
    iterations: int
    avg_time_per_iteration: float
    std_dev: float
    min_time: float
    max_time: float
    timestamp: str
    metadata: Dict[str, Any]


class BenchmarkSuite:
    """Comprehensive benchmarking system for Houdinis"""

    def __init__(self, results_dir: Optional[str] = None):
        """
        Initialize benchmarking suite.

        Args:
            results_dir: Directory to store benchmark results
        """
        if results_dir is None:
            results_dir = Path(__file__).parent / "results"

        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)

        self.results: List[BenchmarkResult] = []
        self.baseline: Optional[Dict[str, float]] = None

    def run_benchmark(self, func, iterations: int = 10, **kwargs) -> BenchmarkResult:
        """
        Run a benchmark function multiple times and collect statistics.

        Args:
            func: Function to benchmark
            iterations: Number of iterations
            **kwargs: Arguments to pass to function

        Returns:
            BenchmarkResult with statistics
        """
        times = []

        for i in range(iterations):
            start_time = time.perf_counter()
            try:
                func(**kwargs)
            except Exception as e:
                print(f"Warning: Benchmark iteration {i} failed: {e}")
                continue
            elapsed = time.perf_counter() - start_time
            times.append(elapsed)

        if not times:
            raise ValueError(f"All benchmark iterations failed for {func.__name__}")

        # Calculate statistics
        avg_time = statistics.mean(times)
        std_dev = statistics.stdev(times) if len(times) > 1 else 0.0
        min_time = min(times)
        max_time = max(times)

        result = BenchmarkResult(
            name=func.__name__,
            category="unknown",
            execution_time=sum(times),
            iterations=len(times),
            avg_time_per_iteration=avg_time,
            std_dev=std_dev,
            min_time=min_time,
            max_time=max_time,
            timestamp=datetime.now().isoformat(),
            metadata=kwargs,
        )

        self.results.append(result)
        return result

    def benchmark_quantum_operations(self):
        """Benchmark basic quantum operations"""
        print("\n[BENCHMARK] Quantum Operations...")

        backend = QuantumBackend(backend_type="simulator")

        from quantum.simulator import QuantumSimulator

        simulator = QuantumSimulator(backend=backend)

        # Benchmark: Circuit creation
        def create_circuit():
            return simulator.create_circuit(n_qubits=4)

        result = self.run_benchmark(create_circuit, iterations=100)
        result.category = "quantum_ops"
        print(
            f"[BENCHMARK]   Circuit creation: {result.avg_time_per_iteration*1000:.2f}ms"
        )

        # Benchmark: Hadamard gates
        def apply_hadamards():
            circuit = simulator.create_circuit(n_qubits=4)
            for i in range(4):
                simulator.apply_hadamard(circuit, qubit=i)
            return circuit

        result = self.run_benchmark(apply_hadamards, iterations=50)
        result.category = "quantum_ops"
        print(
            f"[BENCHMARK]   Hadamard gates (4): {result.avg_time_per_iteration*1000:.2f}ms"
        )

        # Benchmark: Circuit measurement
        def measure_circuit():
            circuit = simulator.create_circuit(n_qubits=4)
            simulator.apply_hadamard(circuit, qubit=0)
            return simulator.measure(circuit)

        result = self.run_benchmark(measure_circuit, iterations=50)
        result.category = "quantum_ops"
        print(
            f"[BENCHMARK]   Circuit measurement: {result.avg_time_per_iteration*1000:.2f}ms"
        )

    def benchmark_shor_algorithm(self):
        """Benchmark Shor's algorithm performance"""
        print("\n[BENCHMARK] Shor's Algorithm...")

        backend = QuantumBackend(backend_type="simulator")
        attacker = RSAShorAttack(backend=backend)

        # Benchmark different modulus sizes
        test_cases = [
            (15, "N=15 (3×5)"),
            (21, "N=21 (3×7)"),
        ]

        for N, description in test_cases:

            def run_shor():
                return attacker.factor(N)

            result = self.run_benchmark(run_shor, iterations=5, N=N)
            result.category = "shor_algorithm"
            print(
                f"[BENCHMARK]   {description}: {result.avg_time_per_iteration*1000:.2f}ms"
            )

    def benchmark_grover_search(self):
        """Benchmark Grover's algorithm performance"""
        print("\n[BENCHMARK] Grover's Algorithm...")

        backend = QuantumBackend(backend_type="simulator")
        grover = GroverBruteforce(backend=backend)

        # Benchmark different search space sizes
        test_cases = [
            (3, 0b101, "3-bit space"),
            (4, 0b1010, "4-bit space"),
        ]

        for bits, target, description in test_cases:

            def run_grover():
                return grover.search(key_space_bits=bits, target_key=target)

            result = self.run_benchmark(run_grover, iterations=5, bits=bits)
            result.category = "grover_algorithm"
            print(
                f"[BENCHMARK]   {description}: {result.avg_time_per_iteration*1000:.2f}ms"
            )

    def benchmark_pqc_attacks(self):
        """Benchmark PQC attack frameworks"""
        print("\n[BENCHMARK] Post-Quantum Cryptography Attacks...")

        # Kyber attacks
        print("[BENCHMARK]   CRYSTALS-Kyber...")
        attacker = KyberAttack(parameter_set="kyber512")

        def kyber_timing():
            return attacker.timing_attack(num_samples=100)

        result = self.run_benchmark(kyber_timing, iterations=5)
        result.category = "pqc_kyber"
        print(
            f"[BENCHMARK]     Timing attack (100 samples): {result.avg_time_per_iteration:.2f}s"
        )

        def kyber_cca():
            return attacker.cca_attack(num_queries=50)

        result = self.run_benchmark(kyber_cca, iterations=3)
        result.category = "pqc_kyber"
        print(
            f"[BENCHMARK]     CCA attack (50 queries): {result.avg_time_per_iteration:.2f}s"
        )

        # Dilithium attacks
        print("[BENCHMARK]   CRYSTALS-Dilithium...")
        attacker = DilithiumAttack(parameter_set="dilithium2")

        def dilithium_forgery():
            return attacker.signature_forgery_attack(num_attempts=50)

        result = self.run_benchmark(dilithium_forgery, iterations=3)
        result.category = "pqc_dilithium"
        print(
            f"[BENCHMARK]     Forgery attack (50 attempts): {result.avg_time_per_iteration:.2f}s"
        )

    def detect_regressions(self, threshold: float = 0.15) -> List[Dict[str, Any]]:
        """
        Detect performance regressions by comparing to baseline.

        Args:
            threshold: Percentage slowdown threshold (0.15 = 15%)

        Returns:
            List of detected regressions
        """
        if not self.baseline:
            print("[BENCHMARK] No baseline loaded, loading from disk...")
            self.load_baseline()

        if not self.baseline:
            print("[BENCHMARK] No baseline available for comparison")
            return []

        regressions = []

        for result in self.results:
            baseline_time = self.baseline.get(result.name)

            if baseline_time is None:
                continue

            # Calculate slowdown percentage
            slowdown = (result.avg_time_per_iteration - baseline_time) / baseline_time

            if slowdown > threshold:
                regressions.append(
                    {
                        "name": result.name,
                        "category": result.category,
                        "baseline_time": baseline_time,
                        "current_time": result.avg_time_per_iteration,
                        "slowdown_percent": slowdown * 100,
                        "threshold_percent": threshold * 100,
                    }
                )

        return regressions

    def save_baseline(self):
        """Save current results as baseline"""
        baseline = {}

        for result in self.results:
            baseline[result.name] = result.avg_time_per_iteration

        baseline_file = self.results_dir / "baseline.json"

        with open(baseline_file, "w") as f:
            json.dump(baseline, f, indent=2)

        print(f"[BENCHMARK] Baseline saved to {baseline_file}")

    def load_baseline(self):
        """Load baseline from disk"""
        baseline_file = self.results_dir / "baseline.json"

        if not baseline_file.exists():
            return

        with open(baseline_file, "r") as f:
            self.baseline = json.load(f)

        print(f"[BENCHMARK] Baseline loaded ({len(self.baseline)} benchmarks)")

    def save_results(self):
        """Save benchmark results to disk"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = self.results_dir / f"benchmark_{timestamp}.json"

        results_data = {
            "timestamp": timestamp,
            "benchmarks": [asdict(r) for r in self.results],
        }

        with open(results_file, "w") as f:
            json.dump(results_data, f, indent=2)

        print(f"[BENCHMARK] Results saved to {results_file}")

    def generate_report(self) -> str:
        """Generate comprehensive benchmark report"""
        report = []
        report.append("=" * 70)
        report.append("HOUDINIS BENCHMARK REPORT")
        report.append("=" * 70)
        report.append(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total benchmarks: {len(self.results)}")
        report.append("")

        # Group by category
        categories = {}
        for result in self.results:
            if result.category not in categories:
                categories[result.category] = []
            categories[result.category].append(result)

        # Report by category
        for category, results in sorted(categories.items()):
            report.append(f"Category: {category.upper()}")
            report.append("-" * 70)

            for result in results:
                report.append(f"  {result.name}:")
                report.append(f"    Avg: {result.avg_time_per_iteration*1000:.2f}ms")
                report.append(f"    Std Dev: {result.std_dev*1000:.2f}ms")
                report.append(
                    f"    Range: {result.min_time*1000:.2f}ms - {result.max_time*1000:.2f}ms"
                )
                report.append(f"    Iterations: {result.iterations}")

            report.append("")

        # Regression detection
        regressions = self.detect_regressions()

        if regressions:
            report.append("PERFORMANCE REGRESSIONS DETECTED")
            report.append("-" * 70)

            for reg in regressions:
                report.append(f"   {reg['name']}:")
                report.append(f"    Baseline: {reg['baseline_time']*1000:.2f}ms")
                report.append(f"    Current: {reg['current_time']*1000:.2f}ms")
                report.append(f"    Slowdown: {reg['slowdown_percent']:.1f}%")

            report.append("")
        else:
            report.append(" No performance regressions detected")
            report.append("")

        # Summary statistics
        total_time = sum(r.execution_time for r in self.results)
        avg_time = statistics.mean(r.avg_time_per_iteration for r in self.results)

        report.append("SUMMARY")
        report.append("-" * 70)
        report.append(f"Total execution time: {total_time:.2f}s")
        report.append(f"Average benchmark time: {avg_time*1000:.2f}ms")
        report.append("")
        report.append("=" * 70)

        return "\n".join(report)


@pytest.mark.benchmark
class TestBenchmarkSuite:
    """Test cases for the benchmark suite itself"""

    def test_benchmark_suite_initialization(self):
        """Test benchmark suite initialization"""
        suite = BenchmarkSuite()
        assert suite.results_dir.exists()
        assert len(suite.results) == 0

    def test_run_simple_benchmark(self):
        """Test running a simple benchmark"""
        suite = BenchmarkSuite()

        def simple_func():
            time.sleep(0.01)

        result = suite.run_benchmark(simple_func, iterations=5)

        assert result.iterations == 5
        assert result.avg_time_per_iteration > 0.01
        assert result.std_dev >= 0

    def test_save_and_load_baseline(self):
        """Test saving and loading baseline"""
        suite = BenchmarkSuite()

        def dummy_func():
            time.sleep(0.001)

        suite.run_benchmark(dummy_func, iterations=5)
        suite.save_baseline()

        # Load in new suite
        suite2 = BenchmarkSuite()
        suite2.load_baseline()

        assert suite2.baseline is not None
        assert "dummy_func" in suite2.baseline


def run_all_benchmarks(save_baseline: bool = False):
    """
    Run complete benchmark suite.

    Args:
        save_baseline: If True, save results as new baseline
    """
    print("\n" + "=" * 70)
    print("HOUDINIS COMPREHENSIVE BENCHMARK SUITE")
    print("=" * 70)

    suite = BenchmarkSuite()
    suite.load_baseline()

    # Run all benchmark categories
    try:
        suite.benchmark_quantum_operations()
    except Exception as e:
        print(f"[BENCHMARK] Quantum ops failed: {e}")

    try:
        suite.benchmark_shor_algorithm()
    except Exception as e:
        print(f"[BENCHMARK] Shor algorithm failed: {e}")

    try:
        suite.benchmark_grover_search()
    except Exception as e:
        print(f"[BENCHMARK] Grover search failed: {e}")

    try:
        suite.benchmark_pqc_attacks()
    except Exception as e:
        print(f"[BENCHMARK] PQC attacks failed: {e}")

    # Generate and print report
    print("\n")
    report = suite.generate_report()
    print(report)

    # Save results
    suite.save_results()

    if save_baseline:
        suite.save_baseline()
        print("\n[BENCHMARK]  Baseline updated")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Houdinis Benchmark Suite")
    parser.add_argument(
        "--save-baseline",
        action="store_true",
        help="Save current results as new baseline",
    )
    parser.add_argument("--pytest", action="store_true", help="Run pytest benchmarks")

    args = parser.parse_args()

    if args.pytest:
        pytest.main([__file__, "-v", "-m", "benchmark"])
    else:
        run_all_benchmarks(save_baseline=args.save_baseline)
