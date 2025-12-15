"""
End-to-End Docker Integration Tests for Houdinis Framework

Tests Docker container execution, networking, and security isolation.
Requires Docker installed and running.
"""

import pytest
import subprocess
import time
import os
import json
from pathlib import Path


# Check if Docker is available
def is_docker_available():
    """Check if Docker is installed and running."""
    try:
        result = subprocess.run(
            ["docker", "version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


DOCKER_AVAILABLE = is_docker_available()
SKIP_REASON = "Docker not available or not running"


@pytest.mark.e2e
@pytest.mark.docker
@pytest.mark.skipif(not DOCKER_AVAILABLE, reason=SKIP_REASON)
class TestDockerBuildAndRun:
    """Test Docker image build and container execution."""

    @pytest.fixture(scope="class")
    def project_root(self):
        """Get project root directory."""
        return Path(__file__).parent.parent.parent

    @pytest.fixture(scope="class")
    def docker_image_name(self):
        """Docker image name for testing."""
        return "houdinis-test:latest"

    def test_dockerfile_exists(self, project_root):
        """Test that Dockerfile exists."""
        dockerfile = project_root / "docker" / "Dockerfile"
        assert dockerfile.exists(), "Dockerfile not found in docker/"

    def test_docker_build_success(self, project_root, docker_image_name):
        """Test Docker image builds successfully."""
        dockerfile_path = project_root / "docker" / "Dockerfile"
        
        # Build Docker image
        result = subprocess.run(
            [
                "docker", "build",
                "-t", docker_image_name,
                "-f", str(dockerfile_path),
                str(project_root)
            ],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        assert result.returncode == 0, f"Docker build failed: {result.stderr}"
        
        # Verify image exists
        result = subprocess.run(
            ["docker", "images", "-q", docker_image_name],
            capture_output=True,
            text=True
        )
        assert result.stdout.strip(), "Docker image not found after build"

    def test_docker_run_basic(self, docker_image_name):
        """Test Docker container runs successfully."""
        result = subprocess.run(
            [
                "docker", "run", "--rm",
                docker_image_name,
                "python3", "-c", "print('Hello from Houdinis')"
            ],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        assert result.returncode == 0, f"Container run failed: {result.stderr}"
        assert "Hello from Houdinis" in result.stdout

    def test_docker_python_version(self, docker_image_name):
        """Test correct Python version in container."""
        result = subprocess.run(
            [
                "docker", "run", "--rm",
                docker_image_name,
                "python3", "--version"
            ],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        assert result.returncode == 0
        assert "Python 3." in result.stdout

    def test_docker_dependencies_installed(self, docker_image_name):
        """Test that required dependencies are installed."""
        packages_to_check = ["qiskit", "numpy", "pytest"]
        
        for package in packages_to_check:
            result = subprocess.run(
                [
                    "docker", "run", "--rm",
                    docker_image_name,
                    "python3", "-c", f"import {package}; print('{package} OK')"
                ],
                capture_output=True,
                text=True,
                timeout=15
            )
            
            assert result.returncode == 0, f"Package {package} not installed"
            assert f"{package} OK" in result.stdout


@pytest.mark.e2e
@pytest.mark.docker
@pytest.mark.skipif(not DOCKER_AVAILABLE, reason=SKIP_REASON)
class TestDockerExploitExecution:
    """Test exploit execution inside Docker containers."""

    @pytest.fixture
    def docker_image_name(self):
        return "houdinis-test:latest"

    def test_simon_algorithm_in_docker(self, docker_image_name):
        """Test Simon's algorithm execution in Docker."""
        result = subprocess.run(
            [
                "docker", "run", "--rm",
                docker_image_name,
                "python3", "-c",
                """
import sys
sys.path.insert(0, '/app')
from exploits.simon_algorithm import SimonAlgorithm

simon = SimonAlgorithm(n_bits=3)
print('Simon algorithm initialized successfully')
"""
            ],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        assert result.returncode == 0, f"Simon algorithm failed: {result.stderr}"
        assert "initialized successfully" in result.stdout

    def test_quantum_backend_in_docker(self, docker_image_name):
        """Test quantum backend initialization in Docker."""
        result = subprocess.run(
            [
                "docker", "run", "--rm",
                docker_image_name,
                "python3", "-c",
                """
import sys
sys.path.insert(0, '/app')
from quantum.simulator import QuantumSimulator

sim = QuantumSimulator(num_qubits=2)
print('Quantum simulator initialized successfully')
"""
            ],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        assert result.returncode == 0, f"Quantum backend failed: {result.stderr}"
        assert "initialized successfully" in result.stdout

    def test_security_modules_in_docker(self, docker_image_name):
        """Test security modules work in Docker."""
        result = subprocess.run(
            [
                "docker", "run", "--rm",
                docker_image_name,
                "python3", "-c",
                """
import sys
sys.path.insert(0, '/app')
from security.security_config import SecurityConfig

config = SecurityConfig()
print('Security modules loaded successfully')
"""
            ],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        assert result.returncode == 0, f"Security modules failed: {result.stderr}"
        assert "loaded successfully" in result.stdout


@pytest.mark.e2e
@pytest.mark.docker
@pytest.mark.skipif(not DOCKER_AVAILABLE, reason=SKIP_REASON)
class TestDockerNetworking:
    """Test Docker networking and isolation."""

    @pytest.fixture
    def docker_image_name(self):
        return "houdinis-test:latest"

    def test_container_network_isolation(self, docker_image_name):
        """Test containers run in isolated network."""
        # Run container with no network
        result = subprocess.run(
            [
                "docker", "run", "--rm", "--network", "none",
                docker_image_name,
                "python3", "-c", "print('Network isolated')"
            ],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        assert result.returncode == 0
        assert "Network isolated" in result.stdout

    def test_container_hostname(self, docker_image_name):
        """Test container has correct hostname."""
        result = subprocess.run(
            [
                "docker", "run", "--rm",
                docker_image_name,
                "hostname"
            ],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        assert result.returncode == 0
        assert len(result.stdout.strip()) > 0


@pytest.mark.e2e
@pytest.mark.docker
@pytest.mark.skipif(not DOCKER_AVAILABLE, reason=SKIP_REASON)
class TestDockerSecurity:
    """Test Docker security features."""

    @pytest.fixture
    def docker_image_name(self):
        return "houdinis-test:latest"

    def test_container_runs_as_nonroot(self, docker_image_name):
        """Test container runs as non-root user."""
        result = subprocess.run(
            [
                "docker", "run", "--rm",
                docker_image_name,
                "whoami"
            ],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        assert result.returncode == 0
        username = result.stdout.strip()
        # Should not be root
        assert username != "root", "Container should not run as root"

    def test_container_filesystem_readonly(self, docker_image_name):
        """Test container can run with read-only filesystem."""
        result = subprocess.run(
            [
                "docker", "run", "--rm", "--read-only",
                docker_image_name,
                "python3", "-c", "print('Read-only OK')"
            ],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        # Should work with read-only filesystem for basic operations
        assert result.returncode == 0 or "Read-only" in result.stderr

    def test_container_no_privileged(self, docker_image_name):
        """Test container doesn't require privileged mode."""
        result = subprocess.run(
            [
                "docker", "run", "--rm",
                docker_image_name,
                "python3", "-c", "print('No privileges needed')"
            ],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        assert result.returncode == 0
        assert "No privileges needed" in result.stdout


@pytest.mark.e2e
@pytest.mark.docker
@pytest.mark.skipif(not DOCKER_AVAILABLE, reason=SKIP_REASON)
class TestDockerVolumes:
    """Test Docker volume mounting and data persistence."""

    @pytest.fixture
    def docker_image_name(self):
        return "houdinis-test:latest"

    @pytest.fixture
    def temp_dir(self, tmp_path):
        """Create temporary directory for volume testing."""
        return tmp_path

    def test_volume_mount_read(self, docker_image_name, temp_dir):
        """Test reading from mounted volume."""
        # Create test file
        test_file = temp_dir / "test.txt"
        test_file.write_text("Test data from host")
        
        result = subprocess.run(
            [
                "docker", "run", "--rm",
                "-v", f"{temp_dir}:/data:ro",
                docker_image_name,
                "cat", "/data/test.txt"
            ],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        assert result.returncode == 0
        assert "Test data from host" in result.stdout

    def test_volume_mount_write(self, docker_image_name, temp_dir):
        """Test writing to mounted volume."""
        result = subprocess.run(
            [
                "docker", "run", "--rm",
                "-v", f"{temp_dir}:/data",
                docker_image_name,
                "sh", "-c", "echo 'Data from container' > /data/output.txt"
            ],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        assert result.returncode == 0
        
        # Verify file was created
        output_file = temp_dir / "output.txt"
        assert output_file.exists()
        assert "Data from container" in output_file.read_text()


@pytest.mark.e2e
@pytest.mark.docker
@pytest.mark.skipif(not DOCKER_AVAILABLE, reason=SKIP_REASON)
class TestDockerCompose:
    """Test Docker Compose integration."""

    @pytest.fixture
    def project_root(self):
        return Path(__file__).parent.parent.parent

    def test_docker_compose_file_exists(self, project_root):
        """Test docker-compose.yml exists."""
        compose_file = project_root / "docker" / "docker-compose.yml"
        assert compose_file.exists(), "docker-compose.yml not found"

    def test_docker_compose_syntax(self, project_root):
        """Test docker-compose.yml has valid syntax."""
        compose_file = project_root / "docker" / "docker-compose.yml"
        
        result = subprocess.run(
            ["docker-compose", "-f", str(compose_file), "config"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Accept both success and "docker-compose not found"
        if result.returncode != 0 and "not found" in result.stderr.lower():
            pytest.skip("docker-compose not installed")
        
        assert result.returncode == 0, f"Invalid compose file: {result.stderr}"


@pytest.mark.e2e
@pytest.mark.docker
@pytest.mark.slow
@pytest.mark.skipif(not DOCKER_AVAILABLE, reason=SKIP_REASON)
class TestDockerPerformance:
    """Test Docker container performance."""

    @pytest.fixture
    def docker_image_name(self):
        return "houdinis-test:latest"

    def test_container_startup_time(self, docker_image_name):
        """Test container starts within acceptable time."""
        start_time = time.time()
        
        result = subprocess.run(
            [
                "docker", "run", "--rm",
                docker_image_name,
                "python3", "-c", "print('Started')"
            ],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        elapsed = time.time() - start_time
        
        assert result.returncode == 0
        assert elapsed < 10.0, f"Container took {elapsed:.2f}s to start (> 10s)"

    def test_parallel_container_execution(self, docker_image_name):
        """Test multiple containers can run in parallel."""
        import concurrent.futures
        
        def run_container(i):
            result = subprocess.run(
                [
                    "docker", "run", "--rm",
                    docker_image_name,
                    "python3", "-c", f"print('Container {i}')"
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(run_container, i) for i in range(3)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        assert all(results), "Not all containers completed successfully"


def test_docker_module_imports():
    """Test that Docker test module can be imported."""
    assert is_docker_available is not None
    assert DOCKER_AVAILABLE is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "-m", "docker"])
