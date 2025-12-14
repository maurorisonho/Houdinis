"""
Docker Helper Functions for Houdinis Notebooks
Author: Mauro Risonho de Paula Assumpção aka firebitsbr
License: MIT

This module provides helper functions to interact with Houdinis Docker containers
from Jupyter notebooks.
"""

import subprocess
import json
import time
import socket
from typing import Dict, List, Optional


class HoudinisDockerManager:
    """Manager for Houdinis Docker containers"""
    
    def __init__(self):
        self.framework_container = "houdinis_framework"
        self.target_container = "houdinis_target"
        self.compose_file = "../docker/docker-compose.yml"
        
    def check_containers(self) -> List[Dict]:
        """Check if Houdinis Docker containers are running"""
        try:
            result = subprocess.run(
                ['docker', 'ps', '--filter', 'name=houdinis', '--format', '{{json .}}'],
                capture_output=True, text=True, check=True
            )
            
            containers = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    containers.append(json.loads(line))
            
            return containers
        except Exception as e:
            print(f" Error checking containers: {e}")
            return []
    
    def start_containers(self) -> bool:
        """Start Houdinis Docker containers"""
        try:
            print(" Starting Docker containers...")
            subprocess.run(
                ['docker', 'compose', '-f', self.compose_file, 'up', '-d'],
                check=True, capture_output=True, cwd='.'
            )
            time.sleep(5)  # Wait for containers to be ready
            print(" Containers started successfully")
            return True
        except Exception as e:
            print(f" Error starting containers: {e}")
            return False
    
    def stop_containers(self) -> bool:
        """Stop Houdinis Docker containers"""
        try:
            print(" Stopping Docker containers...")
            subprocess.run(
                ['docker', 'compose', '-f', self.compose_file, 'down'],
                check=True, capture_output=True, cwd='.'
            )
            print(" Containers stopped successfully")
            return True
        except Exception as e:
            print(f" Error stopping containers: {e}")
            return False
    
    def get_container_ip(self, container_name: str) -> Optional[str]:
        """Get IP address of a Docker container"""
        try:
            result = subprocess.run(
                ['docker', 'inspect', '-f', 
                 '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}', 
                 container_name],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except Exception as e:
            print(f" Error getting IP for {container_name}: {e}")
            return None
    
    def exec_in_framework(self, command: str, workdir: str = "/app", timeout: int = 30) -> Dict:
        """Execute command in houdinis_framework container"""
        try:
            cmd = ['docker', 'exec', '-w', workdir, self.framework_container, 
                   'bash', '-c', command]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            return {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode,
                'success': result.returncode == 0
            }
        except subprocess.TimeoutExpired:
            return {
                'stdout': '', 
                'stderr': 'Command timeout', 
                'returncode': -1,
                'success': False
            }
        except Exception as e:
            return {
                'stdout': '', 
                'stderr': str(e), 
                'returncode': -1,
                'success': False
            }
    
    def test_service(self, host: str, port: int, timeout: int = 3) -> bool:
        """Test if a service is reachable"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def get_status(self) -> Dict:
        """Get comprehensive status of Houdinis environment"""
        containers = self.check_containers()
        
        status = {
            'containers_running': len(containers),
            'containers': [],
            'framework_ip': None,
            'target_ip': None,
            'services': {}
        }
        
        for container in containers:
            status['containers'].append({
                'name': container['Names'],
                'status': container['Status'],
                'image': container['Image']
            })
        
        if len(containers) >= 2:
            status['framework_ip'] = self.get_container_ip(self.framework_container)
            status['target_ip'] = self.get_container_ip(self.target_container)
            
            # Test target services
            if status['target_ip']:
                status['services'] = {
                    'ssh': self.test_service(status['target_ip'], 22),
                    'http': self.test_service(status['target_ip'], 80),
                    'https': self.test_service(status['target_ip'], 443)
                }
        
        return status
    
    def print_status(self):
        """Print formatted status information"""
        status = self.get_status()
        
        print(" HOUDINIS DOCKER ENVIRONMENT STATUS")
        print("=" * 70)
        print(f"\n Containers Running: {status['containers_running']}/2")
        
        for container in status['containers']:
            print(f"\n   {container['name']}")
            print(f"     Status: {container['status']}")
            print(f"     Image: {container['image']}")
        
        if status['framework_ip'] and status['target_ip']:
            print(f"\n Network Configuration:")
            print(f"  Framework IP: {status['framework_ip']}")
            print(f"  Target IP: {status['target_ip']}")
            
            print(f"\n Target Services:")
            for service, reachable in status['services'].items():
                status_icon = "" if reachable else ""
                print(f"  {status_icon} {service.upper()}")
        
        print("\n" + "=" * 70)


# Convenience function for notebooks
def get_docker_manager() -> HoudinisDockerManager:
    """Get a HoudinisDockerManager instance"""
    return HoudinisDockerManager()
