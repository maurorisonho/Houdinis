#!/usr/bin/env python3
"""
Docker Service and Container Manager
====================================

This script helps manage the lifecycle of Docker and Containerd services,
as well as bulk management of Docker containers.

Usage:
    sudo python3 manage_docker.py [OPTIONS]

Options:
    --start-all       Start Docker/Containerd services and resume all containers
    --stop-all        Stop all containers and then stop Docker/Containerd services
    --status          Check the status of services and running containers
    
    --start-services  Only start system services
    --stop-services   Only stop system services
    
    --start-containers Start all stopped containers
    --stop-containers  Stop all running containers
    
Author: Houdinis Framework
"""

import subprocess
import sys
import argparse
import shutil
from typing import List

COLORS = {
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "YELLOW": "\033[93m",
    "RESET": "\033[0m"
}

def log(message: str, color: str = "RESET"):
    """Print a colored message."""
    print(f"{COLORS.get(color, '')}{message}{COLORS['RESET']}")

def run_command(command: List[str], ignore_errors: bool = False) -> bool:
    """Run a system command."""
    try:
        subprocess.run(command, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        if not ignore_errors:
            log(f"Error running command {' '.join(command)}: {e.stderr.strip()}", "RED")
        return False

def check_sudo():
    """Check if script is running with sudo/root."""
    import os
    if os.geteuid() != 0:
        log("This script must be run as root (sudo).", "RED")
        sys.exit(1)

def manage_service(service: str, action: str):
    """Start or stop a system service."""
    log(f"{action.capitalize()}ing service: {service}...", "YELLOW")
    if run_command(["systemctl", action, service]):
        log(f"Successfully {action}ed {service}.", "GREEN")
    else:
        log(f"Failed to {action} {service}.", "RED")

def get_container_ids(all_containers: bool = False) -> List[str]:
    """Get list of container IDs."""
    cmd = ["docker", "ps", "-q"]
    if all_containers:
        cmd.append("-a")
    
    try:
        result = subprocess.run(cmd, check=True, text=True, stdout=subprocess.PIPE)
        return result.stdout.strip().split()
    except Exception:
        return []

def stop_containers():
    """Stop all running containers."""
    ids = get_container_ids(all_containers=False)
    if not ids:
        log("No running containers found.", "GREEN")
        return

    log(f"Stopping {len(ids)} containers...", "YELLOW")
    if run_command(["docker", "stop"] + ids):
        log("All containers stopped.", "GREEN")

def start_containers():
    """Start all stopped containers."""
    # Note: This attempts to start ALL containers, including those that exited properly.
    # A more sophisticated approach might filter, but for "start all" this is acceptable request.
    ids = get_container_ids(all_containers=True)
    if not ids:
        log("No containers found to start.", "GREEN")
        return

    log(f"Starting {len(ids)} containers...", "YELLOW")
    if run_command(["docker", "start"] + ids):
        log("Containers started.", "GREEN")

def check_status():
    """Check status of services and containers."""
    services = ["docker", "containerd"]
    
    print("\n=== Service Status ===")
    for svc in services:
        try:
            res = subprocess.run(["systemctl", "is-active", svc], text=True, stdout=subprocess.PIPE)
            status = res.stdout.strip()
            color = "GREEN" if status == "active" else "RED"
            log(f"{svc}: {status}", color)
        except Exception:
            log(f"{svc}: unknown", "RED")
            
    print("\n=== Container Status ===")
    if shutil.which("docker"):
        subprocess.run(["docker", "ps", "--format", "table {{.ID}}\t{{.Image}}\t{{.Status}}\t{{.Names}}"])
    else:
        log("Docker CLI not found.", "RED")

def main():
    parser = argparse.ArgumentParser(description="Manage Docker/Containerd services and containers.")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--start-all", action="store_true", help="Start services and resume containers")
    group.add_argument("--stop-all", action="store_true", help="Stop containers and services")
    group.add_argument("--status", action="store_true", help="Show status")
    group.add_argument("--start-services", action="store_true", help="Start system services only")
    group.add_argument("--stop-services", action="store_true", help="Stop system services only")
    group.add_argument("--start-containers", action="store_true", help="Start all containers")
    group.add_argument("--stop-containers", action="store_true", help="Stop all containers")
    
    args = parser.parse_args()

    if args.status:
        # Status doesn't strictly require sudo, but systemctl might give specific output
        check_status()
        return

    check_sudo()

    if args.stop_all or args.stop_containers:
        stop_containers()
    
    if args.stop_all or args.stop_services:
        manage_service("docker", "stop")
        manage_service("containerd", "stop")
        # Ensure socket is also handled if needed, but usually service stop is enough
        manage_service("docker.socket", "stop")

    if args.start_all or args.start_services:
        manage_service("containerd", "start")
        manage_service("docker.socket", "start")
        manage_service("docker", "start")

    if args.start_all or args.start_containers:
        # Services must be up before starting containers
        if not args.start_services and not args.start_all:
             # Check if docker is running
             if run_command(["systemctl", "is-active", "docker"], ignore_errors=True):
                 start_containers()
             else:
                 log("Docker service is not active. Use --start-all or start services first.", "RED")
        else:
            import time
            time.sleep(2) # Give a moment for socket to be ready
            start_containers()

if __name__ == "__main__":
    main()
