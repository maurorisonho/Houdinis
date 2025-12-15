"""
# Houdinis Framework - Module management system for Houdinis.
# Author: Mauro Risonho de Paula Assumpção aka firebitsbr
# Desenvolvido: Lógica e Codificação por Humano e AI Assistida (Claude Sonnet 4.5)
# License: MIT

Handles loading, registration, and execution of scanner, exploit, and payload modules.
"""

import os
import sys
import importlib
import importlib.util
from typing import Dict, Any, Optional, List, Type
from abc import ABC, abstractmethod


class BaseModule(ABC):
    """
    Abstract base class for all Houdinis modules.
    
    Provides common functionality for scanners, exploits, and payloads including
    option management, requirement validation, and module metadata.
    
    All custom modules (scanners, exploits, payloads) must inherit from this class
    and implement the abstract run() method.
    
    Attributes:
        options (Dict[str, Dict]): Module configuration options
        info (Dict[str, str]): Module metadata (name, description, author, version)
    
    Example:
        >>> class MyExploit(ExploitModule):
        ...     def __init__(self):
        ...         super().__init__()
        ...         self.info['name'] = 'Custom RSA Attack'
        ...     def run(self):
        ...         return {'success': True}
    """

    def __init__(self) -> None:
        """Initialize base module with default options and metadata."""
        self.options = {}
        self.info = {
            "name": "Base Module",
            "description": "Base module class",
            "author": "Mauro Risonho de Paula Assumpção aka firebitsbr",
            "version": "1.0",
            "category": "base",
        }

    @abstractmethod
    def run(self) -> Dict[str, Any]:
        """
        Execute the module.

        Returns:
            Dict containing execution results with at least 'success' key
        """
        pass

    def check_requirements(self) -> bool:
        """
        Validate that all required module options have been configured.
        
        Iterates through module options and checks if required options have
        non-empty values. Should be called before run() to ensure proper setup.

        Returns:
            bool: True if all required options are set with values, False otherwise
        
        Example:
            >>> module = ScannerModule()
            >>> module.set_option('TARGET', '192.168.1.1')
            >>> if module.check_requirements():
            ...     module.run()
        """
        for option, config in self.options.items():
            if config.get("required", False):
                value = getattr(self, option.lower(), None)
                if not value:
                    return False
        return True

    def set_option(self, option: str, value: str) -> bool:
        """
        Set module option value.

        Args:
            option: Option name
            value: Option value

        Returns:
            True if option was set successfully, False otherwise
        """
        option = option.upper()
        if option in self.options:
            setattr(self, option.lower(), value)
            return True
        return False

    def get_option(self, option: str) -> Optional[str]:
        """
        Get module option value.

        Args:
            option: Option name

        Returns:
            Option value or None if not set
        """
        option = option.upper()
        if option in self.options:
            return getattr(self, option.lower(), None)
        return None


class ScannerModule(BaseModule):
    """
    Base class for network and vulnerability scanner modules.
    
    Scanner modules perform reconnaissance, vulnerability detection, and
    information gathering. They identify potential attack surfaces and
    quantum-vulnerable cryptographic implementations.
    
    Attributes:
        target (str): Target host or IP address
        port (str): Target port number
        timeout (str): Connection timeout in seconds
    
    Common Scanner Types:
        - Network scanners (port scanning, service detection)
        - SSL/TLS scanners (cipher suite analysis)
        - Quantum vulnerability scanners (crypto algorithm detection)
    
    Example:
        >>> class CustomScanner(ScannerModule):
        ...     def run(self):
        ...         return {'success': True, 'vulns': []}
        >>> scanner = CustomScanner()
        >>> scanner.set_option('TARGET', 'example.com')
        >>> result = scanner.run()
    """

    def __init__(self) -> None:
        """Initialize scanner module with default network options."""
        super().__init__()
        self.info["category"] = "scanner"

        # Common scanner options
        self.options.update(
            {
                "TARGET": {
                    "description": "Target host or IP address",
                    "required": True,
                    "default": "",
                },
                "PORT": {
                    "description": "Target port",
                    "required": False,
                    "default": "443",
                },
                "TIMEOUT": {
                    "description": "Connection timeout in seconds",
                    "required": False,
                    "default": "10",
                },
            }
        )

        # Initialize option values
        self.target = ""
        self.port = "443"
        self.timeout = "10"


class ExploitModule(BaseModule):
    """
    Base class for quantum cryptanalysis exploit modules.
    
    Exploit modules implement quantum algorithms to break cryptographic systems,
    including Shor's algorithm for RSA/ECC, Grover's for symmetric keys, and
    post-quantum attacks on lattice-based schemes.
    
    Attributes:
        target (str): Target host, key, or cryptographic parameter
    
    Common Exploit Types:
        - Shor's algorithm (RSA, ECDSA, DH key recovery)
        - Grover's algorithm (symmetric key exhaustive search)
        - Quantum annealing (optimization-based attacks)
        - Side-channel attacks (timing, power, fault injection)
    
    Example:
        >>> class ShorsRSA(ExploitModule):
        ...     def run(self):
        ...         return {'success': True, 'factors': [p, q]}
        >>> exploit = ShorsRSA()
        >>> exploit.set_option('TARGET', str(N))
        >>> result = exploit.run()
    """

    def __init__(self) -> None:
        """Initialize exploit module with default attack options."""
        super().__init__()
        self.info["category"] = "exploit"

        # Common exploit options
        self.options.update(
            {
                "TARGET": {
                    "description": "Target host or IP address",
                    "required": True,
                    "default": "",
                },
                "PAYLOAD": {
                    "description": "Payload to use for exploitation",
                    "required": False,
                    "default": "",
                },
            }
        )

        # Initialize option values
        self.target = ""
        self.payload = ""

    def exploit(self) -> Dict[str, Any]:
        """
        Execute the exploit.

        Returns:
            Dict containing exploitation results
        """
        return self.run()


class PayloadModule(BaseModule):
    """
    Base class for payload modules.

    Payloads are used to execute specific actions after successful exploitation.
    """

    def __init__(self) -> None:
        """Initialize payload module with common options."""
        super().__init__()
        self.info["category"] = "payload"

        # Common payload options
        self.options.update(
            {
                "LHOST": {
                    "description": "Local host for reverse connections",
                    "required": False,
                    "default": "127.0.0.1",
                },
                "LPORT": {
                    "description": "Local port for reverse connections",
                    "required": False,
                    "default": "4444",
                },
            }
        )

        # Initialize option values
        self.lhost = "127.0.0.1"
        self.lport = "4444"


class ModuleManager:
    """
    Manages loading and registration of modules.
    """

    def __init__(self) -> None:
        """Initialize module manager."""
        self.modules: Dict[str, Type[BaseModule]] = {}
        self.module_paths = {
            "scanners": "scanners",
            "exploits": "exploits",
            "payloads": "payloads",
            "auxiliary": "auxiliary",
        }

    def load_all_modules(self) -> None:
        """Load all modules from the framework directories."""
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        for module_type, module_dir in self.module_paths.items():
            module_path = os.path.join(base_path, module_dir)

            if os.path.exists(module_path):
                self._load_modules_from_directory(module_path, module_type)

    def _load_modules_from_directory(self, directory: str, module_type: str) -> None:
        """
        Load modules from a specific directory.

        Args:
            directory: Directory path containing modules
            module_type: Type of modules (scanners, exploits, payloads)
        """
        for filename in os.listdir(directory):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]  # Remove .py extension
                module_path = os.path.join(directory, filename)

                try:
                    # Load module dynamically
                    spec = importlib.util.spec_from_file_location(
                        f"{module_type}.{module_name}", module_path
                    )
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    # Find module class (should be capitalized module name + Module)
                    class_name = (
                        "".join(word.capitalize() for word in module_name.split("_"))
                        + "Module"
                    )

                    if hasattr(module, class_name):
                        module_class = getattr(module, class_name)

                        # Verify it's a proper module
                        if issubclass(module_class, BaseModule):
                            full_name = f"{module_type[:-1]}/{module_name}"  # Remove 's' from type
                            self.modules[full_name] = module_class

                except Exception as e:
                    print(f"Error loading module {module_name}: {e}")

    def get_module(self, module_name: str) -> Optional[Type[BaseModule]]:
        """
        Get a specific module class by name.

        Args:
            module_name: Name of the module (e.g., "scanner/ssl_scanner")

        Returns:
            Module class or None if not found
        """
        return self.modules.get(module_name)

    def get_modules(
        self, module_type: Optional[str] = None
    ) -> Dict[str, Type[BaseModule]]:
        """
        Get modules by type.

        Args:
            module_type: Type filter (scanner, exploit, payload) or None for all

        Returns:
            Dictionary of matching modules
        """
        if module_type is None:
            return self.modules.copy()

        return {
            name: module_class
            for name, module_class in self.modules.items()
            if name.startswith(f"{module_type}/")
        }

    def register_module(self, name: str, module_class: Type[BaseModule]) -> None:
        """
        Manually register a module.

        Args:
            name: Module name
            module_class: Module class
        """
        self.modules[name] = module_class

    def list_modules(self) -> List[str]:
        """
        Get list of all available module names.

        Returns:
            List of module names
        """
        return list(self.modules.keys())
