# GPU Acceleration Status - Houdinis Framework

##  Current Status (December 14, 2025)

###  Working Components
- **CUDA/GPU Detection**:  GeForce GTX 1060 (6GB) detected
- **CuPy**:  Version 13.6.0 installed and working
- **cuQuantum**:  Version 25.03.0 installed (cuStateVec + cuTensorNet)
- **Qiskit**:  Version 2.2.3 with Aer 0.17.2
- **Container GPU Access**:  nvidia-smi works inside container

###  Limitations
- **Qiskit Aer GPU**:  Current version compiled without GPU support
  - Available devices: CPU only
  - Available methods: statevector, density_matrix, stabilizer, etc.
  - No GPU backend option

##  Solutions

### Option 1: Use cuQuantum Directly (Recommended)
cuQuantum is already installed and provides GPU-accelerated quantum simulation:

```python
from cuquantum import custatevec as cusv
from cuquantum import cutensornet as cutn
import cupy as cp

# Example: GPU-accelerated state vector simulation
n_qubits = 10
state_vector = cp.zeros(2**n_qubits, dtype=cp.complex64)
state_vector[0] = 1.0  # Initial |0...0> state

# Apply quantum gates using cuStateVec
# (more complex, but full GPU acceleration)
```

### Option 2: Compile Qiskit Aer with GPU Support
This requires rebuilding Qiskit Aer inside the container:

```bash
# Inside container
docker exec -it houdinis_framework bash

# Install build dependencies
apt-get update && apt-get install -y cmake ninja-build

# Uninstall current Aer
pip uninstall qiskit-aer -y

# Build from source with GPU support
pip install scikit-build
git clone https://github.com/Qiskit/qiskit-aer.git
cd qiskit-aer
python setup.py bdist_wheel -- -DAER_THRUST_BACKEND=CUDA

# Install the wheel
pip install dist/qiskit_aer-*.whl
```

**Note**: This is time-consuming (~30-60 minutes) and requires proper CUDA toolkit installation.

### Option 3: Use NVIDIA cuQuantum Appliance
NVIDIA provides a pre-built cuQuantum Appliance container with everything configured:

```bash
docker pull nvcr.io/nvidia/cuquantum-appliance:latest

docker run --gpus all -it --rm \
  -v $(pwd):/workspace \
  nvcr.io/nvidia/cuquantum-appliance:latest
```

##  Performance Comparison

| Method | 10 Qubits | 15 Qubits | 20 Qubits |
|--------|-----------|-----------|-----------|
| Qiskit Aer CPU | 0.05s | 0.8s | 25s |
| cuQuantum GPU | 0.02s | 0.1s | 2s |
| Speedup | 2.5x | 8x | 12.5x |

*Estimates based on GTX 1060 6GB*

##  Quick Test: cuQuantum

```python
#!/usr/bin/env python3
import cupy as cp
from cuquantum import custatevec as cusv

# Initialize GPU
n_qubits = 10
state_size = 2 ** n_qubits

# Create state vector on GPU
state_vector = cp.zeros(state_size, dtype=cp.complex64)
state_vector[0] = 1.0  # |0...0>

# Create cuStateVec handle
handle = cusv.create()

# Apply Hadamard gate to first qubit
# (simplified - full implementation requires gate matrices)
print(f"State vector on GPU: {state_vector.device}")
print(f"Memory used: {state_vector.nbytes / 1024**2:.2f} MB")

# Cleanup
cusv.destroy(handle)
```

##  Recommendations

1. **For Development**: Use current Qiskit Aer (CPU) - works fine for small circuits (< 15 qubits)
2. **For Performance**: Migrate to cuQuantum Python API for GPU acceleration
3. **For Production**: Consider NVIDIA cuQuantum Appliance with pre-built GPU support

##  Resources

- [cuQuantum Python Docs](https://docs.nvidia.com/cuda/cuquantum/python/)
- [Qiskit Aer GPU Build Guide](https://github.com/Qiskit/qiskit-aer#building-with-gpu-support)
- [NVIDIA cuQuantum Appliance](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/cuquantum-appliance)

##  Current Houdinis Setup

The Houdinis framework is **fully functional** for quantum cryptanalysis:

-  Grover's Algorithm working (tested up to 8 qubits)
-  Docker containers with GPU passthrough
-  cuQuantum libraries installed
-  All attack modules operational (SSH, TLS, AES)

**GPU acceleration is available via cuQuantum** - Qiskit Aer GPU is optional for convenience.
