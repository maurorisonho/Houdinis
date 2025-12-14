#!/usr/bin/env python3
"""
Integration Tests for Quantum Machine Learning Attacks
======================================================

Integration tests for QML attack frameworks, testing interactions
between QML attacks and other system components.

Author: Houdinis Framework
License: MIT
"""

import pytest
import sys
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from exploits.qml_adversarial import QMLAdversarialAttack
from exploits.qml_gan import QuantumGANAttack
from exploits.qml_qsvm import QSVMAttack
from exploits.qml_transfer_learning import QuantumTransferLearningAttack
from quantum.backend import QuantumBackend


@pytest.mark.integration
@pytest.mark.qml
class TestQMLAdversarialIntegration:
    """Integration tests for QML adversarial attacks"""
    
    def test_adversarial_with_backend(self):
        """Test adversarial attack with quantum backend"""
        backend = QuantumBackend(backend_type='simulator')
        attacker = QMLAdversarialAttack(backend=backend)
        
        # Create simple dataset
        X = np.random.rand(10, 4)
        y = np.random.randint(0, 2, 10)
        
        result = attacker.fgsm_attack(X, y, epsilon=0.1)
        
        assert 'adversarial_examples' in result
        assert 'success_rate' in result
    
    def test_adversarial_pgd_integration(self):
        """Test PGD attack integration"""
        backend = QuantumBackend(backend_type='simulator')
        attacker = QMLAdversarialAttack(backend=backend)
        
        X = np.random.rand(5, 4)
        y = np.random.randint(0, 2, 5)
        
        result = attacker.pgd_attack(X, y, epsilon=0.1, alpha=0.01, iterations=5)
        
        assert 'adversarial_examples' in result
        assert 'attack_iterations' in result


@pytest.mark.integration
@pytest.mark.qml
class TestQMLGANIntegration:
    """Integration tests for Quantum GAN attacks"""
    
    def test_gan_with_backend(self):
        """Test GAN attack with quantum backend"""
        backend = QuantumBackend(backend_type='simulator')
        attacker = QuantumGANAttack(backend=backend)
        
        # Simple training data
        training_data = np.random.rand(20, 4)
        
        result = attacker.generate_synthetic_attacks(
            training_data,
            num_samples=5,
            training_iterations=10
        )
        
        assert 'synthetic_samples' in result
        assert 'quality_score' in result
    
    def test_gan_mode_collapse_detection(self):
        """Test mode collapse detection in GAN"""
        backend = QuantumBackend(backend_type='simulator')
        attacker = QuantumGANAttack(backend=backend)
        
        training_data = np.random.rand(15, 4)
        
        result = attacker.detect_mode_collapse(
            training_data,
            num_samples=10,
            diversity_threshold=0.5
        )
        
        assert 'mode_collapse_detected' in result
        assert isinstance(result['mode_collapse_detected'], bool)


@pytest.mark.integration
@pytest.mark.qml
class TestQSVMIntegration:
    """Integration tests for QSVM attacks"""
    
    def test_qsvm_with_backend(self):
        """Test QSVM attack with quantum backend"""
        backend = QuantumBackend(backend_type='simulator')
        attacker = QSVMAttack(backend=backend)
        
        # Create simple dataset
        X_train = np.random.rand(20, 4)
        y_train = np.random.randint(0, 2, 20)
        X_test = np.random.rand(5, 4)
        
        result = attacker.kernel_attack(X_train, y_train, X_test)
        
        assert 'vulnerable' in result
        assert isinstance(result['vulnerable'], bool)
    
    def test_qsvm_boundary_attack_integration(self):
        """Test boundary attack integration"""
        backend = QuantumBackend(backend_type='simulator')
        attacker = QSVMAttack(backend=backend)
        
        X_train = np.random.rand(15, 4)
        y_train = np.random.randint(0, 2, 15)
        X_test = np.random.rand(3, 4)
        y_test = np.random.randint(0, 2, 3)
        
        result = attacker.boundary_attack(X_train, y_train, X_test, y_test)
        
        assert 'vulnerable' in result
        assert 'misclassified_samples' in result


@pytest.mark.integration
@pytest.mark.qml
class TestQuantumTransferLearningIntegration:
    """Integration tests for quantum transfer learning attacks"""
    
    def test_transfer_learning_with_backend(self):
        """Test transfer learning attack with quantum backend"""
        backend = QuantumBackend(backend_type='simulator')
        attacker = QuantumTransferLearningAttack(backend=backend)
        
        # Source domain data
        X_source = np.random.rand(20, 4)
        y_source = np.random.randint(0, 2, 20)
        
        # Target domain data
        X_target = np.random.rand(10, 4)
        y_target = np.random.randint(0, 2, 10)
        
        result = attacker.domain_adaptation_attack(
            X_source, y_source, X_target, y_target
        )
        
        assert 'vulnerable' in result
        assert 'transfer_success_rate' in result
    
    def test_backdoor_attack_integration(self):
        """Test backdoor attack integration"""
        backend = QuantumBackend(backend_type='simulator')
        attacker = QuantumTransferLearningAttack(backend=backend)
        
        X_source = np.random.rand(15, 4)
        y_source = np.random.randint(0, 2, 15)
        X_target = np.random.rand(5, 4)
        
        result = attacker.backdoor_attack(
            X_source, y_source, X_target,
            trigger_pattern=[0.9, 0.9, 0.1, 0.1]
        )
        
        assert 'backdoor_installed' in result
        assert 'activation_rate' in result


@pytest.mark.integration
@pytest.mark.qml
class TestCrossQMLAttacks:
    """Integration tests combining multiple QML attacks"""
    
    def test_adversarial_then_gan(self):
        """Test combining adversarial and GAN attacks"""
        backend = QuantumBackend(backend_type='simulator')
        
        # Step 1: Generate adversarial examples
        adversarial = QMLAdversarialAttack(backend=backend)
        X = np.random.rand(10, 4)
        y = np.random.randint(0, 2, 10)
        
        adv_result = adversarial.fgsm_attack(X, y, epsilon=0.1)
        adversarial_samples = adv_result['adversarial_examples']
        
        # Step 2: Use GAN to generate more samples based on adversarial examples
        gan = QuantumGANAttack(backend=backend)
        gan_result = gan.generate_synthetic_attacks(
            adversarial_samples,
            num_samples=5,
            training_iterations=10
        )
        
        assert 'synthetic_samples' in gan_result
        print(f"[INTEGRATION] Generated {len(gan_result['synthetic_samples'])} synthetic adversarial samples")
    
    def test_transfer_learning_with_qsvm(self):
        """Test transfer learning attack on QSVM"""
        backend = QuantumBackend(backend_type='simulator')
        
        # Train QSVM on source domain
        qsvm = QSVMAttack(backend=backend)
        X_source = np.random.rand(15, 4)
        y_source = np.random.randint(0, 2, 15)
        
        # Use transfer learning to attack
        transfer = QuantumTransferLearningAttack(backend=backend)
        X_target = np.random.rand(8, 4)
        y_target = np.random.randint(0, 2, 8)
        
        result = transfer.domain_adaptation_attack(
            X_source, y_source, X_target, y_target
        )
        
        assert 'vulnerable' in result
        print(f"[INTEGRATION] Transfer learning attack success rate: {result.get('transfer_success_rate', 0):.2f}")


@pytest.mark.integration
@pytest.mark.qml
class TestQMLWithClassicalCrypto:
    """Integration tests combining QML with classical crypto attacks"""
    
    def test_qml_enhanced_key_recovery(self):
        """Test using QML to enhance key recovery attacks"""
        backend = QuantumBackend(backend_type='simulator')
        
        # Simulate timing data from crypto operations
        timing_data = np.random.rand(50, 8)  # 50 samples, 8 features
        key_labels = np.random.randint(0, 2, 50)  # Binary classification
        
        # Use QSVM to classify timing patterns
        qsvm = QSVMAttack(backend=backend)
        
        # Split data
        X_train = timing_data[:40]
        y_train = key_labels[:40]
        X_test = timing_data[40:]
        
        result = qsvm.kernel_attack(X_train, y_train, X_test)
        
        print(f"[INTEGRATION] QML-enhanced timing analysis vulnerability: {result.get('vulnerable')}")
        assert 'vulnerable' in result


@pytest.mark.integration
@pytest.mark.qml
@pytest.mark.slow
class TestQMLPerformanceIntegration:
    """Integration tests for QML attack performance"""
    
    def test_adversarial_attack_scaling(self):
        """Test adversarial attack performance with different dataset sizes"""
        backend = QuantumBackend(backend_type='simulator')
        attacker = QMLAdversarialAttack(backend=backend)
        
        sizes = [5, 10, 20]
        results = []
        
        for size in sizes:
            X = np.random.rand(size, 4)
            y = np.random.randint(0, 2, size)
            
            result = attacker.fgsm_attack(X, y, epsilon=0.1)
            results.append({
                'size': size,
                'success_rate': result.get('success_rate', 0)
            })
        
        print("[INTEGRATION] Adversarial attack scaling:")
        for res in results:
            print(f"  Size {res['size']}: {res['success_rate']:.2f} success rate")
    
    def test_gan_training_iterations(self):
        """Test GAN attack with different training iterations"""
        backend = QuantumBackend(backend_type='simulator')
        attacker = QuantumGANAttack(backend=backend)
        
        training_data = np.random.rand(20, 4)
        iterations_list = [5, 10, 20]
        
        for iterations in iterations_list:
            result = attacker.generate_synthetic_attacks(
                training_data,
                num_samples=5,
                training_iterations=iterations
            )
            
            quality = result.get('quality_score', 0)
            print(f"[INTEGRATION] GAN with {iterations} iterations: quality = {quality:.2f}")


def run_integration_tests():
    """Run all QML integration tests"""
    print("\n" + "="*70)
    print("Running Quantum Machine Learning Integration Tests")
    print("="*70 + "\n")
    
    pytest.main([
        __file__,
        '-v',
        '-m', 'qml',
        '--tb=short'
    ])


if __name__ == '__main__':
    run_integration_tests()
