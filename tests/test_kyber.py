#!/usr/bin/env python3
"""
Unit Tests for CRYSTALS-Kyber Attack Framework
===============================================

Comprehensive unit tests for the Kyber KEM attack implementation.
Tests all attack methods, parameter sets, and edge cases.

Author: Houdinis Framework
Developed by: Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)
License: MIT
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from exploits.kyber_attack import KyberAttack, KyberParameters


class TestKyberInitialization:
    """Test Kyber attack framework initialization"""

    def test_init_kyber512(self):
        """Test initialization with Kyber512"""
        attacker = KyberAttack(parameter_set="kyber512")
        assert attacker.params.k == 2
        assert attacker.params.security_level == 1

    def test_init_kyber768(self):
        """Test initialization with Kyber768"""
        attacker = KyberAttack(parameter_set="kyber768")
        assert attacker.params.k == 3
        assert attacker.params.security_level == 3

    def test_init_kyber1024(self):
        """Test initialization with Kyber1024"""
        attacker = KyberAttack(parameter_set="kyber1024")
        assert attacker.params.k == 4
        assert attacker.params.security_level == 5

    def test_invalid_parameter_set(self):
        """Test initialization with invalid parameter set"""
        with pytest.raises((ValueError, KeyError)):
            KyberAttack(parameter_set="invalid")


class TestKyberTimingAttack:
    """Test timing attack implementation"""

    def test_timing_attack_basic(self):
        """Test basic timing attack"""
        attacker = KyberAttack(parameter_set="kyber512")
        result = attacker.timing_attack(num_samples=100)

        assert "vulnerable" in result
        assert "timing_variations" in result
        assert isinstance(result["vulnerable"], bool)

    def test_timing_attack_different_sample_sizes(self):
        """Test timing attack with different sample sizes"""
        attacker = KyberAttack(parameter_set="kyber512")

        for num_samples in [50, 100, 200]:
            result = attacker.timing_attack(num_samples=num_samples)
            assert len(result["timing_variations"]) <= num_samples

    def test_timing_attack_all_parameter_sets(self):
        """Test timing attack across all parameter sets"""
        for param_set in ["kyber512", "kyber768", "kyber1024"]:
            attacker = KyberAttack(parameter_set=param_set)
            result = attacker.timing_attack(num_samples=100)
            assert "coefficient_of_variation" in result


class TestKyberPowerAnalysis:
    """Test power analysis attack"""

    def test_power_analysis_basic(self):
        """Test basic power analysis"""
        attacker = KyberAttack(parameter_set="kyber512")
        result = attacker.power_analysis_attack(num_traces=100)

        assert "vulnerable" in result
        assert "power_traces" in result
        assert isinstance(result["vulnerable"], bool)

    def test_power_analysis_snr(self):
        """Test SNR calculation in power analysis"""
        attacker = KyberAttack(parameter_set="kyber512")
        result = attacker.power_analysis_attack(num_traces=100)

        if "snr" in result:
            assert isinstance(result["snr"], (int, float))
            assert result["snr"] > 0


class TestKyberCCAAttack:
    """Test chosen-ciphertext attack"""

    def test_cca_attack_basic(self):
        """Test basic CCA attack"""
        attacker = KyberAttack(parameter_set="kyber512")
        result = attacker.cca_attack(num_queries=50)

        assert "vulnerable" in result
        assert "oracle_queries" in result
        assert isinstance(result["vulnerable"], bool)

    def test_cca_attack_query_count(self):
        """Test CCA attack respects query limit"""
        attacker = KyberAttack(parameter_set="kyber512")

        num_queries = 30
        result = attacker.cca_attack(num_queries=num_queries)
        assert result["oracle_queries"] <= num_queries


class TestKyberFaultInjection:
    """Test fault injection attack"""

    def test_fault_injection_basic(self):
        """Test basic fault injection"""
        attacker = KyberAttack(parameter_set="kyber512")
        result = attacker.fault_injection_attack(num_faults=50)

        assert "vulnerable" in result
        assert "successful_faults" in result
        assert isinstance(result["vulnerable"], bool)

    def test_fault_injection_targets(self):
        """Test fault injection with different targets"""
        attacker = KyberAttack(parameter_set="kyber512")
        result = attacker.fault_injection_attack(num_faults=50)

        if "fault_targets" in result:
            assert isinstance(result["fault_targets"], list)


class TestKyberCacheTiming:
    """Test cache timing attack"""

    def test_cache_timing_basic(self):
        """Test basic cache timing attack"""
        attacker = KyberAttack(parameter_set="kyber512")
        result = attacker.cache_timing_attack(num_measurements=200)

        assert "vulnerable" in result
        assert "cache_patterns" in result
        assert isinstance(result["vulnerable"], bool)

    def test_cache_timing_entropy(self):
        """Test entropy calculation in cache timing"""
        attacker = KyberAttack(parameter_set="kyber512")
        result = attacker.cache_timing_attack(num_measurements=200)

        if "pattern_entropy" in result:
            assert isinstance(result["pattern_entropy"], (int, float))
            assert result["pattern_entropy"] >= 0


class TestKyberLatticeReduction:
    """Test lattice reduction attack"""

    def test_lattice_reduction_basic(self):
        """Test basic lattice reduction"""
        attacker = KyberAttack(parameter_set="kyber512")
        result = attacker.lattice_reduction_attack()

        assert "vulnerable" in result
        assert isinstance(result["vulnerable"], bool)

    def test_lattice_reduction_security_margin(self):
        """Test security margin calculation"""
        attacker = KyberAttack(parameter_set="kyber512")
        result = attacker.lattice_reduction_attack()

        if "security_margin" in result:
            assert isinstance(result["security_margin"], (int, float))


class TestKyberParameterAnalysis:
    """Test parameter analysis"""

    def test_parameter_analysis_basic(self):
        """Test basic parameter analysis"""
        attacker = KyberAttack(parameter_set="kyber512")
        result = attacker.parameter_analysis()

        assert "vulnerable" in result
        assert "weak_parameters" in result
        assert isinstance(result["vulnerable"], bool)

    def test_parameter_analysis_all_sets(self):
        """Test parameter analysis for all sets"""
        for param_set in ["kyber512", "kyber768", "kyber1024"]:
            attacker = KyberAttack(parameter_set=param_set)
            result = attacker.parameter_analysis()
            assert "weak_parameters" in result


class TestKyberComprehensiveAudit:
    """Test comprehensive security audit"""

    def test_comprehensive_audit_basic(self):
        """Test basic comprehensive audit"""
        attacker = KyberAttack(parameter_set="kyber512")
        result = attacker.comprehensive_security_audit()

        assert "parameter_set" in result
        assert "timestamp" in result
        assert "overall_assessment" in result

    def test_comprehensive_audit_completeness(self):
        """Test comprehensive audit includes all attacks"""
        attacker = KyberAttack(parameter_set="kyber512")
        result = attacker.comprehensive_security_audit()

        required_attacks = [
            "timing_attack",
            "power_analysis",
            "cca_attack",
            "fault_injection",
            "cache_timing",
            "lattice_reduction",
            "parameter_analysis",
        ]

        for attack in required_attacks:
            assert attack in result, f"Missing attack: {attack}"

    def test_comprehensive_audit_assessment(self):
        """Test overall assessment structure"""
        attacker = KyberAttack(parameter_set="kyber512")
        result = attacker.comprehensive_security_audit()

        assessment = result["overall_assessment"]
        assert "security_rating" in assessment
        assert "vulnerabilities_found" in assessment
        assert "recommendations" in assessment

        assert isinstance(assessment["security_rating"], str)
        assert isinstance(assessment["vulnerabilities_found"], int)
        assert isinstance(assessment["recommendations"], list)


class TestKyberExport:
    """Test result export functionality"""

    def test_export_to_dict(self):
        """Test exporting results to dictionary"""
        attacker = KyberAttack(parameter_set="kyber512")
        result = attacker.comprehensive_security_audit()

        # Should be JSON-serializable
        import json

        try:
            json.dumps(result)
        except (TypeError, ValueError) as e:
            pytest.fail(f"Result not JSON-serializable: {e}")


@pytest.mark.parametrize("param_set", ["kyber512", "kyber768", "kyber1024"])
class TestKyberParameterSets:
    """Parameterized tests across all Kyber parameter sets"""

    def test_parameter_set_consistency(self, param_set):
        """Test consistency across parameter sets"""
        attacker = KyberAttack(parameter_set=param_set)

        # All parameter sets should support all attacks
        result = attacker.timing_attack(num_samples=50)
        assert "vulnerable" in result

        result = attacker.cca_attack(num_queries=30)
        assert "vulnerable" in result

    def test_security_levels(self, param_set):
        """Test security level assignments"""
        attacker = KyberAttack(parameter_set=param_set)

        expected_levels = {"kyber512": 1, "kyber768": 3, "kyber1024": 5}

        assert attacker.params.security_level == expected_levels[param_set]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
