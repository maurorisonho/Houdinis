# Pylance Configuration for Houdinis

##  Configuration Files

### `pyrightconfig.json`
Configures Pylance/Pyright for the Houdinis project:
- Disables missing import warnings
- Adds extra paths for modules
- Configures for Python 3.10 on Linux

### Type Stubs (`.pyi` files)
Provide type information for Pylance:
- `quantum/backend.pyi` - QuantumBackendManager
- `exploits/grover_bruteforce.pyi` - GroverBruteforceExploit

### `notebooks/.vscode/settings.json`
Specific configuration for Jupyter notebooks:
- Ignores import warnings
- Adds Houdinis paths to Python path

##  Why do these warnings appear?

Houdinis notebooks execute code in two ways:

1. **On host (VS Code)** - To manage Docker
2. **In Docker container** - For quantum attacks (where Qiskit and Houdinis are installed)

Pylance analyzes code **in the host context**, where:
-  `qiskit` is not installed
-  `quantum.*` and `exploits.*` modules exist but may not be in path

##  Soluções Implementadas

### 1. Imports condicionais
```python
try:
    from qiskit import QuantumCircuit
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False
    print("Will use Docker container")
```

### 2. Type hints com `# type: ignore`
```python
from exploits.grover_bruteforce import GroverBruteforceExploit  # type: ignore
```

### 3. Type stubs (`.pyi`)
Provide type signatures without real implementation

### 4. Pylance Configuration
Disables specific warnings via `pyrightconfig.json`

##  How to use

### Option 1: Reload VS Code
```
Ctrl+Shift+P → "Developer: Reload Window"
```

### Option 2: Reload Pylance
```
Ctrl+Shift+P → "Python: Restart Language Server"
```

### Option 3: Ignore warnings
Warnings do not affect execution - code works perfectly when run in notebook.

##  Expected Result

After applying these configurations:
-  Fewer Pylance warnings
-  Type hints working where appropriate
-  Code still works 100% in Docker containers
-  Better VS Code experience

##  Referências

- [Pylance Configuration](https://github.com/microsoft/pylance-release/blob/main/TROUBLESHOOTING.md)
- [Type Stubs Guide](https://typing.readthedocs.io/en/latest/source/stubs.html)
- [Pyright Configuration](https://github.com/microsoft/pyright/blob/main/docs/configuration.md)
