# Installation Guide

This guide covers multiple installation methods for the Houdinis Framework, from quick local setup to production deployments.

## Prerequisites

### System Requirements

- **Operating System**: Linux (Ubuntu 20.04+, Debian 11+), macOS 11+, Windows 10/11 (WSL2)
- **Python**: 3.10 or higher (3.11 recommended)
- **Memory**: Minimum 8GB RAM (16GB+ recommended for quantum simulations)
- **Storage**: 5GB free disk space

### Required Software

```bash
# Python and pip
python3 --version  # Should be 3.10+
pip3 --version

# Git
git --version

# (Optional) Docker
docker --version
docker-compose --version
```

## Installation Methods

### Method 1: Quick Install (Recommended)

For most users, this is the fastest way to get started:

```bash
# Clone the repository
git clone https://github.com/maurorisonho/Houdinis.git
cd Houdinis

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python main.py --help
```

### Method 2: Development Install

For contributors and developers:

```bash
# Clone the repository
git clone https://github.com/maurorisonho/Houdinis.git
cd Houdinis

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests to verify
pytest tests/
```

### Method 3: Docker (Isolated Environment)

For containerized deployment:

```bash
# Clone the repository
git clone https://github.com/maurorisonho/Houdinis.git
cd Houdinis

# Build Docker image
docker-compose build

# Run container
docker-compose up -d

# Access shell in container
docker exec -it houdinis_container bash
```

See [docker/README.md](../docker/README.md) for detailed Docker instructions.

### Method 4: Production Deployment

For Kubernetes/cloud deployments, see:
- [INFRASTRUCTURE_GUIDE.md](INFRASTRUCTURE_GUIDE.md) - Complete cloud deployment guide
- [deploy/README.md](../deploy/README.md) - Kubernetes manifests

## Platform-Specific Instructions

### Ubuntu/Debian

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.11 python3.11-venv python3-pip git

# Install Houdinis
git clone https://github.com/maurorisonho/Houdinis.git
cd Houdinis
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### macOS

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and Git
brew install python@3.11 git

# Install Houdinis
git clone https://github.com/maurorisonho/Houdinis.git
cd Houdinis
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows (WSL2)

```powershell
# Enable WSL2 (PowerShell as Administrator)
wsl --install -d Ubuntu-22.04

# Restart computer, then open Ubuntu terminal
# Follow Ubuntu/Debian instructions above
```

## Quantum Backend Configuration

### IBM Quantum

1. Create account at [quantum-computing.ibm.com](https://quantum-computing.ibm.com/)
2. Get your API token from account settings
3. Configure Houdinis:

```bash
# Save token securely
python -c "from qiskit_ibm_runtime import QiskitRuntimeService; QiskitRuntimeService.save_account(token='YOUR_TOKEN_HERE')"

# Or use config file
cat > config.ini << EOF
[IBM]
token = YOUR_TOKEN_HERE
hub = ibm-q
group = open
project = main
EOF
```

### AWS Braket

```bash
# Install AWS CLI
pip install awscli

# Configure AWS credentials
aws configure
# Enter: Access Key ID, Secret Access Key, Region (us-east-1)

# Verify access
aws braket get-device --device-arn arn:aws:braket:::device/quantum-simulator/amazon/sv1
```

### Local Simulators (No Account Required)

The following simulators work out of the box:
- **Qiskit Aer** (included in requirements.txt)
- **Cirq** (optional: `pip install cirq`)
- **ProjectQ** (optional: `pip install projectq`)

## Verification

### Basic Functionality Test

```bash
# Test CLI
python main.py --help

# Test quantum backend
python -c "from quantum.backend import QuantumBackend; print(QuantumBackend.list_backends())"

# Run basic exploit
python exploits/quantum_rng.py
```

### Full Test Suite

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_houdinis.py::test_quantum_backend

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

### Interactive Notebook Test

```bash
# Install Jupyter (if not already installed)
pip install jupyter

# Launch notebook server
jupyter notebook notebooks/

# Open and run: Shors_Algorithm_RSA_Exploitation.ipynb
```

## Configuration

### Main Configuration File

Edit `config.ini`:

```ini
[DEFAULT]
log_level = INFO
output_dir = ./output

[Quantum]
default_backend = qiskit_aer
shots = 1024
optimization_level = 3

[Security]
enable_input_validation = true
max_key_size = 4096
allowed_ciphers = AES,ChaCha20

[Network]
timeout = 30
max_threads = 10
```

### Environment Variables

```bash
# Set quantum backend
export HOUDINIS_BACKEND=ibm_quantum

# Set log level
export HOUDINIS_LOG_LEVEL=DEBUG

# Set output directory
export HOUDINIS_OUTPUT_DIR=/tmp/houdinis_results
```

## Troubleshooting

### Common Issues

#### Import Error: No module named 'qiskit'

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### IBM Quantum Token Error

```bash
# Delete saved account and reconfigure
rm -rf ~/.qiskit/qiskitrc.json
python -c "from qiskit_ibm_runtime import QiskitRuntimeService; QiskitRuntimeService.save_account(token='YOUR_TOKEN')"
```

#### Permission Denied on Linux

```bash
# Fix permissions
chmod +x main.py
chmod +x docker/*.sh
```

#### Docker Build Fails

```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

### Getting Help

If you encounter issues:

1. **Check Documentation**: Review [README.md](../README.md) and [BACKENDS.md](BACKENDS.md)
2. **Search Issues**: Check [GitHub Issues](https://github.com/maurorisonho/Houdinis/issues)
3. **Run Diagnostics**: `python scripts/check_quality.py`
4. **Ask for Help**: Open a new GitHub issue with:
   - Python version: `python --version`
   - OS information: `uname -a` (Linux/macOS)
   - Error messages and logs
   - Steps to reproduce

## Next Steps

Once installation is complete:

1. **[Quick Start Tutorial](quickstart.md)** - Run your first quantum attack
2. **[Quantum Backends Guide](guides/quantum_backends.md)** - Configure quantum platforms
3. **[API Reference](api/modules.rst)** - Explore the framework
4. **[Jupyter Notebooks](../notebooks/)** - Interactive tutorials

---

**Need Help?** Check the [Troubleshooting](#troubleshooting) section or open a [GitHub Issue](https://github.com/maurorisonho/Houdinis/issues).
