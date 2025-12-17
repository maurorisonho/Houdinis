# Contributing to Houdinis Framework

Thank you for your interest in contributing to Houdinis! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Security](#security)
- [Community](#community)

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Docker and Docker Compose
- Git
- Basic understanding of quantum computing concepts
- Familiarity with cryptography

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Houdinis.git
   cd Houdinis
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/maurorisonho/Houdinis.git
   ```

## Development Environment

### Setup Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black isort mypy bandit
```

### Configure Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Setup hooks
pre-commit install
```

### Docker Development

```bash
# Build Docker images
cd docker
docker-compose build

# Run containers
docker-compose up -d

# Access the framework
docker exec -it houdinis_framework bash
```

## How to Contribute

### Types of Contributions

We welcome various types of contributions:

1. **Bug Reports** - Report issues you encounter
2. **Feature Requests** - Suggest new features or improvements
3. **Code Contributions** - Fix bugs or implement features
4. **Documentation** - Improve docs, add examples, write tutorials
5. **Testing** - Write tests, improve test coverage
6. **Quantum Algorithms** - Implement new quantum algorithms
7. **Cryptanalysis Modules** - Add new exploit modules

### Reporting Bugs

Before creating a bug report:
- Check existing issues to avoid duplicates
- Collect relevant information (OS, Python version, error messages)

Use the bug report template when creating an issue:
- Clear, descriptive title
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Logs or screenshots if applicable

### Suggesting Features

When suggesting features:
- Check if feature already exists or is planned
- Describe the problem it solves
- Explain the proposed solution
- Consider implementation complexity
- Discuss alternatives

## Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

```python
# Maximum line length: 100 characters
# Use 4 spaces for indentation (no tabs)
# Use double quotes for strings
# Use type hints for function signatures

def example_function(param: str, value: int = 10) -> bool:
    """
    Brief description of function.
    
    Args:
        param: Description of param
        value: Description of value with default
    
    Returns:
        Description of return value
    """
    return True
```

### Code Formatting

```bash
# Format code with Black
black .

# Sort imports with isort
isort .

# Type checking with Pyright
pyright .
```

### Naming Conventions

- **Classes**: PascalCase (`QuantumModule`, `RSAShor`)
- **Functions/Methods**: snake_case (`calculate_phase`, `run_exploit`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_QUBITS`, `DEFAULT_BACKEND`)
- **Private members**: Prefix with underscore (`_internal_method`)

### Documentation

All public APIs must include docstrings:

```python
class QuantumExploit:
    """
    Base class for quantum cryptanalysis exploits.
    
    This class provides the foundation for implementing quantum algorithms
    that can be used to break classical cryptographic systems.
    
    Attributes:
        backend: Quantum backend to use for execution
        qubits: Number of qubits required
    
    Example:
        >>> exploit = QuantumExploit(backend='ibm_quantum')
        >>> result = exploit.run(target='192.168.1.1')
    """
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_cli.py

# Run with coverage
pytest --cov=. --cov-report=html

# Run only unit tests
pytest tests/unit/ -v

# Run integration tests (slower)
pytest tests/integration/ -v
```

### Writing Tests

All new code should include tests:

```python
# tests/unit/test_new_feature.py
import pytest
from your_module import YourClass

class TestYourClass:
    """Test suite for YourClass"""
    
    @pytest.fixture
    def instance(self):
        """Create instance for testing"""
        return YourClass()
    
    def test_basic_functionality(self, instance):
        """Test basic functionality"""
        result = instance.method()
        assert result == expected_value
    
    @pytest.mark.security
    def test_security_validation(self, instance):
        """Test security features"""
        # Test security-related functionality
        pass
```

### Test Coverage Requirements

- Unit tests: Minimum 60% coverage
- Integration tests: Major user flows
- Security tests: All security-critical code
- Edge cases: Boundary conditions, error handling

## Pull Request Process

### Before Submitting

1. **Create a branch**:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

2. **Make your changes**:
   - Follow coding standards
   - Add tests
   - Update documentation
   - Run tests locally

3. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: Add quantum Grover optimizer
   
   - Implement optimized Grover's algorithm
   - Add benchmarks for different input sizes
   - Update documentation with usage examples"
   ```

### Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Adding or updating tests
- `refactor:` Code refactoring
- `perf:` Performance improvements
- `security:` Security fixes
- `ci:` CI/CD changes

### Submitting Pull Request

1. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request** on GitHub:
   - Use a clear, descriptive title
   - Fill out the PR template completely
   - Link related issues
   - Add screenshots/demos if applicable
   - Request reviews from maintainers

3. **Address review feedback**:
   - Respond to comments
   - Make requested changes
   - Push updates to your branch

4. **Merge requirements**:
   - All tests pass
   - Code coverage maintained/improved
   - Security scans pass
   - At least one approval from maintainer
   - No merge conflicts

## Security

### Responsible Disclosure

**DO NOT** open public issues for security vulnerabilities!

Instead:
1. Use [GitHub Security Advisories](https://github.com/maurorisonho/Houdinis/security/advisories/new) (private reporting)
2. Provide detailed description
3. Include proof of concept if possible
4. Wait for response before public disclosure

### Security Considerations

When contributing:
- Never commit secrets, API keys, or credentials
- Validate all user inputs
- Use secure coding practices
- Follow OWASP guidelines
- Test for common vulnerabilities

## Community

### Getting Help

- **Documentation**: Read the [docs/](docs/) directory
- **Discussions**: GitHub Discussions for questions
- **Discord**: Join our Discord server (link in README)
- **Email**: houdinis@example.com

### Recognition

Contributors are recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation
- Special mentions for significant contributions

### Areas Needing Help

Check issues labeled:
- `good first issue` - Great for newcomers
- `help wanted` - Need community assistance
- `documentation` - Docs improvements needed
- `testing` - Test coverage needed
- `enhancement` - Feature implementations

## Development Workflow

### 1. Pick an Issue

- Browse open issues
- Comment to claim an issue
- Ask for clarification if needed

### 2. Develop

- Create feature branch
- Write code and tests
- Run local tests
- Update documentation

### 3. Submit

- Push changes
- Create pull request
- Respond to feedback
- Iterate until approved

### 4. Celebrate

- Your contribution is merged!
- Thank you for making Houdinis better!

## Additional Resources

- [Qiskit Documentation](https://qiskit.org/documentation/)
- [Quantum Computing for Beginners](https://quantum-computing.ibm.com/)
- [NIST Post-Quantum Cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography)
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)

---

## Questions?

Don't hesitate to ask! We're here to help.

Thank you for contributing to Houdinis Framework! 
