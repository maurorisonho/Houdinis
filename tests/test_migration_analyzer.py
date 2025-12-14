#!/usr/bin/env python3
"""
Unit Tests for PQC Migration Analyzer
=====================================

Comprehensive unit tests for the PQC migration analysis framework.

Author: Houdinis Framework
License: MIT
"""

import pytest
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from exploits.pqc_migration_analyzer import PQCMigrationAnalyzer, CryptoUsage


class TestMigrationAnalyzerInitialization:
    """Test migration analyzer initialization"""
    
    def test_init_basic(self):
        """Test basic initialization"""
        analyzer = PQCMigrationAnalyzer()
        assert analyzer is not None


class TestFileScan ning:
    """Test file scanning functionality"""
    
    def test_scan_file_with_rsa(self):
        """Test scanning file containing RSA"""
        analyzer = PQCMigrationAnalyzer()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('from Crypto.PublicKey import RSA\nkey = RSA.generate(2048)')
            tmpfile = f.name
        
        try:
            result = analyzer.scan_file(tmpfile)
            assert 'crypto_usages' in result
            assert len(result['crypto_usages']) > 0
            
            # Should find RSA
            algorithms = [usage.algorithm for usage in result['crypto_usages']]
            assert 'RSA' in algorithms
        finally:
            Path(tmpfile).unlink()
    
    def test_scan_file_with_ecdh(self):
        """Test scanning file containing ECDH"""
        analyzer = PQCMigrationAnalyzer()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('from cryptography.hazmat.primitives.asymmetric import ec\nkey = ec.generate_private_key()')
            tmpfile = f.name
        
        try:
            result = analyzer.scan_file(tmpfile)
            assert 'crypto_usages' in result
        finally:
            Path(tmpfile).unlink()


class TestDirectoryScan:
    """Test directory scanning"""
    
    def test_scan_directory_basic(self):
        """Test basic directory scanning"""
        analyzer = PQCMigrationAnalyzer()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            # Create test files
            (tmppath / 'test1.py').write_text('import rsa\nkey = rsa.newkeys(2048)')
            (tmppath / 'test2.py').write_text('from ecdsa import SigningKey')
            
            result = analyzer.scan_directory(tmpdir)
            
            assert 'files_scanned' in result
            assert result['files_scanned'] >= 2
            assert 'crypto_usages' in result


class TestVulnerabilityAssessment:
    """Test vulnerability assessment"""
    
    def test_assess_rsa_vulnerability(self):
        """Test assessing RSA vulnerability"""
        analyzer = PQCMigrationAnalyzer()
        
        usage = CryptoUsage(
            algorithm='RSA',
            file_path='/test.py',
            line_number=1,
            context='RSA.generate(2048)',
            security_level=112
        )
        
        assessment = analyzer.assess_vulnerabilities(usage)
        
        assert assessment.threat_level in ['immediate', 'near_term', 'long_term']
        assert assessment.quantum_security_bits >= 0


class TestRecommendations:
    """Test recommendation generation"""
    
    def test_generate_recommendations_for_rsa(self):
        """Test generating recommendations for RSA"""
        analyzer = PQCMigrationAnalyzer()
        
        usage = CryptoUsage(
            algorithm='RSA',
            file_path='/test.py',
            line_number=1,
            context='RSA.generate(2048)',
            security_level=112
        )
        
        assessment = analyzer.assess_vulnerabilities(usage)
        recommendation = analyzer.generate_recommendations(assessment)
        
        assert recommendation.current_algorithm == 'RSA'
        assert recommendation.recommended_pqc_algorithm is not None


class TestMigrationPath:
    """Test migration path creation"""
    
    def test_create_migration_path_direct(self):
        """Test creating direct migration path"""
        analyzer = PQCMigrationAnalyzer()
        
        usage = CryptoUsage(
            algorithm='RSA',
            file_path='/test.py',
            line_number=1,
            context='RSA.generate(2048)',
            security_level=112
        )
        
        assessment = analyzer.assess_vulnerabilities(usage)
        recommendation = analyzer.generate_recommendations(assessment)
        path = analyzer.create_migration_path(recommendation)
        
        assert 'strategy' in path
        assert 'phases' in path
        assert 'timeline_weeks' in path
        assert len(path['phases']) > 0


class TestComprehensiveReport:
    """Test comprehensive report generation"""
    
    def test_generate_comprehensive_report(self):
        """Test generating comprehensive report"""
        analyzer = PQCMigrationAnalyzer()
        
        scan_result = {
            'files_scanned': 5,
            'crypto_usages': []
        }
        
        report = analyzer.generate_comprehensive_report(
            scan_result=scan_result,
            assessments=[],
            recommendations=[]
        )
        
        assert 'summary' in report
        assert 'vulnerabilities' in report
        assert 'recommendations' in report
        assert 'budget_estimate' in report


class TestExport:
    """Test report export"""
    
    def test_export_report(self):
        """Test exporting report to JSON"""
        analyzer = PQCMigrationAnalyzer()
        
        report = {
            'summary': {'files': 0},
            'vulnerabilities': [],
            'recommendations': []
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            tmpfile = f.name
        
        try:
            analyzer.export_report(report, tmpfile)
            assert Path(tmpfile).exists()
        finally:
            Path(tmpfile).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
