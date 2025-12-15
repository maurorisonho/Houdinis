# Houdinis Framework - Quantum Cryptography Testing Platform

![Houdinis Logo](https://img.shields.io/badge/Houdinis-Framework-blue?style=for-the-badge&logo=quantum)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/maurorisonho/Houdinis/main?labpath=notebooks%2Fplayground.ipynb)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

** Available in:** [English](README.md) | [Português](README.pt-BR.md) | [Español](README.es.md) | [](README.zh.md)

Houdinis is a comprehensive quantum cryptography exploitation framework designed for security researchers, penetration testers, and quantum computing enthusiasts. The framework provides tools to test quantum algorithms, evaluate cryptographic vulnerabilities, and benchmark quantum computing backends.

##  Try It Now - Zero Installation!

**Experience Houdinis in your browser without installing anything:**

[![Launch Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/maurorisonho/Houdinis/main?labpath=notebooks%2Fplayground.ipynb)

 Click to start an interactive 5-minute tutorial with:
-  Live quantum circuit execution
-  Grover's algorithm demo
-  RSA security analysis
-  Interactive visualizations

*Runs completely in your browser powered by [MyBinder.org](https://mybinder.org/)*

## Documentation

** [Official Documentation](https://maurorisonho.github.io/Houdinis/)** - Complete API documentation and user guides  
** [Quick Start Guide](docs/quickstart.md)** - Get started in 10 minutes  
** [Installation Guide](docs/installation.md)** - Multi-platform installation instructions  
** [Introduction](docs/introduction.md)** - Framework overview and concepts

**Additional Documentation:**
- [Complete Documentation Index](docs/README.md) - Comprehensive documentation index  
- [Docker Guide](docs/DOCKER_README.md) - Containerization with Rocky Linux 9  
- [Implementation Details](docs/IMPLEMENTATION_SUMMARY.md) - Technical implementation guide  
- [Backend Support](docs/BACKENDS.md) - Quantum computing platforms supported  
- [Documentation Guide](docs/README_DOCS.md) - For contributors to documentation

## Key Features

### Multi-Backend Quantum Computing Support
- **IBM Quantum Experience** - Access to real quantum hardware and cloud simulators
- **NVIDIA cuQuantum** - GPU-accelerated quantum circuit simulation
- **Amazon Braket** - AWS quantum computing service with multiple hardware providers
- **Microsoft Azure Quantum** - Enterprise quantum cloud platform
- **Google Cirq** - Research-oriented quantum computing framework
- **PennyLane** - Quantum machine learning and optimization

### Quantum Cryptography Exploits
- **Shor's Algorithm** - RSA and ECC key factorization
- **Grover's Algorithm** - Symmetric key brute force acceleration
- **Quantum Network Scanning** - Identify quantum-vulnerable systems
- **Post-Quantum Migration Tools** - Assess cryptographic transition needs
- **TLS/SSL Quantum Assessment** - Evaluate transport layer security

### Advanced Capabilities
- **Multi-platform benchmarking** - Compare performance across backends
- **NISQ algorithm optimization** - Noisy Intermediate-Scale Quantum device support
- **Quantum machine learning** - Cryptanalysis using QML techniques
- **Harvest Now, Decrypt Later** - Future quantum threat assessment

##  Installation

###  Option 1: Try in Browser (Recommended for Learning)

**Zero installation required!** Launch an interactive environment:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/maurorisonho/Houdinis/main?labpath=notebooks%2Fplayground.ipynb)

Perfect for:
- Learning quantum cryptography
- Testing small quantum circuits
- Exploring framework features
- Quick demos and prototyping

###  Option 2: Local Installation

For production use and full features:

```bash
git clone https://github.com/maurorisonho/Houdinis.git
cd Houdinis
pip install -r requirements.txt
python main.py
```

### Dependencies
```bash
# Core quantum computing libraries
pip install qiskit qiskit-aer qiskit-ibmq-provider
pip install cirq pennylane

# Cloud platform SDKs  
pip install amazon-braket-sdk azure-quantum
pip install cuquantum-python  # Requires NVIDIA GPU

# Framework dependencies
pip install numpy scipy matplotlib networkx
pip install cryptography paramiko requests
```

##  Testing

Teste a instalação e funcionalidade básica do framework:

```bash
# Teste principal do framework
python3 tests/test_houdinis.py

# Ou usando pytest (se instalado)
pytest tests/
```

### Docker Tests
```bash
# Quick access from project root
./docker-run.sh test
./setup-docker.sh
./build-docker.sh

# Or from docker directory
cd docker/
./docker-manager.sh test
./run-docker.sh --test

# Or with Docker Compose
cd docker/
./docker.sh compose-test
```

### Complete Test Documentation
For detailed information about tests, structure, debugging and contributions, see:
**[`tests/README.md`](tests/README.md)** - Complete test documentation

## Quick Start Guide

### 1. Basic Framework Usage
```python
from core.session import Session
from core.cli import CLI

# Initialize Houdinis session
cli = CLI()

### Documentação Completa de Testes
Para informações detalhadas sobre testes, estrutura, debugging e contribuições, consulte:
**[`tests/README.md`](tests/README.md)** - Documentação completa de testes

##  Quick Start Guide

### 1. Basic Framework Usage
```python
from core.session import Session
from core.cli import CLI

# Initialize Houdinis session
cli = CLI()
cli.start()

# Load quantum modules
use auxiliary/quantum_config
use exploits/rsa_shor
```

### 2. Configure Quantum Backend
```bash
# IBM Quantum configuration
houdinis> use auxiliary/quantum_config
houdinis> set BACKEND ibm_quantum
houdinis> set TOKEN your_ibm_token_here
houdinis> run

# NVIDIA cuQuantum configuration  
houdinis> set BACKEND nvidia_cuquantum
houdinis> set GPU_DEVICE 0
houdinis> run
```

### 3. Run Quantum Exploit
```bash
# Shor's algorithm RSA factorization
houdinis> use exploits/rsa_shor
houdinis> set TARGET_NUMBER 15
houdinis> set BACKEND ibmq_qasm_simulator
houdinis> run

# Grover's algorithm brute force
houdinis> use exploits/grover_bruteforce
houdinis> set TARGET_KEY_SIZE 64
houdinis> set BACKEND nvidia_cuquantum
houdinis> run
```

### 4. Multi-Backend Benchmarking
```bash
# Compare algorithm performance across backends
houdinis> use exploits/multi_backend_benchmark
houdinis> set ALGORITHM shor
houdinis> set QUBITS 8
houdinis> set BACKENDS all
houdinis> set RUNS 5
houdinis> run
```

##  Module Reference

### Core Modules

#### `auxiliary/quantum_config`
Multi-platform quantum backend configuration module.

**Options:**
- `BACKEND`: Target quantum computing platform
- `TOKEN`: Authentication token for cloud services
- `HUB/GROUP/PROJECT`: IBM Quantum access parameters
- `DEVICE_ID`: Specific quantum device selection

**Supported Backends:**
- `ibm_quantum` - IBM Quantum Experience
- `nvidia_cuquantum` - NVIDIA GPU simulation
- `amazon_braket` - AWS Braket service
- `azure_quantum` - Microsoft Azure Quantum
- `google_cirq` - Google quantum computing
- `pennylane` - Quantum ML platform

### Exploitation Modules

#### `exploits/rsa_shor`
Implements Shor's algorithm for RSA key factorization.

**Options:**
- `TARGET_NUMBER`: Number to factorize (default: 15)
- `BACKEND`: Quantum backend to use
- `QUBITS`: Number of qubits (auto-calculated)
- `SHOTS`: Measurement repetitions (default: 1024)

#### `exploits/grover_bruteforce`
Grover's algorithm for symmetric key brute force.

**Options:**
- `TARGET_KEY_SIZE`: Key size in bits (default: 64)
- `SEARCH_SPACE`: Search space size (default: 2^16)
- `ORACLE_TYPE`: Oracle implementation type
- `ITERATIONS`: Grover iterations (auto-calculated)

#### `exploits/multi_backend_benchmark`
Performance comparison across quantum backends.

**Options:**
- `ALGORITHM`: Algorithm to benchmark (shor, grover, qft, vqe)
- `QUBITS`: Circuit size (default: 4)
- `BACKENDS`: Backends to test (default: all)
- `RUNS`: Benchmark runs per backend (default: 3)
- `SAVE_RESULTS`: Save results to JSON file

### Network Scanning Modules

#### `scanners/quantum_vuln_scanner`
Identifies systems vulnerable to quantum attacks.

**Options:**
- `TARGET`: Target network or host
- `CHECK_TLS`: Scan TLS/SSL configurations
- `CHECK_SSH`: Analyze SSH key algorithms
- `QUANTUM_TIMELINE`: Years until quantum threat (default: 15)

#### `scanners/network_scanner`
General network reconnaissance with quantum awareness.

**Options:**
- `TARGET`: Target network range
- `PORTS`: Ports to scan (default: common)
- `CRYPTO_ANALYSIS`: Perform cryptographic analysis
- `OUTPUT_FORMAT`: Report format (json, xml, txt)

### Utility Modules

#### `payloads/decrypt_tls`
TLS/SSL quantum decryption simulation.

#### `utils/banner`
Framework banner and version information.

##  Backend Comparison

| Backend | Type | Performance | Cost | Use Case |
|---------|------|-------------|------|----------|
| IBM Quantum | Real Hardware | Medium | Free Tier | Research, Education |
| NVIDIA cuQuantum | GPU Simulation | Very High | Local GPU | Large Simulations |
| Amazon Braket | Cloud | High | Pay-per-use | Production, Hybrid |
| Azure Quantum | Cloud | High | Enterprise | Business Applications |
| Google Cirq | Simulation | Medium | Free | Algorithm Development |

### Performance Benchmarks (Sample)

| Algorithm | IBM Quantum | NVIDIA cuQuantum | Amazon Braket | Azure Quantum |
|-----------|-------------|------------------|---------------|---------------|
| Shor (8 qubits) | 45.2s | 2.1s | 12.7s | 18.3s |
| Grover (6 qubits) | 32.1s | 1.3s | 8.9s | 14.2s |
| QFT (5 qubits) | 28.5s | 0.8s | 6.2s | 9.7s |

##  Documentation

### Notebooks Directory
Comprehensive Jupyter notebooks with detailed examples:

- `Shors_Algorithm_RSA_Exploitation.ipynb` - RSA factorization tutorial
- `Grovers_Algorithm_Symmetric_Key_Attacks.ipynb` - Symmetric key attacks
- `Post_Quantum_Cryptography_Analysis.ipynb` - PQC migration guide
- `Quantum_Machine_Learning_Cryptanalysis.ipynb` - QML techniques
- `Multi_Backend_Performance_Comparison.ipynb` - Backend benchmarking

### Configuration Files

#### `config.ini`
Main framework configuration:
```ini
[DEFAULT]
framework_name = Houdinis
version = 1.0.0
author = Mauro Risonho de Paula Assumpção aka firebitsbr

[quantum]
default_backend = ibm_quantum
max_qubits = 20
default_shots = 1024

[security]
enable_logging = true
log_level = INFO
```

## [SECURITY] Security Considerations

### Responsible Use
This framework is designed for:
- **Security research** and vulnerability assessment
- **Educational purposes** and quantum computing learning
- **Cryptographic analysis** and post-quantum migration planning
- **Algorithm benchmarking** and performance evaluation

### Ethical Guidelines
- Only test systems you own or have explicit permission to test
- Respect cloud platform terms of service and usage limits
- Use findings to improve security, not to cause harm
- Report vulnerabilities responsibly through proper channels

### Legal Disclaimer
Users are responsible for complying with applicable laws and regulations. The authors assume no liability for misuse of this framework.

##  Contributing

### Development Setup
```bash
git clone https://github.com/firebitsbr/Houdinis.git
cd Houdinis
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Run tests
python -m pytest tests/

# Code formatting
black . && flake8 .
```

### Contribution Guidelines
1. Fork the repository
2. Create a feature branch
3. Implement your changes with tests
4. Ensure code quality (black, flake8, mypy)
5. Submit a pull request with detailed description

### Adding New Backends
1. Implement backend class in `quantum/backend.py`
2. Add configuration support in `auxiliary/quantum_config.py`
3. Update `requirements.txt` with new dependencies
4. Add documentation to `BACKENDS.md`
5. Include example in demo scripts

##  License

MIT License

Copyright (c) 2025 Mauro Risonho de Paula Assumpção aka firebitsbr

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

##  Acknowledgments

- **IBM Quantum Team** - Qiskit and quantum computing access
- **NVIDIA** - cuQuantum GPU acceleration
- **Amazon Web Services** - Braket quantum computing service
- **Microsoft** - Azure Quantum platform
- **Google** - Cirq quantum computing framework
- **Xanadu** - PennyLane quantum machine learning
- **Quantum Computing Community** - Research and collaboration
- **Claude Code** for AI-assisted development and code optimization

##  CI/CD & Infrastructure

### Automated Testing (GitHub Actions)
[![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=github-actions)](https://github.com/firebitsbr/Houdinis/actions)

** O que funciona automaticamente:**
- Lint & Code Quality (Black, flake8, Pyright)
- Security Scanning (Bandit, Safety, Trivy)
- Automated Tests (pytest em 3 versões Python, 3 SOs)
- Docker Builds
- Package Building
- Coverage Reports (Codecov)

** Requer configuração simples (5 minutos):**
- PyPI Publishing: Requer `PYPI_API_TOKEN` secret
- [Ver guia completo de configuração](.github/README.md)

** Documentação:**
- [GitHub Actions Pipeline](.github/README.md) - Detalhes do CI/CD
- [Infrastructure Guide](docs/INFRASTRUCTURE_GUIDE.md) - Deploy em cloud e custos

### Status Atual
```
Desenvolvimento:   FUNCIONAL (sem configuração)
PyPI Publishing:    OPCIONAL (requer token)
Cloud Deploy:      NÃO CONFIGURADO (requer infraestrutura paga)
Quantum Hardware:  NÃO CONFIGURADO (requer acesso)
```

##  Code Quality

### Current Score: 8.6/10 
[![Type Hints](https://img.shields.io/badge/Type%20Hints-75.3%25-yellow)](docs/CODE_QUALITY_PLAN.md)
[![Docstrings](https://img.shields.io/badge/Docstrings-97.2%25-brightgreen)](docs/CODE_QUALITY_PLAN.md)
[![Pylance](https://img.shields.io/badge/Pylance-8.6%2F10-yellow)](docs/CODE_QUALITY_PLAN.md)

**Metrics:**
-  **397 functions** analyzed
-  **75.3% type coverage** (299/397 functions)
-  **97.2% docstring coverage** (386/397 functions)
-  **0 unused imports**

**Tools:**
```bash
# Validate code quality
python scripts/check_quality.py

# Type checking
pyright .

# Auto-format
black . && isort .
```

** Documentation:**
- [Code Quality Plan](docs/CODE_QUALITY_PLAN.md) - Roadmap to 9.5/10
- [Quality Script](scripts/check_quality.py) - Automated validation

##  Support

- **GitHub Issues**: [Report bugs and feature requests](https://github.com/firebitsbr/Houdinis/issues)
- **Discussions**: [Community discussions and Q&A](https://github.com/firebitsbr/Houdinis/discussions)
- **Email**: mauro.risonho@gmail.com
- **Twitter**: [@firebitsbr](https://twitter.com/firebitsbr)

---

 **Houdinis Framework** - Making quantum cryptography testing accessible to everyone.

*"Any sufficiently advanced cryptography is indistinguishable from magic... until quantum computers arrive."*
