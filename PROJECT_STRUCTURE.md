# Houdinis Project Structure

> **Developed by:** Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)

This document provides an overview of the Houdinis Framework project structure after organization.

##  Root Directory Structure

```
Houdinis/
  Core Files
    main.py                 # Main entry point
    setup.py               # Package setup configuration
    config.ini             # Configuration file
    requirements.txt       # Python dependencies
    pytest.ini             # Testing configuration
    pyrightconfig.json     # Python type checking config

  Documentation
    README.md              # Main README (English)
    README.pt-BR.md        # Portuguese documentation
    README.es.md           # Spanish documentation
    README.zh.md           # Chinese documentation
    LICENSE                # MIT License
    CODE_OF_CONDUCT.md     # Community guidelines
    CONTRIBUTING.md        # Contribution guide

  Source Code
    core/                  # Core framework modules
    quantum/               # Quantum computing backends
    exploits/              # Quantum attack modules
    scanners/              # Vulnerability scanners
    security/              # Security validation
    payloads/              # Attack payloads
    utils/                 # Utility functions
    auxiliary/             # Auxiliary modules

  Testing
    tests/                 # Test suites
    .pytest_cache/         # Pytest cache

  Documentation (Extended)
    docs/                  # Comprehensive documentation
    notebooks/             # Jupyter notebooks
    binder/                # Binder configuration

  Interactive Playground
    playground/            # Web-based quantum playground

  Docker & Deployment
    docker/                # Main Docker configurations
    deploy/                # Deployment scripts
    .docker-files/         # Docker helper scripts 

  Development & CI/CD
    .github/               # GitHub Actions workflows
    scripts/               # Build and automation scripts
    metrics/               # Code metrics
    monitoring/            # Monitoring tools

  Development Tools
    .tools/                # Dev utilities & scripts 

  Reports & Analysis
    .reports/              # Generated reports & logs 

  Archives
    .legacy/               # Deprecated files 
    .backups/              # Backup files
    videos/                # Video content

  Hidden System Files
     .git/                  # Git repository
     .venv/                 # Python virtual environment
     .coverage              # Coverage data
     .benchmarks/           # Benchmark results
     coverage_html/         # HTML coverage reports
```

##  New Organizational Directories

These directories were created to better organize the project:

### `.tools/` - Development Tools
Contains utility scripts for development tasks:
- Header management scripts
- Code cleanup utilities
- Git utilities
- Testing scripts

[View README](.tools/README.md)

### `.reports/` - Reports & Logs
Contains generated reports and logs:
- Performance reports
- Analysis results
- Translation reports
- Build logs

[View README](.reports/README.md)

### `.docker-files/` - Docker Scripts
Contains Docker-related shell scripts:
- Build scripts
- Run scripts
- Setup scripts

[View README](.docker-files/README.md)

### `.legacy/` - Deprecated Files
Contains archived and deprecated files:
- Old git scripts
- Archived documentation
- Historical references

[View README](.legacy/README.md)

##  Key Directories Explained

### Core Application

| Directory | Purpose |
|-----------|---------|
| `core/` | Core framework functionality (CLI, modules, sessions) |
| `quantum/` | Quantum backend integrations (IBM, NVIDIA, AWS, etc.) |
| `exploits/` | Quantum cryptanalysis attack implementations |
| `scanners/` | Network and cryptographic vulnerability scanners |
| `security/` | Security validation and configuration |

### Development & Testing

| Directory | Purpose |
|-----------|---------|
| `tests/` | Unit tests, integration tests, benchmarks |
| `scripts/` | Build automation and maintenance scripts |
| `notebooks/` | Interactive Jupyter notebooks and tutorials |

### Deployment

| Directory | Purpose |
|-----------|---------|
| `docker/` | Docker configurations (Dockerfile, compose) |
| `deploy/` | Deployment automation scripts |
| `playground/` | Web-based interactive playground |

### Documentation

| Directory | Purpose |
|-----------|---------|
| `docs/` | Comprehensive project documentation |
| `binder/` | MyBinder.org configuration |

##  Getting Started

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run main application
python main.py

# Run tests
pytest tests/
```

### Development Setup
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Install dev dependencies
pip install -r requirements.txt

# Run in development mode
python main.py --dev
```

### Docker Setup
```bash
# Build Docker image
bash .docker-files/build-docker.sh

# Run in container
bash .docker-files/docker-run.sh
```

##  Documentation Links

- **Main Documentation**: [docs/README.md](docs/README.md)
- **API Documentation**: [docs/API.md](docs/API.md)
- **Installation Guide**: [docs/installation.md](docs/installation.md)
- **Docker Guide**: [docker/README.md](docker/README.md)
- **Playground Guide**: [playground/README.md](playground/README.md)

##  Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to this project.

##  License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

---

**Last Updated:** December 15, 2025
**Project Version:** 1.0.0
**Framework:** Houdinis - Quantum Cryptography Testing Platform
