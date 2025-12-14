# Pylance Configuration for Houdinis

##  Configuration Files

### `pyrightconfig.json`
Configura o Pylance/Pyright para o projeto Houdinis:
- Desabilita warnings de imports ausentes
- Adiciona caminhos extras para módulos
- Configura para Python 3.10 no Linux

### Type Stubs (`.pyi` files)
Fornecem informações de tipo para o Pylance:
- `quantum/backend.pyi` - QuantumBackendManager
- `exploits/grover_bruteforce.pyi` - GroverBruteforceExploit

### `notebooks/.vscode/settings.json`
Configuração específica para notebooks Jupyter:
- Ignora warnings de imports
- Adiciona caminhos do Houdinis ao Python path

##  Por que esses warnings aparecem?

Os notebooks Houdinis executam código de duas formas:

1. **No host (VS Code)** - Para gerenciar Docker
2. **No container Docker** - Para ataques quânticos (onde Qiskit e Houdinis estão instalados)

O Pylance analisa o código **no contexto do host**, onde:
-  `qiskit` não está instalado
-  Módulos `quantum.*` e `exploits.*` existem mas podem não estar no path

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
Fornecem assinaturas de tipo sem implementação real

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
Os warnings não afetam a execução - o código funciona perfeitamente quando executado no notebook.

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
