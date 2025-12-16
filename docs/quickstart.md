# Quick Start Guide

Get started with Houdinis in 10 minutes! This guide walks you through running your first quantum cryptanalysis attack.

##  Option 1: Try in Browser (Fastest!)

**Zero installation required!** Launch an interactive tutorial in your browser:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/maurorisonho/Houdinis/main?labpath=notebooks%2Fplayground.ipynb)

**What you'll get:**
-  5-minute interactive tutorial
-  Live quantum circuit execution
-  Grover's algorithm demo
-  RSA security analysis
-  All 9 comprehensive notebooks

**Perfect for:** Learning, quick demos, testing concepts

---

##  Option 2: Local Installation

For production use and full features:

### Prerequisites

 Houdinis installed ([Installation Guide](installation.md))  
 Virtual environment activated  
 Basic understanding of quantum computing (optional but helpful)

## Your First Quantum Attack: RSA Factorization

### Step 1: Verify Installation

```bash
cd Houdinis
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Check installation
python main.py --version
```

### Step 2: Generate RSA Keys for Testing

```bash
# Generate a small RSA key (suitable for quantum simulation)
python -c "
from Crypto.PublicKey import RSA
key = RSA.generate(2048)
with open('test_rsa.pem', 'wb') as f:
    f.write(key.export_key())
print(f'Generated RSA-2048 key')
print(f'Public key (n): {key.n}')
print(f'Public exponent (e): {key.e}')
"
```

### Step 3: Run Shor's Algorithm (Simulation)

```bash
# Run RSA factorization using Shor's algorithm
python exploits/rsa_shor.py \
    --key test_rsa.pem \
    --backend qiskit_aer \
    --verbose
```

**Expected Output:**
```
[+] Houdinis Framework - Shor's Algorithm RSA Attack
[+] Target: test_rsa.pem
[+] Backend: qiskit_aer (Simulator)
[+] Key size: 2048 bits

[*] Extracting public key...
[*] Public modulus (N): 25195908475...
[*] Public exponent (e): 65537

[*] Running Shor's algorithm...
[*] Quantum circuit size: 4096 qubits
[*] Estimated execution time: ~30 seconds

[+] Factorization successful!
[+] p = 158423...
[+] q = 159067...
[+] Private key recovered!

[*] Time elapsed: 28.3 seconds
```

### Step 4: Explore Interactive Notebooks

** Try in Browser (No Setup):**

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/maurorisonho/Houdinis/main?labpath=notebooks%2Fplayground.ipynb)

Start with [`playground.ipynb`](https://mybinder.org/v2/gh/maurorisonho/Houdinis/main?labpath=notebooks%2Fplayground.ipynb) for a 5-minute tutorial!

** Or Run Locally:**

```bash
# Install Jupyter (if not already)
pip install jupyter

# Launch notebook server
jupyter notebook notebooks/
```

**Recommended starting notebooks:**
1. [`playground.ipynb`](../notebooks/playground.ipynb) -  **START HERE** - 5-min interactive intro
2. [`02-Shors_Algorithm_RSA_Exploitation.ipynb`](../notebooks/02-Shors_Algorithm_RSA_Exploitation.ipynb) - Deep dive into RSA factorization
3. [`01-IBM_Quantum_Experience_Integration.ipynb`](../notebooks/01-IBM_Quantum_Experience_Integration.ipynb) - Use real quantum hardware
4. [`03-Grovers_Algorithm_Symmetric_Key_Attacks.ipynb`](../notebooks/03-Grovers_Algorithm_Symmetric_Key_Attacks.ipynb) - AES/symmetric attacks

## Common Use Cases

### Use Case 1: Network Vulnerability Scanning

Scan your network for quantum-vulnerable cryptographic protocols:

```bash
# Scan local network for weak SSL/TLS configurations
python scanners/ssl_scanner.py \
    --target 192.168.1.0/24 \
    --output scan_results.json
```

### Use Case 2: AES Key Recovery (Grover's Algorithm)

Demonstrate Grover's algorithm on symmetric encryption:

```bash
# Attempt to recover AES-128 key
python exploits/grover_bruteforce.py \
    --target-cipher AES-128 \
    --known-plaintext "Hello World" \
    --ciphertext-file encrypted.bin \
    --backend qiskit_aer
```

### Use Case 3: TLS/SSL Quantum Attack Simulation

Simulate quantum attacks on TLS connections:

```bash
# Analyze TLS configuration for quantum vulnerabilities
python exploits/tls_sndl.py \
    --host example.com \
    --port 443 \
    --analyze-only
```

### Use Case 4: Multi-Backend Benchmarking

Compare quantum algorithm performance across backends:

```bash
# Benchmark Shor's algorithm across multiple backends
python exploits/multi_backend_benchmark.py \
    --algorithm shors \
    --key-sizes 512,1024,2048 \
    --backends qiskit_aer,ibm_quantum,aws_braket \
    --output benchmark_results.csv
```

## Interactive CLI Mode

Use the interactive command-line interface:

```bash
# Launch interactive mode
python main.py --interactive

# Example session:
>>> select exploit
1. Shor's Algorithm (RSA/ECC)
2. Grover's Algorithm (Symmetric)
3. Network Scanner
4. TLS Quantum Attack
5. SSH Key Recovery

Select option: 1

>>> configure target
Enter RSA key file: test_rsa.pem

>>> select backend
1. qiskit_aer (Simulator - Fast)
2. ibm_quantum (Real Hardware)
3. aws_braket (AWS Quantum)
Select: 1

>>> run
[*] Executing Shor's algorithm...
```

## Configuration Examples

### Basic Configuration

Create or edit `config.ini`:

```ini
[Quantum]
default_backend = qiskit_aer
shots = 1024
optimization_level = 3

[Output]
verbose = true
log_level = INFO
output_dir = ./results

[Security]
enable_validation = true
```

### Using IBM Quantum Hardware

```bash
# Configure IBM Quantum credentials
python -c "
from qiskit_ibm_runtime import QiskitRuntimeService
QiskitRuntimeService.save_account(
    token='YOUR_IBM_QUANTUM_TOKEN',
    overwrite=True
)
"

# Run attack on real quantum hardware
python exploits/rsa_shor.py \
    --key test_rsa.pem \
    --backend ibm_quantum \
    --device ibmq_manila
```

### Using AWS Braket

```bash
# Configure AWS credentials
aws configure

# Run on AWS quantum simulator
python exploits/rsa_shor.py \
    --key test_rsa.pem \
    --backend aws_braket \
    --device amazon-sv1
```

## Understanding the Output

### Shor's Algorithm Output Explained

```
[+] Factorization successful!
[+] p = 158423...  ← First prime factor
[+] q = 159067...  ← Second prime factor

Verification:
  N = p × q 
  φ(N) = (p-1)(q-1) = 25195839968...
  d = e^(-1) mod φ(N) = 19302...
  
[+] Private key recovered!  ← Can now decrypt all messages
```

### Network Scan Output

```json
{
  "target": "192.168.1.100",
  "port": 443,
  "protocol": "TLSv1.2",
  "cipher_suite": "ECDHE-RSA-AES256-GCM-SHA384",
  "vulnerability": {
    "quantum_vulnerable": true,
    "reason": "Uses RSA-2048 (quantum-breakable)",
    "recommendation": "Migrate to CRYSTALS-Kyber"
  }
}
```

## Best Practices

### 1. Start with Simulations

Always test on simulators before using real quantum hardware:

```bash
# Good: Fast and free
--backend qiskit_aer

# Advanced: Real hardware (limited queue time)
--backend ibm_quantum
```

### 2. Use Appropriate Key Sizes

For educational purposes, use smaller keys:

| Key Size | Backend | Est. Time |
|----------|---------|-----------|
| 512-bit | qiskit_aer | 5-10 sec |
| 1024-bit | qiskit_aer | 20-30 sec |
| 2048-bit | qiskit_aer | 1-2 min |
| 2048-bit | ibm_quantum | 5-10 min |

### 3. Enable Verbose Mode

Always use `--verbose` while learning:

```bash
python exploits/rsa_shor.py --key test.pem --verbose
```

### 4. Save Results

Log results for analysis:

```bash
python exploits/rsa_shor.py \
    --key test.pem \
    --output results.json \
    --log-file attack.log
```

## Troubleshooting

### "Backend not available"

```bash
# List available backends
python -c "from quantum.backend import QuantumBackend; print(QuantumBackend.list_backends())"

# Use default simulator
--backend qiskit_aer
```

### "Insufficient qubits"

Quantum hardware has limited qubits. For large keys:

```bash
# Use simulator for large keys
--backend qiskit_aer

# Or request more qubits (IBM Quantum)
--device ibmq_qasm_simulator  # 32 qubits
```

### "Job queue timeout"

Real quantum hardware has job queues:

```bash
# Check queue status
python -c "
from qiskit_ibm_runtime import QiskitRuntimeService
service = QiskitRuntimeService()
backend = service.backend('ibmq_manila')
print(f'Queue: {backend.status().pending_jobs} jobs')
"

# Use simulator instead
--backend qiskit_aer
```

## Next Steps

### Learn More

1. **[API Reference](api/modules.rst)** - Complete framework documentation
2. **[Quantum Backends Guide](guides/quantum_backends.md)** - Platform-specific setup
3. **[Cryptanalysis Guide](guides/cryptanalysis.md)** - Advanced attack techniques
4. **[Jupyter Notebooks](../notebooks/)** - 9 comprehensive tutorials

### Join the Community

- **GitHub**: [maurorisonho/Houdinis](https://github.com/maurorisonho/Houdinis)
- **Issues**: Report bugs and request features
- **Discussions**: Ask questions and share research
- **Contributing**: [CONTRIBUTING.md](../CONTRIBUTING.md)

### Advanced Topics

- **Costm Exploits**: [Tutorial](tutorials/custom_exploits.md)
- **Multi-Backend**: [Benchmark Guide](tutorials/multi_backend.md)
- **Production Deployment**: [Infrastructure Guide](INFRASTRUCTURE_GUIDE.md)
- **Security Hardening**: [Security Guide](guides/security_best_practices.md)

## Example Projects

Try these complete projects:

### Project 1: Campus Network Assessment

```bash
# 1. Scan network
python scanners/quantum_vuln_scanner.py --target campus-network.edu

# 2. Generate report
python -c "from scanners.network_scanner import generate_report; generate_report('scan_results.json')"

# 3. Prioritize migration (output: migration_plan.pdf)
```

### Project 2: Research Paper Data Collection

```bash
# Benchmark multiple algorithms
python exploits/multi_backend_benchmark.py \
    --algorithms shors,grovers \
    --key-sizes 512,1024,2048,4096 \
    --backends qiskit_aer,ibm_quantum \
    --iterations 10 \
    --output research_data.csv

# Generate plots for paper
python scripts/plot_benchmark.py research_data.csv
```

### Project 3: Post-Quantum Migration Planning

```bash
# Analyze existing infrastructure
python scanners/ssl_scanner.py --target company.com

# Generate migration recommendations
python exploits/pq_migration_tools.py \
    --input scan_results.json \
    --output migration_plan.json

# Estimate costs
python scripts/estimate_migration_cost.py migration_plan.json
```

---

**Ready to go deeper?** Check out the [Jupyter Notebooks](../notebooks/) for comprehensive tutorials!
