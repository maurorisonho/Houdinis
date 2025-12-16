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
Fornecem assinaturas de tipo sem implementation real

### 4. Configuração do Pylance
Desabilita warnings específicos via `pyrightconfig.json`

##  Como usar

### Opção 1: Recarregar VS Code
```
Ctrl+Shift+P → "Developer: Reload Window"
```

### Opção 2: Recarregar Pylance
```
Ctrl+Shift+P → "Python: Restart Language Server"
```

### Opção 3: Ignorar warnings
Os warnings não afetam a execution - o código funciona perfeitamente quando executado no notebook.

##  Resultado Esperado

Após aplicar essas configurações:
-  Menos warnings do Pylance
-  Type hints funcionando onde apropriado
-  Código ainda funciona 100% nos containers Docker
-  Melhor experiência no VS Code

##  Referências

- [Pylance Configuration](https://github.com/microsoft/pylance-release/blob/main/TROUBLESHOOTING.md)
- [Type Stubs Guide](https://typing.readthedocs.io/en/latest/source/stubs.html)
- [Pyright Configuration](https://github.com/microsoft/pyright/blob/main/docs/configuration.md)
