"""
Houdinis Framework - Performance Benchmarking Suite
Data de Criação: 15 de dezembro de 2025
Author: Mauro Risonho de Paula Assumpção aka firebitsbr
License: MIT

Comprehensive benchmarking and performance profiling for quantum algorithms.
"""

import time
import psutil
import os
import json
from typing import Dict, Any, List, Callable, Optional
from pathlib import Path
import numpy as np


class PerformanceBenchmark:
    """
    Performance benchmarking and profiling for Houdinis framework.
    
    Tracks execution time, memory usage, and quantum resource utilization.
    """
    
    def __init__(self, output_dir: str = "benchmarks") -> None:
        """
        Initialize performance benchmark.
        
        Args:
            output_dir: Directory to save benchmark results
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.results: List[Dict[str, Any]] = []
        
    def benchmark_function(
        self,
        func: Callable,
        *args,
        name: str = "unnamed",
        iterations: int = 10,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Benchmark a function's performance.
        
        Args:
            func: Function to benchmark
            *args: Positional arguments for function
            name: Name of the benchmark
            iterations: Number of iterations to run
            **kwargs: Keyword arguments for function
            
        Returns:
            Benchmark results dictionary
        """
        print(f"[*] Benchmarking: {name}")
        
        times = []
        memory_usage = []
        
        for i in range(iterations):
            # Measure memory before
            process = psutil.Process(os.getpid())
            mem_before = process.memory_info().rss / 1024 / 1024  # MB
            
            # Time the execution
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            
            # Measure memory after
            mem_after = process.memory_info().rss / 1024 / 1024  # MB
            
            execution_time = end_time - start_time
            memory_delta = mem_after - mem_before
            
            times.append(execution_time)
            memory_usage.append(memory_delta)
            
            print(f"    Iteration {i+1}/{iterations}: {execution_time:.4f}s, Memory: {memory_delta:.2f}MB")
        
        # Calculate statistics
        benchmark_result = {
            "name": name,
            "iterations": iterations,
            "times": {
                "min": min(times),
                "max": max(times),
                "mean": np.mean(times),
                "median": np.median(times),
                "std": np.std(times),
            },
            "memory": {
                "min_mb": min(memory_usage),
                "max_mb": max(memory_usage),
                "mean_mb": np.mean(memory_usage),
            },
            "timestamp": time.time(),
        }
        
        self.results.append(benchmark_result)
        
        print(f"[+] Average time: {benchmark_result['times']['mean']:.4f}s ± {benchmark_result['times']['std']:.4f}s")
        print(f"[+] Average memory: {benchmark_result['memory']['mean_mb']:.2f}MB")
        
        return benchmark_result
    
    def compare_implementations(
        self,
        implementations: Dict[str, Callable],
        *args,
        iterations: int = 5,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Compare multiple implementations of the same algorithm.
        
        Args:
            implementations: Dictionary of {name: function}
            *args: Arguments to pass to functions
            iterations: Number of iterations per implementation
            **kwargs: Keyword arguments to pass to functions
            
        Returns:
            Comparison results
        """
        print(f"\n[*] Comparing {len(implementations)} implementations")
        print("=" * 60)
        
        comparison_results = {}
        
        for name, func in implementations.items():
            result = self.benchmark_function(
                func, *args, name=name, iterations=iterations, **kwargs
            )
            comparison_results[name] = result
        
        # Find the fastest
        fastest = min(
            comparison_results.items(),
            key=lambda x: x[1]['times']['mean']
        )
        
        print(f"\n[+] Fastest implementation: {fastest[0]}")
        print(f"    Average time: {fastest[1]['times']['mean']:.4f}s")
        
        # Calculate speedup ratios
        baseline_time = list(comparison_results.values())[0]['times']['mean']
        
        print(f"\n Speedup Analysis (baseline: {list(comparison_results.keys())[0]})")
        for name, result in comparison_results.items():
            speedup = baseline_time / result['times']['mean']
            print(f"    {name}: {speedup:.2f}x")
        
        return comparison_results
    
    def save_results(self, filename: Optional[str] = None) -> str:
        """
        Save benchmark results to JSON file.
        
        Args:
            filename: Optional custom filename
            
        Returns:
            Path to saved file
        """
        if filename is None:
            filename = f"benchmark_{int(time.time())}.json"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"[+] Benchmark results saved to: {filepath}")
        return str(filepath)
    
    def load_results(self, filename: str) -> List[Dict[str, Any]]:
        """
        Load benchmark results from JSON file.
        
        Args:
            filename: Filename to load
            
        Returns:
            List of benchmark results
        """
        filepath = self.output_dir / filename
        
        with open(filepath, 'r') as f:
            results = json.load(f)
        
        print(f"[+] Loaded {len(results)} benchmark results from: {filepath}")
        return results
    
    def generate_report(self) -> str:
        """
        Generate a formatted benchmark report.
        
        Returns:
            Formatted report string
        """
        if not self.results:
            return "No benchmark results available."
        
        report = []
        report.append("\n" + "=" * 60)
        report.append("PERFORMANCE BENCHMARK REPORT")
        report.append("=" * 60)
        
        for i, result in enumerate(self.results, 1):
            report.append(f"\n{i}. {result['name']}")
            report.append(f"   Iterations: {result['iterations']}")
            report.append(f"   Time (mean ± std): {result['times']['mean']:.4f}s ± {result['times']['std']:.4f}s")
            report.append(f"   Time (min/max): {result['times']['min']:.4f}s / {result['times']['max']:.4f}s")
            report.append(f"   Memory (mean): {result['memory']['mean_mb']:.2f}MB")
        
        report.append("\n" + "=" * 60)
        
        report_str = "\n".join(report)
        print(report_str)
        return report_str


class QuantumAlgorithmBenchmark:
    """Specialized benchmarking for quantum algorithms."""
    
    def __init__(self) -> None:
        """Initialize quantum algorithm benchmark."""
        self.benchmark = PerformanceBenchmark(output_dir="benchmarks/quantum")
    
    def benchmark_shors_algorithm(
        self,
        N_values: List[int],
        iterations: int = 5
    ) -> Dict[str, Any]:
        """
        Benchmark Shor's algorithm for different input sizes.
        
        Args:
            N_values: List of numbers to factor
            iterations: Iterations per size
            
        Returns:
            Benchmark results
        """
        from quantum.simulator import QuantumSimulator
        
        print("\n[*] Benchmarking Shor's Algorithm")
        print("=" * 60)
        
        results = {}
        
        for N in N_values:
            print(f"\n[*] Testing N = {N}")
            
            sim = QuantumSimulator(num_qubits=20)
            a = 7  # Common coprime for testing
            
            result = self.benchmark.benchmark_function(
                sim.simulate_shors_period_finding,
                N, a,
                name=f"Shor's (N={N})",
                iterations=iterations
            )
            
            results[f"N={N}"] = result
        
        return results
    
    def benchmark_grovers_algorithm(
        self,
        database_sizes: List[int],
        iterations: int = 5
    ) -> Dict[str, Any]:
        """
        Benchmark Grover's algorithm for different database sizes.
        
        Args:
            database_sizes: List of database sizes
            iterations: Iterations per size
            
        Returns:
            Benchmark results
        """
        from quantum.simulator import QuantumSimulator
        
        print("\n[*] Benchmarking Grover's Algorithm")
        print("=" * 60)
        
        results = {}
        
        for size in database_sizes:
            print(f"\n[*] Testing database size = {size}")
            
            sim = QuantumSimulator(num_qubits=20)
            target = [size // 2]  # Search for middle element
            
            result = self.benchmark.benchmark_function(
                sim.simulate_grovers_search,
                size, target,
                name=f"Grover's (size={size})",
                iterations=iterations
            )
            
            results[f"size={size}"] = result
        
        return results
    
    def benchmark_quantum_annealing(
        self,
        problem_sizes: List[int],
        iterations: int = 3
    ) -> Dict[str, Any]:
        """
        Benchmark quantum annealing for different problem sizes.
        
        Args:
            problem_sizes: List of problem sizes
            iterations: Iterations per size
            
        Returns:
            Benchmark results
        """
        from exploits.quantum_annealing_attack import QuantumAnnealingAttack
        
        print("\n[*] Benchmarking Quantum Annealing")
        print("=" * 60)
        
        results = {}
        
        for size in problem_sizes:
            print(f"\n[*] Testing problem size = {size}")
            
            qa = QuantumAnnealingAttack(problem_size=size)
            
            # Create test knapsack problem
            weights = list(range(1, size + 1))
            values = list(range(2, size + 2))
            capacity = sum(weights) // 2
            
            result = self.benchmark.benchmark_function(
                qa.solve_knapsack_annealing,
                weights, values, capacity,
                name=f"Annealing (size={size})",
                iterations=iterations
            )
            
            results[f"size={size}"] = result
        
        return results
    
    def run_comprehensive_suite(self) -> None:
        """Run comprehensive quantum algorithm benchmark suite."""
        print("\n" + "=" * 60)
        print("COMPREHENSIVE QUANTUM ALGORITHM BENCHMARK SUITE")
        print("=" * 60)
        
        # Benchmark Shor's algorithm
        print("\n Phase 1: Shor's Algorithm")
        self.benchmark_shors_algorithm(N_values=[15, 21, 35], iterations=3)
        
        # Benchmark Grover's algorithm
        print("\n Phase 2: Grover's Algorithm")
        self.benchmark_grovers_algorithm(database_sizes=[16, 64, 256], iterations=3)
        
        # Benchmark quantum annealing
        print("\n Phase 3: Quantum Annealing")
        self.benchmark_quantum_annealing(problem_sizes=[4, 6, 8], iterations=2)
        
        # Generate and save report
        report = self.benchmark.generate_report()
        self.benchmark.save_results("comprehensive_benchmark.json")
        
        print("\n[+] Comprehensive benchmark suite complete!")


def demonstrate_benchmarking() -> None:
    """Demonstrate benchmarking capabilities."""
    print("=" * 60)
    print("Houdinis Performance Benchmarking Demonstration")
    print("=" * 60)
    
    # Create benchmark suite
    quantum_bench = QuantumAlgorithmBenchmark()
    
    # Run comprehensive suite
    quantum_bench.run_comprehensive_suite()


if __name__ == "__main__":
    demonstrate_benchmarking()
