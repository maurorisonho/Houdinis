#!/usr/bin/env python3
"""
Quick Test Script for Houdinis Docker Integration
Run this to verify notebook-to-docker connectivity
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from docker_helpers import get_docker_manager


def main():
    print(" HOUDINIS DOCKER INTEGRATION TEST")
    print("=" * 70)

    # Create manager
    mgr = get_docker_manager()

    # Test 1: Check containers
    print("\n Test 1: Checking container status...")
    containers = mgr.check_containers()

    if len(containers) < 2:
        print("    Not all containers running. Starting them...")
        if not mgr.start_containers():
            print("   Failed to start containers")
            return False
        containers = mgr.check_containers()

    print(f"   {len(containers)} containers running")

    # Test 2: Get IPs
    print("\n Test 2: Getting container IPs...")
    framework_ip = mgr.get_container_ip("houdinis_framework")
    target_ip = mgr.get_container_ip("houdinis_target")

    if not framework_ip or not target_ip:
        print("   Failed to get container IPs")
        return False

    print(f"   Framework: {framework_ip}")
    print(f"   Target: {target_ip}")

    # Test 3: Test services
    print("\n Test 3: Testing target services...")
    services = {"SSH": 22, "HTTP": 80, "HTTPS": 443}

    all_reachable = True
    for name, port in services.items():
        reachable = mgr.test_service(target_ip, port)
        status = "" if reachable else ""
        print(f"  {status} {name} (port {port})")
        all_reachable = all_reachable and reachable

    if not all_reachable:
        print("    Some services not reachable")

    # Test 4: Execute in framework
    print("\n Test 4: Executing command in framework container...")
    result = mgr.exec_in_framework("python3 -c 'import sys; print(sys.version)'")

    if result["success"]:
        print(f"   Python version: {result['stdout'].strip().split()[0]}")
    else:
        print(f"   Execution failed: {result['stderr']}")
        return False

    # Test 5: Test Houdinis import
    print("\n Test 5: Testing Houdinis imports...")
    test_cmd = """python3 -c "
import sys
sys.path.insert(0, '/app')
try:
    from quantum.backend import QuantumBackendManager
    print('Quantum modules OK')
except ImportError as e:
    print(f'Import error: {e}')
    sys.exit(1)
"
"""
    result = mgr.exec_in_framework(test_cmd)

    if result["success"] and "OK" in result["stdout"]:
        print("   Houdinis modules available")
    else:
        print(f"    Module import issues: {result['stderr']}")

    # Test 6: Test SSH connectivity
    print("\n Test 6: Testing SSH connectivity to target...")
    ssh_test = """python3 -c "
import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect('target', username='root', password='vulnerable', timeout=5)
    stdin, stdout, stderr = ssh.exec_command('echo SUCCESS')
    result = stdout.read().decode().strip()
    ssh.close()
    print(result)
except Exception as e:
    print(f'SSH error: {e}')
    sys.exit(1)
"
"""
    result = mgr.exec_in_framework(ssh_test)

    if result["success"] and "SUCCESS" in result["stdout"]:
        print("   SSH connection successful")
    else:
        print(f"    SSH connection issues: {result['stderr']}")

    # Final status
    print("\n" + "=" * 70)
    print(" FINAL STATUS")
    print("=" * 70)
    mgr.print_status()

    print("\n All tests completed!")
    print("\n You can now use the Jupyter notebooks to run quantum attacks")
    print("   Start with: Grovers_Algorithm_Symmetric_Key_Attacks.ipynb")

    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
