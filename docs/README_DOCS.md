# Houdinis Documentation

This directory contains the complete documentation for the Houdinis Quantum Cryptanalysis Framework.

## Documentation Structure

```
docs/
 conf.py                 # Sphinx configuration
 index.md               # Documentation homepage
 introduction.md        # Framework introduction
 installation.md        # Installation guide
 quickstart.md         # Quick start tutorial
 Makefile              # Build automation
 build_docs.sh         # Build script
 requirements.txt      # Documentation dependencies

 api/                  # API Reference
    core.md          # Core module API
    quantum.md       # Quantum module API
    exploits.md      # Exploits module API
    scanners.md      # Scanners module API
    security.md      # Security module API

 guides/              # User Guides
    quantum_backends.md       # Backend configuration
    cryptanalysis.md          # Cryptanalysis techniques
    network_scanning.md       # Network scanning guide
    security_best_practices.md

 tutorials/           # Step-by-step Tutorials
     shors_algorithm.md
     grovers_algorithm.md
     multi_backend.md
     custom_exploits.md
```

## Building Documentation Locally

### Quick Build

```bash
cd docs/
./build_docs.sh
```

### Using Make

```bash
cd docs/

# Install dependencies
make install

# Build HTML documentation
make html

# Build and serve locally
make livehtml

# Clean build directory
make clean

# Check for broken links
make linkcheck
```

### Manual Build

```bash
cd docs/

# Install dependencies
pip install -r requirements.txt

# Build HTML
sphinx-build -b html . _build/html

# Open in browser
xdg-open _build/html/index.html  # Linux
open _build/html/index.html      # macOS
start _build/html/index.html     # Windows
```

## Viewing Documentation

### Local Server

```bash
cd docs/_build/html
python -m http.server 8000
# Open http://localhost:8000 in browser
```

### Online (GitHub Pages)

After pushing to main branch, documentation is automatically deployed to:
- **URL**: https://maurorisonho.github.io/Houdinis/

## Writing Documentation

### Adding New Pages

1. Create markdown file in appropriate directory:
   ```bash
   # For guides
   touch guides/new_guide.md
   
   # For tutorials
   touch tutorials/new_tutorial.md
   ```

2. Add to `index.md` table of contents:
   ```markdown
   ```{toctree}
   :maxdepth: 2
   :caption: Guides
   
   guides/new_guide
   ```
   ```

3. Rebuild documentation:
   ```bash
   make html
   ```

### Markdown Syntax

This project uses **MyST Parser** for enhanced Markdown:

#### Basic Formatting

```markdown
# Heading 1
## Heading 2
### Heading 3

**bold text**
*italic text*
`inline code`

[link text](url)
![image alt](image.png)
```

#### Code Blocks

````markdown
```python
from quantum.backend import QuantumBackend
backend = QuantumBackend("qiskit_aer")
```
````

#### Admonitions

```markdown
```{note}
This is a note admonition.
```

```{warning}
This is a warning!
```

```{tip}
Helpful tip here.
```

```{important}
Important information.
```
```

#### Tables

```markdown
| Algorithm | Complexity | Impact |
|-----------|-----------|--------|
| Shor's | O(n³) | Breaks RSA |
| Grover's | O(2^(n/2)) | Weakens AES |
```

#### Cross-References

```markdown
See [Installation Guide](installation.md) for setup.
Check the {ref}`API Reference <api-reference>` for details.
```

### API Documentation

API docs are auto-generated from Python docstrings. Use **Google-style docstrings**:

```python
def quantum_attack(target: str, backend: str = "qiskit_aer") -> dict:
    """Execute quantum cryptanalysis attack.
    
    This function performs a quantum attack on the specified target
    using the configured quantum backend.
    
    Args:
        target: Path to target key file (RSA/ECC)
        backend: Quantum backend to use (default: qiskit_aer)
            Supported: qiskit_aer, ibm_quantum, aws_braket
            
    Returns:
        dict: Attack results containing:
            - success (bool): Whether attack succeeded
            - factors (tuple): Prime factors if RSA
            - time (float): Execution time in seconds
            
    Raises:
        ValueError: If target file is invalid
        BackendError: If quantum backend fails
        
    Example:
        >>> result = quantum_attack("test.pem", "qiskit_aer")
        >>> print(result['factors'])
        (158423, 159067)
        
    Note:
        Large key sizes (>2048 bits) require significant quantum resources.
        Use simulators for testing.
        
    See Also:
        - :func:`configure_backend`: Backend configuration
        - :class:`QuantumBackend`: Backend management class
    """
    pass
```

### Building API Documentation

API docs are automatically generated:

```bash
# Generate module docs
sphinx-apidoc -o docs/api . --force --module-first

# Build with API docs included
make html
```

## Documentation Coverage

Check documentation coverage:

```bash
# Install interrogate
pip install interrogate

# Check coverage
interrogate . -vv

# Generate report
interrogate . --generate-badge docs/_static/doc_coverage.svg
```

**Current Coverage:** 96.7% (87/90 modules documented)

## Style Guide

### Writing Style

- **Tone**: Professional, educational, clear
- **Audience**: Security researchers, students, developers
- **Voice**: Active voice preferred
- **Tense**: Present tense for descriptions

### Structure

1. **Start with overview**: Brief summary paragraph
2. **Prerequisites**: List requirements/knowledge needed
3. **Step-by-step**: Clear numbered/bulleted instructions
4. **Examples**: Concrete code examples with output
5. **Troubleshooting**: Common issues and solutions
6. **Next steps**: Links to related documentation

### Code Examples

-  **Include complete examples** that users can copy-paste
-  **Show expected output** so users can verify
-  **Add comments** to explain non-obvious steps
-  **Use realistic data** (not foo/bar)
-  **Don't use placeholders** without explaining them

Example:

```python
# Good: Complete, runnable example
from quantum.backend import QuantumBackend

# Initialize Qiskit Aer simulator (no account needed)
backend = QuantumBackend("qiskit_aer")

# List available backends
print(backend.list_backends())
# Output: ['qiskit_aer', 'ibm_quantum', 'aws_braket']
```

## Continuous Integration

Documentation is automatically:

1. **Built** on every push to `main`/`develop`
2. **Tested** for broken links
3. **Deployed** to GitHub Pages (main branch only)
4. **Coverage checked** with interrogate

See `.github/workflows/docs.yml` for CI/CD configuration.

## Documentation Checklist

Before committing documentation changes:

- [ ] Builds successfully (`make html`)
- [ ] No Sphinx warnings
- [ ] Links work (`make linkcheck`)
- [ ] Code examples tested
- [ ] Spelling checked
- [ ] Images optimized (<100KB each)
- [ ] Cross-references valid
- [ ] Mobile-responsive (check narrow width)

## Getting Help

- **Sphinx Docs**: https://www.sphinx-doc.org/
- **MyST Parser**: https://myst-parser.readthedocs.io/
- **RTD Theme**: https://sphinx-rtd-theme.readthedocs.io/
- **Project Issues**: https://github.com/maurorisonho/Houdinis/issues

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines.

Documentation contributions are highly valued! Areas needing help:

- [ ] API reference completion
- [ ] More tutorials/examples
- [ ] Video tutorials
- [ ] Translations (PT-BR, ES, ZH)
- [ ] Interactive examples
- [ ] Diagram creation

---

**Questions?** Open an issue or discussion on GitHub!
