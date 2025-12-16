#!/usr/bin/env python3
"""
# Houdinis Framework - Quantum Cryptography Testing Platform
# Author: Mauro Risonho de Paula Assumpção aka firebitsbr
# Developed by: Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)
# License: MIT

Unit Tests for FALCON and SPHINCS+ Attack Frameworks
====================================================
Comprehensive unit tests for FALCON and SPHINCS+ signature attack implementations.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from exploits.falcon_sphincs_attack import FALCONAttack, SPHINCSAttack


# FALCON Tests
class TestFALCONInitialization:
    """Test FALCON attack framework initialization"""

    def test_init_falcon512(self):
        """Test initialization with FALCON-512"""
        attacker = FALCONAttack(parameter_set="falcon512")
        assert attacker.params.n == 512
        assert attacker.params.security_level == 1

    def test_init_falcon1024(self):
        """Test initialization with FALCON-1024"""
        attacker = FALCONAttack(parameter_set="falcon1024")
        assert attacker.params.n == 1024
        assert attacker.params.security_level == 5


class TestFALCONNTRULattice:
    """Test NTRU lattice attack"""

    def test_ntru_lattice_basic(self):
        """Test basic NTRU lattice attack"""
        attacker = FALCONAttack(parameter_set="falcon512")
        result = attacker.ntru_lattice_attack(num_attempts=50)

        assert "vulnerable" in result
        assert isinstance(result["vulnerable"], bool)


class TestFALCONGaussianSampling:
    """Test Gaussian sampling attack"""

    def test_gaussian_sampling_basic(self):
        """Test basic Gaussian sampling attack"""
        attacker = FALCONAttack(parameter_set="falcon512")
        result = attacker.gaussian_sampling_attack(num_samples=500)

        assert "vulnerable" in result
        assert "chi_square_statistic" in result


class TestFALCONComprehensive:
    """Test FALCON comprehensive audit"""

    def test_comprehensive_audit(self):
        """Test FALCON comprehensive audit"""
        attacker = FALCONAttack(parameter_set="falcon512")
        result = attacker.comprehensive_security_audit()

        assert "overall_assessment" in result
        assert "security_rating" in result["overall_assessment"]


# SPHINCS+ Tests
class TestSPHINCSInitialization:
    """Test SPHINCS+ attack framework initialization"""

    def test_init_sphincs128f(self):
        """Test initialization with SPHINCS+-128f"""
        attacker = SPHINCSAttack(parameter_set="sphincs128f")
        assert attacker.params.security_level == 128

    def test_init_sphincs256f(self):
        """Test initialization with SPHINCS+-256f"""
        attacker = SPHINCSAttack(parameter_set="sphincs256f")
        assert attacker.params.security_level == 256


class TestSPHINCSHashCollision:
    """Test hash collision attack"""

    def test_hash_collision_basic(self):
        """Test basic hash collision attack"""
        attacker = SPHINCSAttack(parameter_set="sphincs128f")
        result = attacker.hash_collision_attack(num_attempts=5000)

        assert "vulnerable" in result
        assert isinstance(result["vulnerable"], bool)


class TestSPHINCSMultiTarget:
    """Test multi-target attack"""

    def test_multi_target_basic(self):
        """Test basic multi-target attack"""
        attacker = SPHINCSAttack(parameter_set="sphincs128f")
        result = attacker.multi_target_attack(num_targets=5, attempts_per_target=500)

        assert "vulnerable" in result
        assert "security_reduction" in result


class TestSPHINCSComprehensive:
    """Test SPHINCS+ comprehensive audit"""

    def test_comprehensive_audit(self):
        """Test SPHINCS+ comprehensive audit"""
        attacker = SPHINCSAttack(parameter_set="sphincs128f")
        result = attacker.comprehensive_security_audit()

        assert "overall_assessment" in result
        assert "security_rating" in result["overall_assessment"]


@pytest.mark.parametrize("param_set", ["falcon512", "falcon1024"])
class TestFALCONParameterSets:
    """Parameterized tests for FALCON parameter sets"""

    def test_parameter_consistency(self, param_set):
        """Test consistency across parameter sets"""
        attacker = FALCONAttack(parameter_set=param_set)
        result = attacker.ntru_lattice_attack(num_attempts=30)
        assert "vulnerable" in result


@pytest.mark.parametrize("param_set", ["sphincs128f", "sphincs256f"])
class TestSPHINCSParameterSets:
    """Parameterized tests for SPHINCS+ parameter sets"""

    def test_parameter_consistency(self, param_set):
        """Test consistency across parameter sets"""
        attacker = SPHINCSAttack(parameter_set=param_set)
        result = attacker.hash_collision_attack(num_attempts=1000)
        assert "vulnerable" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
