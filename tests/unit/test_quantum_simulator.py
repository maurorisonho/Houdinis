"""
Houdinis Framework - Unit Tests for Quantum Simulator
Tests classical quantum simulation functionality
"""

import pytest
import sys
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from quantum.simulator import QuantumSimulator


class TestQuantumSimulatorInitialization:
    """Test quantum simulator initialization"""
    
    def test_default_initialization(self):
        """Test simulator with default parameters"""
        sim = QuantumSimulator()
        
        assert sim.num_qubits == 10
        assert sim.max_qubits == 20
    
    def test_custom_qubits(self):
        """Test simulator with custom qubit count"""
        sim = QuantumSimulator(num_qubits=15)
        
        assert sim.num_qubits == 15
        assert sim.max_qubits == 20
    
    def test_max_qubits_limit(self):
        """Test that max_qubits is reasonable"""
        sim = QuantumSimulator()
        
        # Should be limited for classical simulation
        assert sim.max_qubits <= 25


class TestShorsPeriodFinding:
    """Test Shor's algorithm period finding simulation"""
    
    @pytest.fixture
    def simulator(self):
        """Create simulator instance"""
        return QuantumSimulator()
    
    def test_period_finding_small_numbers(self, simulator):
        """Test period finding with small numbers"""
        N = 15
        a = 7
        
        result = simulator.simulate_shors_period_finding(N, a)
        
        assert result['success'] is True
        assert 'period' in result
        assert result['period'] > 0
        assert 'measurements' in result
        assert result['method'] == 'classical_simulation'
    
    def test_period_finding_returns_qubits_used(self, simulator):
        """Test that result includes qubits used"""
        N = 21
        a = 5
        
        result = simulator.simulate_shors_period_finding(N, a)
        
        assert 'qubits_used' in result
        expected_qubits = math.ceil(math.log2(N)) * 2
        assert result['qubits_used'] == expected_qubits
    
    def test_period_finding_measurements(self, simulator):
        """Test that measurements are included"""
        N = 15
        a = 7
        
        result = simulator.simulate_shors_period_finding(N, a)
        
        assert 'measurements' in result
        assert isinstance(result['measurements'], (list, dict))
        assert 'shots' in result
        assert result['shots'] == 1024
    
    def test_period_finding_coprime(self, simulator):
        """Test period finding with coprime numbers"""
        N = 15
        a = 2  # coprime to 15
        
        result = simulator.simulate_shors_period_finding(N, a)
        
        # Should find a valid period
        if result['success']:
            period = result['period']
            assert period > 0
            # Verify: a^period ≡ 1 (mod N)
            assert pow(a, period, N) == 1


class TestGroversSearch:
    """Test Grover's search algorithm simulation"""
    
    @pytest.fixture
    def simulator(self):
        """Create simulator instance"""
        return QuantumSimulator()
    
    def test_grover_small_database(self, simulator):
        """Test Grover's search on small database"""
        database_size = 16
        target_items = [7]
        
        result = simulator.simulate_grovers_search(database_size, target_items)
        
        assert result['success'] is True
        assert 'iterations' in result
        assert 'qubits_used' in result
        assert result['qubits_used'] == math.ceil(math.log2(database_size))
    
    def test_grover_optimal_iterations(self, simulator):
        """Test that optimal iterations are calculated correctly"""
        database_size = 64
        target_items = [42]
        
        result = simulator.simulate_grovers_search(database_size, target_items)
        
        expected_iterations = math.floor(
            math.pi/4 * math.sqrt(database_size / len(target_items))
        )
        assert result['iterations'] == expected_iterations
    
    def test_grover_multiple_targets(self, simulator):
        """Test Grover's search with multiple targets"""
        database_size = 32
        target_items = [5, 10, 15]
        
        result = simulator.simulate_grovers_search(database_size, target_items)
        
        assert result['success'] is True
        # With multiple targets, fewer iterations needed
        assert result['iterations'] > 0
    
    def test_grover_database_too_large(self, simulator):
        """Test error handling for database too large"""
        database_size = 2**25  # Larger than max_qubits
        target_items = [0]
        
        result = simulator.simulate_grovers_search(database_size, target_items)
        
        assert result['success'] is False
        assert 'error' in result
        assert 'too large' in result['error'].lower()
    
    def test_grover_results_format(self, simulator):
        """Test that results are in correct format"""
        database_size = 8
        target_items = [3]
        
        result = simulator.simulate_grovers_search(database_size, target_items)
        
        if result['success']:
            # Should have measurement statistics
            assert 'iterations' in result
            assert 'qubits_used' in result
            assert isinstance(result['qubits_used'], int)


class TestSimulatorHelperMethods:
    """Test simulator helper methods"""
    
    @pytest.fixture
    def simulator(self):
        """Create simulator instance"""
        return QuantumSimulator()
    
    def test_find_period_classical(self, simulator):
        """Test classical period finding helper"""
        # This tests the internal _find_period_classical method
        N = 15
        a = 7
        
        # Call the simulation which uses the helper
        result = simulator.simulate_shors_period_finding(N, a)
        
        if result['success']:
            period = result['period']
            # Verify it's a valid period
            assert pow(a, period, N) == 1
    
    def test_simulate_period_measurements(self, simulator):
        """Test period measurement simulation"""
        N = 15
        a = 7
        
        result = simulator.simulate_shors_period_finding(N, a)
        
        # Should produce measurements
        assert 'measurements' in result
        measurements = result['measurements']
        
        # Measurements should be related to the period
        if isinstance(measurements, dict):
            assert len(measurements) > 0


@pytest.mark.quantum
class TestQuantumAlgorithmProperties:
    """Test quantum algorithm properties"""
    
    @pytest.fixture
    def simulator(self):
        """Create simulator instance"""
        return QuantumSimulator()
    
    def test_shor_quadratic_speedup(self, simulator):
        """Test that Shor's provides theoretical speedup"""
        # For small N, verify qubits needed
        N = 15
        a = 7
        
        result = simulator.simulate_shors_period_finding(N, a)
        qubits = result['qubits_used']
        
        # Qubits should be O(log N)
        expected = math.ceil(math.log2(N)) * 2
        assert qubits == expected
    
    def test_grover_quadratic_speedup(self, simulator):
        """Test that Grover's provides quadratic speedup"""
        database_size = 256
        target_items = [42]
        
        result = simulator.simulate_grovers_search(database_size, target_items)
        iterations = result['iterations']
        
        # Grover's needs O(√N) iterations
        expected = math.floor(math.pi/4 * math.sqrt(database_size))
        assert iterations == expected
        
        # Classical would need O(N) iterations
        assert iterations < database_size


@pytest.mark.unit
class TestSimulatorEdgeCases:
    """Test edge cases and error conditions"""
    
    @pytest.fixture
    def simulator(self):
        """Create simulator instance"""
        return QuantumSimulator()
    
    def test_period_finding_N_equals_1(self, simulator):
        """Test period finding with N=1"""
        result = simulator.simulate_shors_period_finding(1, 1)
        
        # Should handle gracefully
        assert isinstance(result, dict)
    
    def test_period_finding_a_equals_1(self, simulator):
        """Test period finding with a=1"""
        result = simulator.simulate_shors_period_finding(15, 1)
        
        # a=1 has period 1 for any N
        if result['success']:
            assert result['period'] == 1
    
    def test_grover_empty_targets(self, simulator):
        """Test Grover's with empty target list"""
        database_size = 16
        target_items = []
        
        # Should either handle gracefully or raise error
        try:
            result = simulator.simulate_grovers_search(database_size, target_items)
            # If it succeeds, should have some result
            assert isinstance(result, dict)
        except (ValueError, ZeroDivisionError):
            # Expected for empty targets
            pass
    
    def test_grover_database_size_zero(self, simulator):
        """Test Grover's with database size 0"""
        try:
            result = simulator.simulate_grovers_search(0, [0])
            assert isinstance(result, dict)
        except (ValueError, ZeroDivisionError):
            # Expected for invalid database size
            pass


@pytest.mark.performance
class TestSimulatorPerformance:
    """Test simulator performance characteristics"""
    
    @pytest.fixture
    def simulator(self):
        """Create simulator instance"""
        return QuantumSimulator()
    
    def test_large_number_factoring(self, simulator):
        """Test period finding for larger numbers"""
        N = 21
        a = 2
        
        import time
        start = time.time()
        result = simulator.simulate_shors_period_finding(N, a)
        elapsed = time.time() - start
        
        # Should complete in reasonable time
        assert elapsed < 5.0  # 5 seconds
        assert result['success'] is True
    
    def test_grover_scaling(self, simulator):
        """Test Grover's algorithm scaling"""
        # Test with increasing database sizes
        sizes = [8, 16, 32, 64]
        
        for size in sizes:
            result = simulator.simulate_grovers_search(size, [0])
            
            # Should complete successfully
            assert result['success'] is True
            
            # Iterations should scale as √N
            expected = math.floor(math.pi/4 * math.sqrt(size))
            assert result['iterations'] == expected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
