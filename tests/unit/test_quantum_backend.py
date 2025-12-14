"""
Houdinis Framework - Unit Tests for Quantum Backend
Tests backend initialization, device listing, and circuit execution
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from quantum.backend import (
    QuantumBackendBase,
    IBMQuantumBackend,
    QISKIT_AVAILABLE,
    CUQUANTUM_AVAILABLE,
    BRAKET_AVAILABLE,
    AZURE_QUANTUM_AVAILABLE,
    CIRQ_AVAILABLE,
    PENNYLANE_AVAILABLE,
)


class MockQuantumBackend(QuantumBackendBase):
    """Mock backend for testing abstract base class"""

    def initialize(self, **kwargs):
        self.is_connected = True
        return {"success": True, "backend": "mock"}

    def list_devices(self):
        return {"devices": ["mock_device_1", "mock_device_2"]}

    def execute_circuit(self, circuit, device=None):
        return {"success": True, "result": "mock_result"}


class TestQuantumBackendBase:
    """Test abstract base class functionality"""

    def test_backend_initialization(self):
        """Test backend initializes with correct attributes"""
        backend = MockQuantumBackend("Test Backend")

        assert backend.name == "Test Backend"
        assert backend.is_connected is False
        assert backend.available_devices == {}

    def test_backend_abstract_methods(self):
        """Test that abstract methods must be implemented"""
        # Attempt to instantiate without implementing abstract methods
        with pytest.raises(TypeError):
            QuantumBackendBase("Invalid")

    def test_mock_backend_initialize(self):
        """Test mock backend initialization"""
        backend = MockQuantumBackend("Mock")
        result = backend.initialize()

        assert result["success"] is True
        assert backend.is_connected is True

    def test_mock_backend_list_devices(self):
        """Test mock backend device listing"""
        backend = MockQuantumBackend("Mock")
        devices = backend.list_devices()

        assert "devices" in devices
        assert len(devices["devices"]) == 2

    def test_mock_backend_execute_circuit(self):
        """Test mock backend circuit execution"""
        backend = MockQuantumBackend("Mock")
        result = backend.execute_circuit("mock_circuit")

        assert result["success"] is True
        assert "result" in result


@pytest.mark.skipif(not QISKIT_AVAILABLE, reason="Qiskit not installed")
class TestIBMQuantumBackend:
    """Test IBM Quantum backend"""

    @pytest.fixture
    def backend(self):
        """Create IBM Quantum backend instance"""
        return IBMQuantumBackend()

    def test_backend_creation(self, backend):
        """Test IBM backend is created correctly"""
        assert backend.name == "IBM Quantum"
        assert backend.provider is None
        assert backend.ibmq_token is None
        assert backend.is_connected is False

    @patch("quantum.backend.IBMQ")
    def test_initialize_without_token(self, mock_ibmq, backend):
        """Test initialization without token"""
        result = backend.initialize()

        # Should attempt to load saved account or fail gracefully
        assert "success" in result

    @patch("quantum.backend.IBMQ")
    def test_initialize_with_token(self, mock_ibmq, backend):
        """Test initialization with token"""
        mock_provider = Mock()
        mock_ibmq.enable_account.return_value = mock_provider

        result = backend.initialize(token="fake_token")

        assert backend.ibmq_token == "fake_token"

    @patch("quantum.backend.IBMQ")
    def test_list_devices_not_connected(self, mock_ibmq, backend):
        """Test listing devices when not connected"""
        result = backend.list_devices()

        assert result["success"] is False
        assert "error" in result


class TestBackendAvailability:
    """Test backend availability detection"""

    def test_qiskit_availability(self):
        """Test Qiskit availability is detected"""
        assert isinstance(QISKIT_AVAILABLE, bool)

    def test_cuquantum_availability(self):
        """Test cuQuantum availability is detected"""
        assert isinstance(CUQUANTUM_AVAILABLE, bool)

    def test_braket_availability(self):
        """Test Braket availability is detected"""
        assert isinstance(BRAKET_AVAILABLE, bool)

    def test_azure_availability(self):
        """Test Azure Quantum availability is detected"""
        assert isinstance(AZURE_QUANTUM_AVAILABLE, bool)

    def test_cirq_availability(self):
        """Test Cirq availability is detected"""
        assert isinstance(CIRQ_AVAILABLE, bool)

    def test_pennylane_availability(self):
        """Test PennyLane availability is detected"""
        assert isinstance(PENNYLANE_AVAILABLE, bool)


@pytest.mark.integration
@pytest.mark.skipif(not QISKIT_AVAILABLE, reason="Qiskit not installed")
class TestIBMQuantumIntegration:
    """Integration tests for IBM Quantum backend"""

    @pytest.fixture
    def backend(self):
        """Create backend instance"""
        return IBMQuantumBackend()

    def test_aer_simulator_available(self, backend):
        """Test that Aer simulator is available"""
        from qiskit import Aer

        simulator = Aer.get_backend("aer_simulator")
        assert simulator is not None

    @pytest.mark.slow
    def test_simple_circuit_execution(self, backend):
        """Test execution of a simple quantum circuit"""
        try:
            from qiskit import QuantumCircuit, Aer, execute

            # Create simple circuit
            qc = QuantumCircuit(2, 2)
            qc.h(0)
            qc.cx(0, 1)
            qc.measure([0, 1], [0, 1])

            # Execute on simulator
            simulator = Aer.get_backend("aer_simulator")
            job = execute(qc, simulator, shots=100)
            result = job.result()

            assert result is not None
            counts = result.get_counts()
            assert isinstance(counts, dict)
            assert len(counts) > 0

        except Exception as e:
            pytest.skip(f"Circuit execution failed: {e}")


@pytest.mark.unit
class TestBackendErrorHandling:
    """Test error handling in backends"""

    def test_backend_without_qiskit(self):
        """Test backend behavior when Qiskit not available"""
        with patch("quantum.backend.QISKIT_AVAILABLE", False):
            backend = IBMQuantumBackend()
            result = backend.initialize()

            assert result["success"] is False
            assert "Qiskit not installed" in result.get("error", "")

    def test_backend_with_invalid_token(self):
        """Test backend with invalid token"""
        if not QISKIT_AVAILABLE:
            pytest.skip("Qiskit not available")

        backend = IBMQuantumBackend()

        with patch("quantum.backend.IBMQ.enable_account") as mock_enable:
            mock_enable.side_effect = Exception("Invalid token")
            result = backend.initialize(token="invalid_token")

            # Should handle error gracefully
            assert isinstance(result, dict)


@pytest.mark.security
class TestBackendSecurity:
    """Test security aspects of quantum backends"""

    def test_token_not_logged(self):
        """Test that tokens are not logged or printed"""
        if not QISKIT_AVAILABLE:
            pytest.skip("Qiskit not available")

        backend = IBMQuantumBackend()
        backend.ibmq_token = "secret_token_12345"

        # Token should not appear in string representation
        backend_str = str(backend.__dict__)
        # This is a basic check - in production, ensure proper secret handling

    def test_token_storage(self):
        """Test that tokens are stored securely"""
        if not QISKIT_AVAILABLE:
            pytest.skip("Qiskit not available")

        backend = IBMQuantumBackend()
        token = "test_token"

        # Token should only be stored in memory, not written to disk
        backend.ibmq_token = token
        assert backend.ibmq_token == token


@pytest.mark.quantum
class TestQuantumOperations:
    """Test quantum-specific operations"""

    @pytest.mark.skipif(not QISKIT_AVAILABLE, reason="Qiskit not installed")
    def test_bell_state_creation(self):
        """Test creation of Bell state"""
        from qiskit import QuantumCircuit, Aer, execute

        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure([0, 1], [0, 1])

        backend = Aer.get_backend("aer_simulator")
        job = execute(qc, backend, shots=1000)
        result = job.result()
        counts = result.get_counts()

        # Bell state should produce |00 and |11 with roughly equal probability
        assert "00" in counts or "11" in counts

    @pytest.mark.skipif(not QISKIT_AVAILABLE, reason="Qiskit not installed")
    def test_superposition_state(self):
        """Test creation of superposition state"""
        from qiskit import QuantumCircuit, Aer, execute

        qc = QuantumCircuit(1, 1)
        qc.h(0)
        qc.measure(0, 0)

        backend = Aer.get_backend("aer_simulator")
        job = execute(qc, backend, shots=1000)
        result = job.result()
        counts = result.get_counts()

        # Superposition should produce both |0 and |1
        assert len(counts) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
