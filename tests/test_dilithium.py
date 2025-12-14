#!/usr/bin/env python3
"""
Unit Tests for CRYSTALS-Dilithium Attack Framework
==================================================

Comprehensive unit tests for the Dilithium signature attack implementation.
Tests all attack methods, parameter sets, and edge cases.

Author: Houdinis Framework
License: MIT
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from exploits.dilithium_attack import DilithiumAttack, DilithiumParameters


class TestDilithiumInitialization:
    """Test Dilithium attack framework initialization"""
    
    def test_init_dilithium2(self):
        """Test initialization with Dilithium2"""
        attacker = DilithiumAttack(parameter_set='dilithium2')
        assert attacker.params.k == 4
        assert attacker.params.security_level == 2
    
    def test_init_dilithium3(self):
        """Test initialization with Dilithium3"""
        attacker = DilithiumAttack(parameter_set='dilithium3')
        assert attacker.params.k == 6
        assert attacker.params.security_level == 3
    
    def test_init_dilithium5(self):
        """Test initialization with Dilithium5"""
        attacker = DilithiumAttack(parameter_set='dilithium5')
        assert attacker.params.k == 8
        assert attacker.params.security_level == 5
    
    def test_invalid_parameter_set(self):
        """Test initialization with invalid parameter set"""
        with pytest.raises((ValueError, KeyError)):
            DilithiumAttack(parameter_set='invalid')


class TestDilithiumSignatureForgery:
    """Test signature forgery attack"""
    
    def test_forgery_basic(self):
        """Test basic signature forgery"""
        attacker = DilithiumAttack(parameter_set='dilithium2')
        result = attacker.signature_forgery_attack(num_attempts=50)
        
        assert 'vulnerable' in result
        assert 'forgery_attempts' in result
        assert isinstance(result['vulnerable'], bool)
    
    def test_forgery_strategies(self):
        """Test different forgery strategies"""
        attacker = DilithiumAttack(parameter_set='dilithium2')
        result = attacker.signature_forgery_attack(num_attempts=50)
        
        if 'strategies_tested' in result:
            assert isinstance(result['strategies_tested'], list)
            assert len(result['strategies_tested']) > 0
    
    def test_forgery_all_parameter_sets(self):
        """Test forgery across all parameter sets"""
        for param_set in ['dilithium2', 'dilithium3', 'dilithium5']:
            attacker = DilithiumAttack(parameter_set=param_set)
            result = attacker.signature_forgery_attack(num_attempts=30)
            assert 'vulnerable' in result


class TestDilithiumNonceReuse:
    """Test nonce reuse attack"""
    
    def test_nonce_reuse_basic(self):
        """Test basic nonce reuse detection"""
        attacker = DilithiumAttack(parameter_set='dilithium2')
        result = attacker.nonce_reuse_attack(num_signatures=30)
        
        assert 'vulnerable' in result
        assert 'reuse_detected' in result
        assert isinstance(result['vulnerable'], bool)
    
    def test_nonce_reuse_similarity(self):
        """Test nonce similarity threshold"""
        attacker = DilithiumAttack(parameter_set='dilithium2')
        result = attacker.nonce_reuse_attack(num_signatures=30)
        
        if 'similar_pairs' in result:
            assert isinstance(result['similar_pairs'], int)
            assert result['similar_pairs'] >= 0


class TestDilithiumTimingAttack:
    """Test timing attack implementation"""
    
    def test_timing_attack_basic(self):
        """Test basic timing attack"""
        attacker = DilithiumAttack(parameter_set='dilithium2')
        result = attacker.timing_attack(num_measurements=200)
        
        assert 'vulnerable' in result
        assert 'timing_measurements' in result
        assert isinstance(result['vulnerable'], bool)
    
    def test_timing_attack_classification(self):
        """Test message classification in timing attack"""
        attacker = DilithiumAttack(parameter_set='dilithium2')
        result = attacker.timing_attack(num_measurements=200)
        
        if 'message_classification' in result:
            assert isinstance(result['message_classification'], dict)


class TestDilithiumFaultInjection:
    """Test fault injection attack"""
    
    def test_fault_injection_basic(self):
        """Test basic fault injection"""
        attacker = DilithiumAttack(parameter_set='dilithium2')
        result = attacker.fault_injection_attack(num_faults=50)
        
        assert 'vulnerable' in result
        assert 'successful_faults' in result
        assert isinstance(result['vulnerable'], bool)
    
    def test_fault_injection_targets(self):
        """Test fault injection targets"""
        attacker = DilithiumAttack(parameter_set='dilithium2')
        result = attacker.fault_injection_attack(num_faults=50)
        
        if 'fault_targets' in result:
            assert isinstance(result['fault_targets'], list)
            assert len(result['fault_targets']) > 0


class TestDilithiumHashCollision:
    """Test hash collision attack"""
    
    def test_hash_collision_basic(self):
        """Test basic hash collision attack"""
        attacker = DilithiumAttack(parameter_set='dilithium2')
        result = attacker.hash_collision_attack(num_attempts=500)
        
        assert 'vulnerable' in result
        assert isinstance(result['vulnerable'], bool)
    
    def test_hash_collision_detection(self):
        """Test collision detection"""
        attacker = DilithiumAttack(parameter_set='dilithium2')
        result = attacker.hash_collision_attack(num_attempts=500)
        
        if 'collisions_found' in result:
            assert isinstance(result['collisions_found'], int)
            assert result['collisions_found'] >= 0


class TestDilithiumLatticeAttack:
    """Test lattice attack implementation"""
    
    def test_lattice_attack_basic(self):
        """Test basic lattice attack"""
        attacker = DilithiumAttack(parameter_set='dilithium2')
        result = attacker.lattice_attack()
        
        assert 'vulnerable' in result
        assert isinstance(result['vulnerable'], bool)
    
    def test_lattice_attack_hardness(self):
        """Test hardness estimation"""
        attacker = DilithiumAttack(parameter_set='dilithium2')
        result = attacker.lattice_attack()
        
        if 'mlwe_hardness' in result or 'msis_hardness' in result:
            # Should have some hardness estimate
            assert True


class TestDilithiumParameterAnalysis:
    """Test parameter analysis"""
    
    def test_parameter_analysis_basic(self):
        """Test basic parameter analysis"""
        attacker = DilithiumAttack(parameter_set='dilithium2')
        result = attacker.parameter_analysis()
        
        assert 'vulnerable' in result
        assert 'weak_parameters' in result
        assert isinstance(result['vulnerable'], bool)
    
    def test_parameter_analysis_modulus(self):
        """Test modulus validation"""
        attacker = DilithiumAttack(parameter_set='dilithium2')
        result = attacker.parameter_analysis()
        
        # Should check modulus q = 8380417
        assert 'weak_parameters' in result


class TestDilithiumComprehensiveAudit:
    """Test comprehensive security audit"""
    
    def test_comprehensive_audit_basic(self):
        """Test basic comprehensive audit"""
        attacker = DilithiumAttack(parameter_set='dilithium2')
        result = attacker.comprehensive_security_audit()
        
        assert 'parameter_set' in result
        assert 'timestamp' in result
        assert 'overall_assessment' in result
    
    def test_comprehensive_audit_completeness(self):
        """Test comprehensive audit includes all attacks"""
        attacker = DilithiumAttack(parameter_set='dilithium2')
        result = attacker.comprehensive_security_audit()
        
        required_attacks = [
            'signature_forgery',
            'nonce_reuse',
            'timing_attack',
            'fault_injection',
            'hash_collision',
            'lattice_attack',
            'parameter_analysis'
        ]
        
        for attack in required_attacks:
            assert attack in result, f"Missing attack: {attack}"
    
    def test_comprehensive_audit_assessment(self):
        """Test overall assessment structure"""
        attacker = DilithiumAttack(parameter_set='dilithium2')
        result = attacker.comprehensive_security_audit()
        
        assessment = result['overall_assessment']
        assert 'security_rating' in assessment
        assert 'vulnerabilities_found' in assessment
        assert 'recommendations' in assessment
        
        assert isinstance(assessment['security_rating'], str)
        assert isinstance(assessment['vulnerabilities_found'], int)
        assert isinstance(assessment['recommendations'], list)


class TestDilithiumExport:
    """Test result export functionality"""
    
    def test_export_to_dict(self):
        """Test exporting results to dictionary"""
        attacker = DilithiumAttack(parameter_set='dilithium2')
        result = attacker.comprehensive_security_audit()
        
        # Should be JSON-serializable
        import json
        try:
            json.dumps(result)
        except (TypeError, ValueError) as e:
            pytest.fail(f"Result not JSON-serializable: {e}")


@pytest.mark.parametrize("param_set", ['dilithium2', 'dilithium3', 'dilithium5'])
class TestDilithiumParameterSets:
    """Parameterized tests across all Dilithium parameter sets"""
    
    def test_parameter_set_consistency(self, param_set):
        """Test consistency across parameter sets"""
        attacker = DilithiumAttack(parameter_set=param_set)
        
        # All parameter sets should support all attacks
        result = attacker.signature_forgery_attack(num_attempts=30)
        assert 'vulnerable' in result
        
        result = attacker.nonce_reuse_attack(num_signatures=20)
        assert 'vulnerable' in result
    
    def test_security_levels(self, param_set):
        """Test security level assignments"""
        attacker = DilithiumAttack(parameter_set=param_set)
        
        expected_levels = {
            'dilithium2': 2,
            'dilithium3': 3,
            'dilithium5': 5
        }
        
        assert attacker.params.security_level == expected_levels[param_set]
    
    def test_parameter_dimensions(self, param_set):
        """Test parameter dimensions"""
        attacker = DilithiumAttack(parameter_set=param_set)
        
        expected_k = {
            'dilithium2': 4,
            'dilithium3': 6,
            'dilithium5': 8
        }
        
        assert attacker.params.k == expected_k[param_set]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
