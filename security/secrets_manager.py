#!/usr/bin/env python3
"""
Houdinis Framework - Secrets Management Module
Author: Mauro Risonho de Paula Assumpção aka firebitsbr
Desenvolvido: Lógica e Codificação por Humano e AI Assistida (Claude Sonnet 4.5)
License: MIT

Secure secrets management for API keys, tokens, and credentials.
"""

import os
import json
import base64
import secrets as py_secrets
from pathlib import Path
from typing import Dict, Optional, Any
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import logging


class SecretsManager:
    """Secure secrets management for Houdinis framework"""

    def __init__(self, secrets_dir: Optional[str] = None):
        """Initialize secrets manager"""
        if secrets_dir:
            self.secrets_dir = Path(secrets_dir)
        else:
            self.secrets_dir = Path.home() / ".houdinis" / "secrets"

        self.secrets_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.secrets_file = self.secrets_dir / "credentials.enc"
        self.key_file = self.secrets_dir / ".key"

        self.logger = self._setup_logging()
        self._cipher = None

    def _setup_logging(self) -> logging.Logger:
        """Setup secure logging"""
        logger = logging.getLogger("houdinis.secrets")
        logger.setLevel(logging.INFO)

        # Log to file only, never to console (security)
        log_file = self.secrets_dir / "secrets.log"
        handler = logging.FileHandler(log_file, mode="a")
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(handler)

        return logger

    def _get_cipher(self, master_password: Optional[str] = None) -> Fernet:
        """Get or create cipher for encryption/decryption"""
        if self._cipher:
            return self._cipher

        # Try to load existing key
        if self.key_file.exists():
            with open(self.key_file, "rb") as f:
                key = f.read()
        else:
            # Generate new key from master password or random
            if master_password:
                salt = py_secrets.token_bytes(16)
                kdf = PBKDF2(
                    algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000
                )
                key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
            else:
                key = Fernet.generate_key()

            # Save key securely
            with open(self.key_file, "wb") as f:
                f.write(key)
            os.chmod(self.key_file, 0o600)

            self.logger.info("Created new encryption key")

        self._cipher = Fernet(key)
        return self._cipher

    def store_secret(self, key: str, value: str, category: str = "general") -> bool:
        """
        Store a secret securely

        Args:
            key: Secret identifier (e.g., 'ibm_quantum_token')
            value: Secret value to encrypt and store
            category: Category for organization (e.g., 'api_keys', 'passwords')

        Returns:
            True if successful, False otherwise
        """
        try:
            # Load existing secrets
            secrets = self._load_secrets()

            # Add new secret
            if category not in secrets:
                secrets[category] = {}

            secrets[category][key] = value

            # Save encrypted secrets
            self._save_secrets(secrets)

            self.logger.info(f"Stored secret: {category}/{key}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to store secret {category}/{key}: {e}")
            return False

    def get_secret(
        self, key: str, category: str = "general", default: Optional[str] = None
    ) -> Optional[str]:
        """
        Retrieve a secret

        Args:
            key: Secret identifier
            category: Category to search in
            default: Default value if not found

        Returns:
            Secret value or default if not found
        """
        try:
            secrets = self._load_secrets()
            return secrets.get(category, {}).get(key, default)
        except Exception as e:
            self.logger.error(f"Failed to retrieve secret {category}/{key}: {e}")
            return default

    def delete_secret(self, key: str, category: str = "general") -> bool:
        """Delete a secret"""
        try:
            secrets = self._load_secrets()
            if category in secrets and key in secrets[category]:
                del secrets[category][key]
                self._save_secrets(secrets)
                self.logger.info(f"Deleted secret: {category}/{key}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to delete secret {category}/{key}: {e}")
            return False

    def list_secrets(self, category: Optional[str] = None) -> Dict[str, list]:
        """
        List available secrets (keys only, not values)

        Args:
            category: Optional category filter

        Returns:
            Dictionary of categories and their secret keys
        """
        try:
            secrets = self._load_secrets()

            if category:
                if category in secrets:
                    return {category: list(secrets[category].keys())}
                return {category: []}

            return {cat: list(keys.keys()) for cat, keys in secrets.items()}

        except Exception as e:
            self.logger.error(f"Failed to list secrets: {e}")
            return {}

    def _load_secrets(self) -> Dict[str, Dict[str, str]]:
        """Load and decrypt secrets from file"""
        if not self.secrets_file.exists():
            return {}

        try:
            cipher = self._get_cipher()

            with open(self.secrets_file, "rb") as f:
                encrypted_data = f.read()

            decrypted_data = cipher.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode())

        except Exception as e:
            self.logger.error(f"Failed to load secrets: {e}")
            return {}

    def _save_secrets(self, secrets: Dict[str, Dict[str, str]]):
        """Encrypt and save secrets to file"""
        try:
            cipher = self._get_cipher()

            # Serialize and encrypt
            json_data = json.dumps(secrets).encode()
            encrypted_data = cipher.encrypt(json_data)

            # Write atomically
            temp_file = self.secrets_file.with_suffix(".tmp")
            with open(temp_file, "wb") as f:
                f.write(encrypted_data)
            os.chmod(temp_file, 0o600)

            # Atomic rename
            temp_file.replace(self.secrets_file)

        except Exception as e:
            self.logger.error(f"Failed to save secrets: {e}")
            raise

    @staticmethod
    def get_from_env(key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get secret from environment variable

        Supports common naming conventions:
        - HOUDINIS_API_KEY
        - IBM_QUANTUM_TOKEN
        - AWS_ACCESS_KEY_ID
        etc.
        """
        # Try direct lookup
        value = os.getenv(key, default)
        if value:
            return value

        # Try with HOUDINIS_ prefix
        prefixed_key = f"HOUDINIS_{key.upper()}"
        return os.getenv(prefixed_key, default)

    def import_from_env(self, mapping: Optional[Dict[str, str]] = None):
        """
        Import secrets from environment variables

        Args:
            mapping: Dict of env_var_name -> (category, key)
                    e.g., {'IBM_QUANTUM_TOKEN': ('api_keys', 'ibm_quantum')}
        """
        if not mapping:
            # Default mappings for common secrets
            mapping = {
                "IBM_QUANTUM_TOKEN": ("api_keys", "ibm_quantum"),
                "AWS_ACCESS_KEY_ID": ("api_keys", "aws_access_key"),
                "AWS_SECRET_ACCESS_KEY": ("api_keys", "aws_secret_key"),
                "AZURE_QUANTUM_SUBSCRIPTION": ("api_keys", "azure_subscription"),
                "GOOGLE_QUANTUM_PROJECT": ("api_keys", "google_project"),
            }

        imported = 0
        for env_var, (category, key) in mapping.items():
            value = os.getenv(env_var)
            if value:
                if self.store_secret(key, value, category):
                    imported += 1

        self.logger.info(f"Imported {imported} secrets from environment")
        return imported


# Global instance
_secrets_manager: Optional[SecretsManager] = None


def get_secrets_manager() -> SecretsManager:
    """Get global secrets manager instance"""
    global _secrets_manager
    if _secrets_manager is None:
        _secrets_manager = SecretsManager()
    return _secrets_manager


def get_quantum_token(backend: str) -> Optional[str]:
    """
    Get quantum backend API token

    Args:
        backend: Backend name ('ibm', 'aws', 'azure', 'google')

    Returns:
        API token or None if not found
    """
    manager = get_secrets_manager()

    # Map backend names to secret keys
    key_mapping = {
        "ibm": "ibm_quantum",
        "aws": "aws_access_key",
        "azure": "azure_subscription",
        "google": "google_project",
    }

    key = key_mapping.get(backend.lower())
    if not key:
        return None

    # Try secrets manager first
    token = manager.get_secret(key, "api_keys")
    if token:
        return token

    # Fallback to environment variables
    env_mapping = {
        "ibm": "IBM_QUANTUM_TOKEN",
        "aws": "AWS_ACCESS_KEY_ID",
        "azure": "AZURE_QUANTUM_SUBSCRIPTION",
        "google": "GOOGLE_QUANTUM_PROJECT",
    }

    env_var = env_mapping.get(backend.lower())
    return SecretsManager.get_from_env(env_var) if env_var else None
