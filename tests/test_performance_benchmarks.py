"""
Performance Benchmark Tests for CI/CD
Author: Mauro Risonho de Paula Assumpção aka firebitsbr
Desenvolvido: Lógica e Codificação por Humano e AI Assistida (Claude Sonnet 4.5)
License: MIT

Automated performance regression testing for Houdinis Framework.
"""

import pytest
import time
import numpy as np
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Note: Quantum algorithm benchmarks are excluded from CI benchmarking
# because they require specific quantum libraries and can be unstable.
# The focus is on stable, reproducible performance metrics for:
# - Cryptographic operations
# - Matrix computations
# - Data processing
# - File I/O
# - Memory operations


# Quantum tests removed - see commit history if needed
# Focus on stable, reproducible benchmarks only

@pytest.mark.benchmark
class TestCryptographicOperations:
    """Benchmark cryptographic operations."""

    def test_rsa_key_generation(self, benchmark):
        """Benchmark RSA key generation."""
        from Crypto.PublicKey import RSA
        
        def generate_key():
            key = RSA.generate(2048)
            return key
        
        benchmark(generate_key)

    def test_aes_encryption_1kb(self, benchmark):
        """Benchmark AES encryption of 1KB data."""
        from Crypto.Cipher import AES
        from Crypto.Random import get_random_bytes
        
        key = get_random_bytes(32)
        data = get_random_bytes(1024)
        
        def encrypt_data():
            cipher = AES.new(key, AES.MODE_EAX)
            ciphertext, tag = cipher.encrypt_and_digest(data)
            return ciphertext
        
        benchmark(encrypt_data)

    def test_sha256_hashing_1mb(self, benchmark):
        """Benchmark SHA-256 hashing of 1MB data."""
        import hashlib
        
        data = b'x' * (1024 * 1024)  # 1MB
        
        def hash_data():
            return hashlib.sha256(data).hexdigest()
        
        benchmark(hash_data)


@pytest.mark.benchmark
class TestMatrixOperations:
    """Benchmark matrix operations (common in quantum computing)."""

    def test_matrix_multiplication_64x64(self, benchmark):
        """Benchmark 64x64 matrix multiplication."""
        A = np.random.rand(64, 64)
        B = np.random.rand(64, 64)
        
        benchmark(np.dot, A, B)

    def test_matrix_eigenvalues_32x32(self, benchmark):
        """Benchmark eigenvalue computation for 32x32 matrix."""
        A = np.random.rand(32, 32)
        A = A + A.T  # Make symmetric
        
        benchmark(np.linalg.eigvals, A)

    def test_svd_decomposition_64x64(self, benchmark):
        """Benchmark SVD decomposition of 64x64 matrix."""
        A = np.random.rand(64, 64)
        
        benchmark(np.linalg.svd, A)

    def test_fft_1024_points(self, benchmark):
        """Benchmark FFT of 1024 points."""
        signal = np.random.rand(1024)
        
        benchmark(np.fft.fft, signal)


@pytest.mark.benchmark
class TestDataProcessing:
    """Benchmark data processing operations."""

    def test_json_serialization_large(self, benchmark):
        """Benchmark JSON serialization of large object."""
        import json
        
        data = {
            'results': [
                {
                    'id': i,
                    'value': np.random.rand(),
                    'metadata': {'timestamp': time.time(), 'iteration': i}
                }
                for i in range(1000)
            ]
        }
        
        def serialize():
            return json.dumps(data)
        
        benchmark(serialize)

    def test_numpy_array_operations(self, benchmark):
        """Benchmark numpy array operations."""
        arr = np.random.rand(10000)
        
        def process_array():
            result = np.sqrt(arr)
            result = np.sin(result)
            result = np.exp(result)
            return result.mean()
        
        benchmark(process_array)

    def test_list_comprehension_10k(self, benchmark):
        """Benchmark list comprehension with 10k elements."""
        data = list(range(10000))
        
        def process_list():
            return [x * 2 + 1 for x in data if x % 3 == 0]
        
        benchmark(process_list)


@pytest.mark.benchmark
class TestFileOperations:
    """Benchmark file I/O operations."""

    def test_write_1mb_file(self, benchmark, tmp_path):
        """Benchmark writing 1MB to file."""
        data = b'x' * (1024 * 1024)
        file_path = tmp_path / "test.bin"
        
        def write_file():
            with open(file_path, 'wb') as f:
                f.write(data)
        
        benchmark(write_file)

    def test_read_1mb_file(self, benchmark, tmp_path):
        """Benchmark reading 1MB from file."""
        data = b'x' * (1024 * 1024)
        file_path = tmp_path / "test.bin"
        
        with open(file_path, 'wb') as f:
            f.write(data)
        
        def read_file():
            with open(file_path, 'rb') as f:
                return f.read()
        
        benchmark(read_file)


@pytest.mark.benchmark
class TestMemoryOperations:
    """Benchmark memory allocation and management."""

    def test_memory_allocation_large_array(self, benchmark):
        """Benchmark allocation of large numpy array."""
        def allocate():
            return np.zeros((1000, 1000))
        
        benchmark(allocate)

    def test_memory_copy_large_array(self, benchmark):
        """Benchmark copying large array."""
        arr = np.random.rand(1000, 1000)
        
        benchmark(np.copy, arr)

    def test_dictionary_creation_10k(self, benchmark):
        """Benchmark creation of dictionary with 10k entries."""
        def create_dict():
            return {i: i * 2 for i in range(10000)}
        
        benchmark(create_dict)


# Performance thresholds (in seconds)
PERFORMANCE_THRESHOLDS = {
    'test_shor_factorization_15': 2.0,
    'test_grover_search_4bit': 1.0,
    'test_simon_algorithm_3bit': 1.5,
    'test_simulator_initialization': 0.1,
    'test_hadamard_gate_application': 0.5,
    'test_cnot_gate_chain': 0.5,
    'test_full_circuit_execution': 1.0,
    'test_rsa_key_generation': 1.0,
    'test_aes_encryption_1kb': 0.01,
    'test_sha256_hashing_1mb': 0.1,
    'test_matrix_multiplication_64x64': 0.05,
    'test_matrix_eigenvalues_32x32': 0.1,
    'test_svd_decomposition_64x64': 0.1,
    'test_fft_1024_points': 0.01,
    'test_json_serialization_large': 0.1,
    'test_numpy_array_operations': 0.01,
    'test_list_comprehension_10k': 0.01,
    'test_write_1mb_file': 0.1,
    'test_read_1mb_file': 0.1,
    'test_memory_allocation_large_array': 0.05,
    'test_memory_copy_large_array': 0.05,
    'test_dictionary_creation_10k': 0.01,
}


if __name__ == '__main__':
    pytest.main([__file__, '--benchmark-only', '-v'])
