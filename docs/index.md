# Houdinis Framework Documentation

Welcome to the comprehensive documentation for the **Houdinis Quantum Cryptanalysis Framework** - a powerful educational and research platform for exploring quantum computing's impact on modern cryptography.

```{toctree}
:maxdepth: 2
:caption: Getting Started

introduction
installation
quickstart
```

```{toctree}
:maxdepth: 2
:caption: Core Modules

api/core
api/quantum
api/exploits
api/scanners
api/security
```

```{toctree}
:maxdepth: 2
:caption: User Guides

guides/quantum_backends
guides/cryptanalysis
guides/network_scanning
guides/security_best_practices
```

```{toctree}
:maxdepth: 2
:caption: Tutorials

tutorials/shors_algorithm
tutorials/grovers_algorithm
tutorials/multi_backend
tutorials/custom_exploits
```

```{toctree}
:maxdepth: 2
:caption: Reference

api/modules
configuration
cli_reference
```

```{toctree}
:maxdepth: 1
:caption: Development

contributing
code_quality
testing
security_audit
changelog
```

## Overview

Houdinis is a comprehensive framework designed for:

- **Educational Research**: Demonstrate quantum computing's impact on cryptography
- **Security Assessment**: Evaluate cryptographic vulnerabilities in post-quantum era
- **Algorithm Implementation**: Practical implementations of Shor's and Grover's algorithms
- **Multi-Backend Support**: IBM Quantum, AWS Braket, Qiskit Aer, and more

## Features

### Quantum Algorithms
- Shor's Algorithm for RSA/ECC factorization
- Grover's Algorithm for symmetric key attacks
- Quantum network reconnaissance
- HNDL (Harvest Now, Decrypt Later) attack simulations

### Cryptanalysis Targets
- RSA/ECDSA key recovery
- AES/3DES vulnerability assessment
- TLS/IPsec quantum attacks
- SSH/IKE protocol analysis
- PGP key cracking

### Enterprise Features
- Multi-backend quantum computing support
- Docker containerization
- Kubernetes deployment
- CI/CD integration
- Comprehensive security framework

## Quick Links

- [GitHub Repository](https://github.com/maurorisonho/Houdinis)
- [Installation Guide](installation.md)
- [Quick Start Tutorial](quickstart.md)
- [API Reference](api/modules.rst)
- [Contributing Guide](contributing.md)

## Indices and tables

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search`
