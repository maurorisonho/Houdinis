#!/usr/bin/env python3
"""
Houdinis Framework - GPU and cuQuantum Test Script
Tests CUDA, cuQuantum, and quantum circuit execution with GPU acceleration
"""

import sys
import subprocess


def print_section(title):
    """Print formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def test_cuda_availability():
    """Test if CUDA is available and accessible"""
    print_section("1. CUDA Availability Test")
    
    try:
        import torch
        cuda_available = torch.cuda.is_available()
        print(f" PyTorch CUDA available: {cuda_available}")
        
        if cuda_available:
            print(f"  GPU Count: {torch.cuda.device_count()}")
            print(f"  Current Device: {torch.cuda.current_device()}")
            print(f"  Device Name: {torch.cuda.get_device_name(0)}")
            print(f"  CUDA Version: {torch.version.cuda}")
        return cuda_available
    except ImportError:
        print(" PyTorch not installed, trying alternative method...")
        
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        if result.returncode == 0:
            print(" NVIDIA GPU detected via nvidia-smi")
            print(result.stdout)
            return True
        else:
            print(" nvidia-smi failed")
            return False
    except FileNotFoundError:
        print(" nvidia-smi not found")
        return False


def test_cupy():
    """Test CuPy CUDA Python library"""
    print_section("2. CuPy Test")
    
    try:
        import cupy as cp
        print(f" CuPy version: {cp.__version__}")
        
        # Test GPU array creation
        x = cp.array([1, 2, 3, 4, 5])
        print(f" Created CuPy array: {x}")
        print(f"  Device: {x.device}")
        
        # Test computation
        result = cp.sum(x ** 2)
        print(f" Sum of squares: {result}")
        
        # Test GPU info
        device = cp.cuda.Device()
        print(f"\n GPU Information:")
        print(f"  Name: {device.attributes['Name']}")
        print(f"  Compute Capability: {device.compute_capability}")
        print(f"  Total Memory: {device.mem_info[1] / 1024**3:.2f} GB")
        print(f"  Free Memory: {device.mem_info[0] / 1024**3:.2f} GB")
        
        return True
    except ImportError as e:
        print(f" CuPy not available: {e}")
        return False
    except Exception as e:
        print(f" CuPy test failed: {e}")
        return False


def test_cuquantum():
    """Test cuQuantum library"""
    print_section("3. cuQuantum Test")
    
    try:
        import cuquantum
        print(f" cuQuantum version: {cuquantum.__version__}")
        
        # Test cuQuantum Python
        try:
            from cuquantum import custatevec
            print(f" cuStateVec available")
            print(f"  Version: {custatevec.get_version()}")
        except Exception as e:
            print(f" cuStateVec: {e}")
        
        try:
            from cuquantum import cutensornet
            print(f" cuTensorNet available")
            print(f"  Version: {cutensornet.get_version()}")
        except Exception as e:
            print(f" cuTensorNet: {e}")
        
        return True
    except ImportError as e:
        print(f" cuQuantum not available: {e}")
        return False
    except Exception as e:
        print(f" cuQuantum test failed: {e}")
        return False


def test_qiskit_aer_gpu():
    """Test Qiskit Aer with GPU support"""
    print_section("4. Qiskit Aer GPU Test")
    
    try:
        from qiskit import QuantumCircuit, transpile
        from qiskit_aer import AerSimulator
        import numpy as np
        
        print(f" Qiskit Aer imported successfully")
        
        # Create a simple quantum circuit
        n_qubits = 10
        circuit = QuantumCircuit(n_qubits, n_qubits)
        
        # Apply Hadamard gates
        circuit.h(range(n_qubits))
        
        # Add some entanglement
        for i in range(n_qubits - 1):
            circuit.cx(i, i + 1)
        
        # Measure
        circuit.measure(range(n_qubits), range(n_qubits))
        
        print(f" Created quantum circuit with {n_qubits} qubits")
        print(f"  Circuit depth: {circuit.depth()}")
        print(f"  Circuit gates: {sum(circuit.count_ops().values())}")
        
        # Test with GPU simulator
        try:
            simulator = AerSimulator(method='statevector', device='GPU')
            print(f" AerSimulator with GPU device created")
            
            # Transpile and run
            transpiled = transpile(circuit, simulator)
            job = simulator.run(transpiled, shots=1000)
            result = job.result()
            counts = result.get_counts()
            
            print(f" Quantum circuit executed on GPU")
            print(f"  Measurement results: {len(counts)} unique states")
            print(f"  Top 3 states:")
            for state, count in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:3]:
                print(f"    {state}: {count}/1000")
            
            return True
        except Exception as e:
            print(f" GPU execution failed, trying CPU: {e}")
            
            # Fallback to CPU
            simulator = AerSimulator()
            transpiled = transpile(circuit, simulator)
            job = simulator.run(transpiled, shots=1000)
            result = job.result()
            print(f" Quantum circuit executed on CPU (fallback)")
            return False
            
    except ImportError as e:
        print(f" Qiskit Aer not available: {e}")
        return False
    except Exception as e:
        print(f" Qiskit Aer test failed: {e}")
        return False


def test_grover_gpu():
    """Test Grover's algorithm with GPU acceleration"""
    print_section("5. Grover's Algorithm GPU Test")
    
    try:
        from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
        from qiskit_aer import AerSimulator
        import numpy as np
        
        # Parameters
        n_qubits = 8
        search_space = 2 ** n_qubits
        target = np.random.randint(0, search_space)
        
        print(f" Testing Grover with {n_qubits} qubits")
        print(f"  Search space: {search_space} states")
        print(f"  Target state: {target} (binary: {format(target, f'0{n_qubits}b')})")
        
        # Create Grover circuit
        qreg = QuantumRegister(n_qubits, 'q')
        creg = ClassicalRegister(n_qubits, 'c')
        circuit = QuantumCircuit(qreg, creg)
        
        # Initialize superposition
        circuit.h(qreg)
        
        # Oracle (simplified)
        target_binary = format(target, f'0{n_qubits}b')
        for i, bit in enumerate(target_binary):
            if bit == '0':
                circuit.x(i)
        circuit.h(n_qubits-1)
        circuit.mcx(list(range(n_qubits-1)), n_qubits-1)
        circuit.h(n_qubits-1)
        for i, bit in enumerate(target_binary):
            if bit == '0':
                circuit.x(i)
        
        # Diffusion
        circuit.h(range(n_qubits))
        circuit.x(range(n_qubits))
        circuit.h(n_qubits-1)
        circuit.mcx(list(range(n_qubits-1)), n_qubits-1)
        circuit.h(n_qubits-1)
        circuit.x(range(n_qubits))
        circuit.h(range(n_qubits))
        
        circuit.measure(qreg, creg)
        
        print(f" Grover circuit created")
        print(f"  Depth: {circuit.depth()}")
        print(f"  Gates: {sum(circuit.count_ops().values())}")
        
        # Try GPU execution
        try:
            simulator = AerSimulator(method='statevector', device='GPU')
            print(f" Running on GPU...")
            
            import time
            start = time.time()
            transpiled = transpile(circuit, simulator)
            job = simulator.run(transpiled, shots=1024)
            result = job.result()
            elapsed = time.time() - start
            
            counts = result.get_counts()
            print(f" GPU execution completed in {elapsed:.3f}s")
            
            # Check if target found
            target_binary_reversed = target_binary[::-1]
            success_count = counts.get(target_binary_reversed, 0)
            success_rate = success_count / 1024
            
            print(f"\n Results:")
            print(f"  Success rate: {success_rate:.1%}")
            print(f"  Classical probability: {1/search_space:.3%}")
            print(f"  Quantum advantage: {(success_rate / (1/search_space)):.1f}x")
            
            return True
        except Exception as e:
            print(f" GPU execution failed: {e}")
            print(f"  Falling back to CPU...")
            
            simulator = AerSimulator()
            import time
            start = time.time()
            transpiled = transpile(circuit, simulator)
            job = simulator.run(transpiled, shots=1024)
            result = job.result()
            elapsed = time.time() - start
            print(f" CPU execution completed in {elapsed:.3f}s")
            return False
            
    except Exception as e:
        print(f" Grover GPU test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all GPU and cuQuantum tests"""
    print("\n" + "" * 80)
    print("  HOUDINIS FRAMEWORK - GPU & cuQuantum Test Suite")
    print("" * 80)
    
    results = {}
    
    # Run tests
    results['CUDA'] = test_cuda_availability()
    results['CuPy'] = test_cupy()
    results['cuQuantum'] = test_cuquantum()
    results['Qiskit Aer GPU'] = test_qiskit_aer_gpu()
    results['Grover GPU'] = test_grover_gpu()
    
    # Summary
    print_section("Test Summary")
    
    for test_name, passed in results.items():
        status = " PASS" if passed else " FAIL"
        print(f"  {status:10} {test_name}")
    
    passed_count = sum(results.values())
    total_count = len(results)
    
    print(f"\n Total: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n  All tests passed! GPU acceleration is fully functional.")
        return 0
    elif passed_count >= 3:
        print("\n  Some tests failed, but core functionality is available.")
        return 0
    else:
        print("\n  Critical tests failed. GPU acceleration may not be available.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
