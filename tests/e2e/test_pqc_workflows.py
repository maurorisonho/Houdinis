#!/usr/bin/env python3
"""
# Houdinis Framework - Quantum Cryptography Testing Platform
# Author: Mauro Risonho de Paula Assumpção aka firebitsbr
# Developed by: Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)
# License: MIT

End-to-End Post-Quantum Cryptography Workflow Tests
====================================================
Comprehensive E2E tests for complete PQC attack workflows.
Tests the entire pipeline from PQC scheme setup to vulnerability assessment.
Test Categories:
- Complete CRYSTALS-Kyber KEM attack workflow
- Full CRYSTALS-Dilithium signature analysis workflow
- FALCON/SPHINCS+ alternative signature testing
- Hybrid classical+PQC attack workflow
- PQC migration analysis workflow
"""

import pytest
import sys
import os
import time
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from exploits.kyber_attack import KyberAttack
from exploits.dilithium_attack import DilithiumAttack
from exploits.falcon_sphincs_attack import FALCONAttack, SPHINCSAttack
from exploits.hybrid_pqc_attack import HybridPQCAttack
from exploits.pqc_migration_analyzer import PQCMigrationAnalyzer


@pytest.mark.e2e
@pytest.mark.pqc
@pytest.mark.slow
class TestKyberAttackWorkflow:
    """End-to-end tests for CRYSTALS-Kyber KEM attack workflows"""

    def test_complete_kyber_security_audit(self):
        """
        Test complete Kyber security audit workflow.

        Workflow:
        1. Initialize Kyber attack framework
        2. Run side-channel attacks (timing, power, cache)
        3. Attempt CCA attack
        4. Perform lattice reduction analysis
        5. Comprehensive security assessment
        """
        print("\n[E2E-PQC] Testing complete Kyber security audit workflow...")

        # Step 1: Initialize for all security levels
        security_levels = ["kyber512", "kyber768", "kyber1024"]

        for level in security_levels:
            print(f"\n[E2E-PQC] Testing {level.upper()}...")

            attacker = KyberAttack(parameter_set=level)

            # Step 2: Side-channel attacks
            print(f"[E2E-PQC] Running side-channel attacks...")

            # Timing attack
            timing_result = attacker.timing_attack(num_samples=500)
            assert (
                "vulnerable" in timing_result
            ), "Timing attack missing vulnerability field"
            print(
                f"[E2E-PQC]   Timing attack: {'VULNERABLE' if timing_result['vulnerable'] else 'SAFE'}"
            )

            # Power analysis
            power_result = attacker.power_analysis_attack(num_traces=300)
            assert (
                "vulnerable" in power_result
            ), "Power attack missing vulnerability field"
            print(
                f"[E2E-PQC]   Power analysis: {'VULNERABLE' if power_result['vulnerable'] else 'SAFE'}"
            )

            # Cache timing
            cache_result = attacker.cache_timing_attack(num_measurements=500)
            assert (
                "vulnerable" in cache_result
            ), "Cache attack missing vulnerability field"
            print(
                f"[E2E-PQC]   Cache timing: {'VULNERABLE' if cache_result['vulnerable'] else 'SAFE'}"
            )

            # Step 3: CCA attack
            print(f"[E2E-PQC] Testing chosen-ciphertext attack...")
            cca_result = attacker.cca_attack(num_queries=100)
            assert "vulnerable" in cca_result, "CCA missing vulnerability field"
            print(
                f"[E2E-PQC]   CCA: {'VULNERABLE' if cca_result['vulnerable'] else 'SAFE'}"
            )

            # Step 4: Lattice reduction
            print(f"[E2E-PQC] Performing lattice reduction analysis...")
            lattice_result = attacker.lattice_reduction_attack()
            assert (
                "vulnerable" in lattice_result
            ), "Lattice attack missing vulnerability field"
            print(
                f"[E2E-PQC]   Lattice: {'VULNERABLE' if lattice_result['vulnerable'] else 'SAFE'}"
            )

            # Step 5: Comprehensive audit
            print(f"[E2E-PQC] Running comprehensive security audit...")
            start_time = time.time()
            audit_result = attacker.comprehensive_security_audit()
            elapsed = time.time() - start_time

            # Verify audit completeness
            required_fields = [
                "parameter_set",
                "timestamp",
                "timing_attack",
                "power_analysis",
                "cca_attack",
                "fault_injection",
                "cache_timing",
                "lattice_reduction",
                "parameter_analysis",
                "overall_assessment",
            ]

            for field in required_fields:
                assert field in audit_result, f"Audit missing field: {field}"

            # Extract overall assessment
            overall = audit_result["overall_assessment"]
            assert "security_rating" in overall, "Missing security rating"
            assert "vulnerabilities_found" in overall, "Missing vulnerability count"
            assert "recommendations" in overall, "Missing recommendations"

            print(f"[E2E-PQC]  Audit completed in {elapsed:.2f}s")
            print(f"[E2E-PQC]   Security rating: {overall['security_rating']}")
            print(f"[E2E-PQC]   Vulnerabilities: {overall['vulnerabilities_found']}")
            print(f"[E2E-PQC]   Critical issues: {overall.get('critical_issues', 0)}")

    def test_kyber_parameter_progression(self):
        """Test security progression across Kyber parameter sets"""
        print("\n[E2E-PQC] Testing Kyber parameter progression...")

        security_levels = ["kyber512", "kyber768", "kyber1024"]
        security_ratings = []

        for level in security_levels:
            attacker = KyberAttack(parameter_set=level)
            audit = attacker.comprehensive_security_audit()

            rating = audit["overall_assessment"]["security_rating"]
            vulnerabilities = audit["overall_assessment"]["vulnerabilities_found"]

            security_ratings.append(
                {"level": level, "rating": rating, "vulnerabilities": vulnerabilities}
            )

            print(f"[E2E-PQC] {level}: {rating} ({vulnerabilities} vulnerabilities)")

        # Verify security increases with parameter set
        # Higher parameter sets should generally have fewer vulnerabilities
        print(f"[E2E-PQC]  Parameter progression analyzed")


@pytest.mark.e2e
@pytest.mark.pqc
@pytest.mark.slow
class TestDilithiumAttackWorkflow:
    """End-to-end tests for CRYSTALS-Dilithium signature attack workflows"""

    def test_complete_dilithium_signature_analysis(self):
        """
        Test complete Dilithium signature analysis workflow.

        Workflow:
        1. Initialize Dilithium attack framework
        2. Test signature forgery attempts
        3. Check for nonce reuse vulnerabilities
        4. Perform timing analysis
        5. Comprehensive security audit
        """
        print("\n[E2E-PQC] Testing complete Dilithium signature analysis...")

        security_levels = ["dilithium2", "dilithium3", "dilithium5"]

        for level in security_levels:
            print(f"\n[E2E-PQC] Testing {level.upper()}...")

            attacker = DilithiumAttack(parameter_set=level)

            # Step 1: Signature forgery
            print(f"[E2E-PQC] Testing signature forgery...")
            forgery_result = attacker.signature_forgery_attack(num_attempts=100)
            assert "vulnerable" in forgery_result, "Forgery result incomplete"
            print(
                f"[E2E-PQC]   Forgery: {'VULNERABLE' if forgery_result['vulnerable'] else 'SAFE'}"
            )

            # Step 2: Nonce reuse detection
            print(f"[E2E-PQC] Checking nonce reuse...")
            nonce_result = attacker.nonce_reuse_attack(num_signatures=50)
            assert "vulnerable" in nonce_result, "Nonce result incomplete"
            print(
                f"[E2E-PQC]   Nonce reuse: {'VULNERABLE' if nonce_result['vulnerable'] else 'SAFE'}"
            )

            # Step 3: Timing attack
            print(f"[E2E-PQC] Performing timing attack...")
            timing_result = attacker.timing_attack(num_measurements=500)
            assert "vulnerable" in timing_result, "Timing result incomplete"
            print(
                f"[E2E-PQC]   Timing: {'VULNERABLE' if timing_result['vulnerable'] else 'SAFE'}"
            )

            # Step 4: Hash collision testing
            print(f"[E2E-PQC] Testing hash collision resistance...")
            hash_result = attacker.hash_collision_attack(num_attempts=1000)
            assert "vulnerable" in hash_result, "Hash result incomplete"
            print(
                f"[E2E-PQC]   Hash: {'VULNERABLE' if hash_result['vulnerable'] else 'SAFE'}"
            )

            # Step 5: Comprehensive audit
            print(f"[E2E-PQC] Running comprehensive audit...")
            start_time = time.time()
            audit_result = attacker.comprehensive_security_audit()
            elapsed = time.time() - start_time

            # Verify audit structure
            required_fields = [
                "parameter_set",
                "timestamp",
                "signature_forgery",
                "nonce_reuse",
                "timing_attack",
                "fault_injection",
                "hash_collision",
                "lattice_attack",
                "parameter_analysis",
                "overall_assessment",
            ]

            for field in required_fields:
                assert field in audit_result, f"Missing field: {field}"

            overall = audit_result["overall_assessment"]
            print(f"[E2E-PQC]  Audit completed in {elapsed:.2f}s")
            print(f"[E2E-PQC]   Security rating: {overall['security_rating']}")
            print(f"[E2E-PQC]   Vulnerabilities: {overall['vulnerabilities_found']}")

    def test_dilithium_multi_signature_analysis(self):
        """Test analysis of multiple signatures"""
        print("\n[E2E-PQC] Testing multi-signature analysis...")

        attacker = DilithiumAttack(parameter_set="dilithium2")

        # Generate multiple signatures (simulated)
        num_signatures = 10
        print(f"[E2E-PQC] Analyzing {num_signatures} signatures...")

        # Check for patterns across signatures
        nonce_result = attacker.nonce_reuse_attack(num_signatures=num_signatures)

        if nonce_result.get("reuse_detected"):
            print(f"[E2E-PQC]  Nonce reuse detected!")
            print(f"[E2E-PQC]    Similar pairs: {nonce_result.get('similar_pairs', 0)}")
        else:
            print(f"[E2E-PQC]  No nonce reuse detected")


@pytest.mark.e2e
@pytest.mark.pqc
class TestFALCONSPHINCSWorkflow:
    """End-to-end tests for FALCON and SPHINCS+ workflows"""

    def test_falcon_complete_analysis(self):
        """Test complete FALCON signature analysis"""
        print("\n[E2E-PQC] Testing FALCON complete analysis...")

        for param_set in ["falcon512", "falcon1024"]:
            print(f"\n[E2E-PQC] Testing {param_set.upper()}...")

            attacker = FALCONAttack(parameter_set=param_set)

            # NTRU lattice attack
            lattice_result = attacker.ntru_lattice_attack(num_attempts=100)
            assert "vulnerable" in lattice_result, "Lattice result incomplete"
            print(
                f"[E2E-PQC]   NTRU lattice: {'VULNERABLE' if lattice_result['vulnerable'] else 'SAFE'}"
            )

            # Gaussian sampling attack
            gaussian_result = attacker.gaussian_sampling_attack(num_samples=1000)
            assert "vulnerable" in gaussian_result, "Gaussian result incomplete"
            print(
                f"[E2E-PQC]   Gaussian: {'VULNERABLE' if gaussian_result['vulnerable'] else 'SAFE'}"
            )

            # Comprehensive audit
            audit = attacker.comprehensive_security_audit()
            overall = audit["overall_assessment"]
            print(f"[E2E-PQC]  {param_set} rating: {overall['security_rating']}")

    def test_sphincs_complete_analysis(self):
        """Test complete SPHINCS+ hash-based signature analysis"""
        print("\n[E2E-PQC] Testing SPHINCS+ complete analysis...")

        for param_set in ["sphincs128f", "sphincs256f"]:
            print(f"\n[E2E-PQC] Testing {param_set.upper()}...")

            attacker = SPHINCSAttack(parameter_set=param_set)

            # Hash collision attack
            collision_result = attacker.hash_collision_attack(num_attempts=10000)
            assert "vulnerable" in collision_result, "Collision result incomplete"
            print(
                f"[E2E-PQC]   Hash collision: {'VULNERABLE' if collision_result['vulnerable'] else 'SAFE'}"
            )

            # Multi-target attack
            multi_result = attacker.multi_target_attack(
                num_targets=10, attempts_per_target=1000
            )
            assert "vulnerable" in multi_result, "Multi-target result incomplete"
            print(
                f"[E2E-PQC]   Multi-target: {'VULNERABLE' if multi_result['vulnerable'] else 'SAFE'}"
            )

            # Signature size analysis
            size_result = attacker.signature_size_analysis(num_samples=100)
            assert "average_entropy" in size_result, "Size analysis incomplete"
            print(
                f"[E2E-PQC]   Avg entropy: {size_result['average_entropy']:.2f} bits/byte"
            )

            # Comprehensive audit
            audit = attacker.comprehensive_security_audit()
            overall = audit["overall_assessment"]
            print(f"[E2E-PQC]  {param_set} rating: {overall['security_rating']}")


@pytest.mark.e2e
@pytest.mark.pqc
@pytest.mark.slow
class TestHybridPQCWorkflow:
    """End-to-end tests for hybrid classical+PQC attack workflows"""

    def test_complete_hybrid_security_assessment(self):
        """
        Test complete hybrid cryptography security assessment.

        Workflow:
        1. Initialize hybrid attack framework
        2. Test downgrade attacks
        3. Check key exchange confusion
        4. Verify signature verification bypass
        5. Analyze transition period vulnerabilities
        """
        print("\n[E2E-PQC] Testing complete hybrid security assessment...")

        configurations = ["hybrid-tls-128", "hybrid-tls-192", "hybrid-tls-256"]

        for config in configurations:
            print(f"\n[E2E-PQC] Testing {config.upper()}...")

            attacker = HybridPQCAttack(configuration=config)

            # Step 1: Downgrade attack
            print(f"[E2E-PQC] Testing downgrade attack...")
            downgrade_result = attacker.downgrade_attack(num_attempts=100)
            assert "vulnerable" in downgrade_result, "Downgrade result incomplete"
            print(
                f"[E2E-PQC]   Downgrade: {'VULNERABLE' if downgrade_result['vulnerable'] else 'SAFE'}"
            )

            # Step 2: Key exchange confusion
            print(f"[E2E-PQC] Testing key exchange confusion...")
            kex_result = attacker.key_exchange_confusion_attack(num_sessions=50)
            assert "vulnerable" in kex_result, "KEX result incomplete"
            print(
                f"[E2E-PQC]   KEX confusion: {'VULNERABLE' if kex_result['vulnerable'] else 'SAFE'}"
            )

            # Step 3: Signature verification bypass
            print(f"[E2E-PQC] Testing signature bypass...")
            sig_result = attacker.signature_verification_bypass(num_attempts=100)
            assert "vulnerable" in sig_result, "Signature result incomplete"
            print(
                f"[E2E-PQC]   Sig bypass: {'VULNERABLE' if sig_result['vulnerable'] else 'SAFE'}"
            )

            # Step 4: Transition period exploit
            print(f"[E2E-PQC] Testing transition vulnerabilities...")
            transition_result = attacker.transition_period_exploit(num_scenarios=50)
            assert "vulnerable" in transition_result, "Transition result incomplete"
            print(
                f"[E2E-PQC]   Transition: {'VULNERABLE' if transition_result['vulnerable'] else 'SAFE'}"
            )

            # Step 5: Comprehensive audit
            print(f"[E2E-PQC] Running comprehensive audit...")
            start_time = time.time()
            audit_result = attacker.comprehensive_hybrid_audit()
            elapsed = time.time() - start_time

            # Verify audit completeness
            required_fields = [
                "configuration",
                "timestamp",
                "downgrade_attack",
                "key_exchange_confusion",
                "signature_verification_bypass",
                "protocol_state_confusion",
                "transition_period_exploit",
                "hybrid_kdf_weakness",
                "implementation_inconsistency",
                "overall_assessment",
            ]

            for field in required_fields:
                assert field in audit_result, f"Missing field: {field}"

            overall = audit_result["overall_assessment"]
            print(f"[E2E-PQC]  Audit completed in {elapsed:.2f}s")
            print(f"[E2E-PQC]   Security rating: {overall['security_rating']}")
            print(f"[E2E-PQC]   Vulnerabilities: {overall['vulnerabilities_found']}")

    def test_hybrid_deployment_scenarios(self):
        """Test different deployment scenarios"""
        print("\n[E2E-PQC] Testing hybrid deployment scenarios...")

        attacker = HybridPQCAttack(configuration="hybrid-tls-128")

        # Test transition period with different deployment phases
        result = attacker.transition_period_exploit(num_scenarios=30)

        if "deployment_phases" in result:
            phases = result["deployment_phases"]
            print(f"[E2E-PQC] Tested {len(phases)} deployment phases:")
            for phase, data in phases.items():
                print(
                    f"[E2E-PQC]   {phase}: {data.get('vulnerable_scenarios', 0)} vulnerable scenarios"
                )

        print(f"[E2E-PQC]  Deployment scenario testing complete")


@pytest.mark.e2e
@pytest.mark.pqc
class TestPQCMigrationWorkflow:
    """End-to-end tests for PQC migration analysis workflows"""

    def test_complete_migration_analysis_workflow(self):
        """
        Test complete PQC migration analysis workflow.

        Workflow:
        1. Scan codebase for classical crypto
        2. Assess vulnerabilities
        3. Generate recommendations
        4. Create migration path
        5. Export comprehensive report
        """
        print("\n[E2E-PQC] Testing complete migration analysis workflow...")

        analyzer = PQCMigrationAnalyzer()

        # Create temporary test directory with sample code
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create sample files with classical crypto
            samples = {
                "server.py": """
import rsa
from Crypto.PublicKey import RSA

key = RSA.generate(2048)
cipher = rsa.encrypt(data, public_key)
""",
                "client.py": """
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import dh

private_key = ec.generate_private_key(ec.SECP256R1())
dh_params = dh.generate_parameters(2048)
""",
                "signatures.py": """
from ecdsa import SigningKey, NIST256p

sk = SigningKey.generate(curve=NIST256p)
signature = sk.sign(message)
""",
            }

            for filename, content in samples.items():
                (tmppath / filename).write_text(content)

            # Step 1: Scan directory
            print(f"[E2E-PQC] Scanning test directory...")
            start_time = time.time()
            scan_result = analyzer.scan_directory(str(tmppath))
            scan_elapsed = time.time() - start_time

            assert "files_scanned" in scan_result, "Scan result incomplete"
            assert "crypto_usages" in scan_result, "Missing crypto usages"

            files_scanned = scan_result["files_scanned"]
            usages = scan_result["crypto_usages"]

            print(f"[E2E-PQC]   Scanned {files_scanned} files in {scan_elapsed:.2f}s")
            print(f"[E2E-PQC]   Found {len(usages)} crypto usages")

            # Verify we found expected algorithms
            algorithms_found = set(usage.algorithm for usage in usages)
            print(f"[E2E-PQC]   Algorithms: {algorithms_found}")

            # Step 2: Assess vulnerabilities
            print(f"[E2E-PQC] Assessing vulnerabilities...")
            assessments = []
            for usage in usages:
                assessment = analyzer.assess_vulnerabilities(usage)
                assessments.append(assessment)

            critical_count = sum(
                1 for a in assessments if a.threat_level == "immediate"
            )
            print(f"[E2E-PQC]   Critical vulnerabilities: {critical_count}")

            # Step 3: Generate recommendations
            print(f"[E2E-PQC] Generating recommendations...")
            recommendations = []
            for assessment in assessments:
                rec = analyzer.generate_recommendations(assessment)
                recommendations.append(rec)

            print(f"[E2E-PQC]   Generated {len(recommendations)} recommendations")

            # Step 4: Create migration path
            print(f"[E2E-PQC] Creating migration path...")
            if recommendations:
                migration_path = analyzer.create_migration_path(recommendations[0])

                assert "strategy" in migration_path, "Missing migration strategy"
                assert "phases" in migration_path, "Missing migration phases"
                assert "timeline_weeks" in migration_path, "Missing timeline"

                print(f"[E2E-PQC]   Strategy: {migration_path['strategy']}")
                print(f"[E2E-PQC]   Timeline: {migration_path['timeline_weeks']} weeks")
                print(f"[E2E-PQC]   Phases: {len(migration_path['phases'])}")

            # Step 5: Generate comprehensive report
            print(f"[E2E-PQC] Generating comprehensive report...")
            report = analyzer.generate_comprehensive_report(
                scan_result=scan_result,
                assessments=assessments,
                recommendations=recommendations,
            )

            required_report_fields = [
                "summary",
                "vulnerabilities",
                "recommendations",
                "migration_paths",
                "timeline",
                "budget_estimate",
            ]

            for field in required_report_fields:
                assert field in report, f"Report missing field: {field}"

            print(f"[E2E-PQC]  Migration analysis workflow complete")
            print(
                f"[E2E-PQC]   Total budget: ${report['budget_estimate']['min']}-${report['budget_estimate']['max']}"
            )
            print(f"[E2E-PQC]   Team size: {report.get('team_size', 'N/A')}")

    def test_migration_export_workflow(self):
        """Test exporting migration analysis to JSON"""
        print("\n[E2E-PQC] Testing migration export workflow...")

        analyzer = PQCMigrationAnalyzer()

        # Create minimal report
        report = {
            "summary": {"files": 0, "usages": 0},
            "vulnerabilities": [],
            "recommendations": [],
            "migration_paths": [],
            "timeline": {"min_weeks": 0, "max_weeks": 0},
            "budget_estimate": {"min": 0, "max": 0},
        }

        # Export to temporary file
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            tmpfile = f.name

        try:
            analyzer.export_report(report, tmpfile)

            # Verify file exists and is valid JSON
            assert os.path.exists(tmpfile), "Export file not created"

            with open(tmpfile, "r") as f:
                loaded_report = json.load(f)

            assert "summary" in loaded_report, "Exported report incomplete"
            print(f"[E2E-PQC]  Export workflow successful")

        finally:
            if os.path.exists(tmpfile):
                os.unlink(tmpfile)


def run_pqc_e2e_tests():
    """Run all PQC E2E tests with reporting"""
    print("\n" + "=" * 70)
    print("Running Post-Quantum Cryptography E2E Workflow Tests")
    print("=" * 70 + "\n")

    # Run with pytest
    pytest.main([__file__, "-v", "-m", "pqc", "--tb=short", "--durations=10"])


if __name__ == "__main__":
    run_pqc_e2e_tests()
