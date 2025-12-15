#!/usr/bin/env python3
"""
Unit Tests for Hybrid PQC Attack Framework
==========================================

Comprehensive unit tests for hybrid classical+PQC attack implementation.

Author: Houdinis Framework
Desenvolvido: Lógica e Codificação por Humano e AI Assistida (Claude Sonnet 4.5)
License: MIT
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from exploits.hybrid_pqc_attack import HybridPQCAttack


class TestHybridInitialization:
    """Test hybrid attack framework initialization"""

    def test_init_tls_128(self):
        """Test initialization with Hybrid-TLS-128"""
        attacker = HybridPQCAttack(configuration="hybrid-tls-128")
        assert attacker.config.security_bits == 128

    def test_init_tls_192(self):
        """Test initialization with Hybrid-TLS-192"""
        attacker = HybridPQCAttack(configuration="hybrid-tls-192")
        assert attacker.config.security_bits == 192

    def test_init_tls_256(self):
        """Test initialization with Hybrid-TLS-256"""
        attacker = HybridPQCAttack(configuration="hybrid-tls-256")
        assert attacker.config.security_bits == 256


class TestHybridDowngradeAttack:
    """Test downgrade attack"""

    def test_downgrade_basic(self):
        """Test basic downgrade attack"""
        attacker = HybridPQCAttack(configuration="hybrid-tls-128")
        result = attacker.downgrade_attack(num_attempts=50)

        assert "vulnerable" in result
        assert isinstance(result["vulnerable"], bool)

    def test_downgrade_methods(self):
        """Test downgrade methods"""
        attacker = HybridPQCAttack(configuration="hybrid-tls-128")
        result = attacker.downgrade_attack(num_attempts=50)

        if "downgrade_methods" in result:
            assert isinstance(result["downgrade_methods"], list)


class TestHybridKeyExchangeConfusion:
    """Test key exchange confusion attack"""

    def test_kex_confusion_basic(self):
        """Test basic key exchange confusion"""
        attacker = HybridPQCAttack(configuration="hybrid-tls-128")
        result = attacker.key_exchange_confusion_attack(num_sessions=30)

        assert "vulnerable" in result
        assert isinstance(result["vulnerable"], bool)


class TestHybridSignatureBypass:
    """Test signature verification bypass"""

    def test_signature_bypass_basic(self):
        """Test basic signature bypass"""
        attacker = HybridPQCAttack(configuration="hybrid-tls-128")
        result = attacker.signature_verification_bypass(num_attempts=50)

        assert "vulnerable" in result
        assert isinstance(result["vulnerable"], bool)


class TestHybridTransitionPeriod:
    """Test transition period exploit"""

    def test_transition_exploit_basic(self):
        """Test basic transition period exploit"""
        attacker = HybridPQCAttack(configuration="hybrid-tls-128")
        result = attacker.transition_period_exploit(num_scenarios=30)

        assert "vulnerable" in result
        assert isinstance(result["vulnerable"], bool)


class TestHybridComprehensiveAudit:
    """Test comprehensive hybrid audit"""

    def test_comprehensive_audit_basic(self):
        """Test basic comprehensive audit"""
        attacker = HybridPQCAttack(configuration="hybrid-tls-128")
        result = attacker.comprehensive_hybrid_audit()

        assert "configuration" in result
        assert "overall_assessment" in result

    def test_comprehensive_audit_completeness(self):
        """Test audit includes all attacks"""
        attacker = HybridPQCAttack(configuration="hybrid-tls-128")
        result = attacker.comprehensive_hybrid_audit()

        required_attacks = [
            "downgrade_attack",
            "key_exchange_confusion",
            "signature_verification_bypass",
            "transition_period_exploit",
        ]

        for attack in required_attacks:
            assert attack in result, f"Missing attack: {attack}"


@pytest.mark.parametrize(
    "config", ["hybrid-tls-128", "hybrid-tls-192", "hybrid-tls-256"]
)
class TestHybridConfigurations:
    """Parameterized tests across hybrid configurations"""

    def test_configuration_consistency(self, config):
        """Test consistency across configurations"""
        attacker = HybridPQCAttack(configuration=config)
        result = attacker.downgrade_attack(num_attempts=30)
        assert "vulnerable" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
