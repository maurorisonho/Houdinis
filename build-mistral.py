#!/usr/bin/env python3
"""
Build Monitor for Houdinis Mistral AI
Displays visual progress of Docker build with CUDA + Ollama + LangChain
"""

import subprocess
import sys
import re
import time
from datetime import datetime

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header():
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}   HOUDINIS MISTRAL AI - BUILD MONITOR{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}\n")
    print(f"{Colors.YELLOW}  This process may take 10-15 minutes{Colors.ENDC}")
    print(f"{Colors.YELLOW}   Components: NVIDIA CUDA 12.4 + Ollama + LangChain + cuQuantum{Colors.ENDC}\n")

def print_step(step_num, total_steps, message, status="⏳"):
    percentage = (step_num / total_steps) * 100
    bar_length = 40
    filled = int(bar_length * step_num / total_steps)
    bar = '' * filled + '' * (bar_length - filled)
    
    print(f"\r{status} [{bar}] {percentage:5.1f}% | Step {step_num}/{total_steps}: {message}", end='', flush=True)

def extract_package_info(line):
    """Extract detailed information from packages being installed"""
    details = []
    
    # Pacotes Python (pip install)
    if 'Collecting' in line:
        pkg = re.search(r'Collecting\s+([^\s\(]+)', line)
        if pkg:
            details.append(f" {pkg.group(1)}")
    
    if 'Downloading' in line:
        # Extrair nome e tamanho do pacote
        pkg_match = re.search(r'Downloading\s+([^\s]+)-([0-9\.]+).*?\(([0-9\.]+\s*[kMG]?B)\)', line)
        if pkg_match:
            details.append(f"  {pkg_match.group(1)} {pkg_match.group(2)} ({pkg_match.group(3)})")
    
    if 'Installing collected packages' in line:
        pkgs = re.search(r'Installing collected packages:\s+(.+)', line)
        if pkgs:
            pkg_list = pkgs.group(1).split(', ')
            details.append(f" Installing {len(pkg_list)} packages")
    
    if 'Successfully installed' in line:
        pkgs = re.search(r'Successfully installed\s+(.+)', line)
        if pkgs:
            details.append(f" {pkgs.group(1)}")
    
    # APT packages (apt-get install)
    if 'Setting up' in line:
        pkg = re.search(r'Setting up\s+([^\s]+)', line)
        if pkg:
            details.append(f"  {pkg.group(1)}")
    
    if 'Unpacking' in line:
        pkg = re.search(r'Unpacking\s+([^\s]+)', line)
        if pkg:
            details.append(f" {pkg.group(1)}")
    
    # Ollama
    if 'ollama' in line.lower() and 'install' in line.lower():
        details.append(f" Installing Ollama")
    
    # Large file downloads
    if re.search(r'\d+%.*?\d+[KMG]B', line):
        progress = re.search(r'(\d+)%.*?(\d+[KMG]B)', line)
        if progress:
            details.append(f"  {progress.group(1)}% ({progress.group(2)})")
    
    return details

def run_docker_build():
    """Execute build and monitor progress with details"""
    
    # Map known Dockerfile.mistral steps
    steps_info = {
        1: "Loading build definitions",
        2: "Downloading NVIDIA CUDA 12.4 base image",
        3: "Installing system dependencies (python3.11, git, wget, curl)",
        4: "Installing Ollama AI framework",
        5: "Configuring /opt/houdinis directory",
        6: "Copying requirements.txt files",
        7: "Installing basic Python packages (~2-3 min)",
        8: "Installing LangChain + OpenAI (~1-2 min)",
        9: "Installing ChromaDB + FAISS + Sentence Transformers (~2-3 min)",
        10: "Installing NVIDIA cuQuantum (optional, GPU only)",
        11: "Copying Houdinis source code",
        12: "Creating data and log directories",
        13: "Creating 'houdinis' user (non-root)",
        14: "Exposing ports (7681, 8001, 8765, 11434)",
        15: "Configuring health check",
        16: "Creating startup script",
        17: "Adjusting file permissions",
        18: "Exporting image layers",
        19: "Saving image to Docker registry",
        20: "Build completed!"
    }
    
    cmd = [
        'docker', 'compose',
        '-f', 'docker/docker-compose-lite.yml',
        'build', '--progress=plain', 'mistral'  # plain to see all details
    ]
    
    print(f"{Colors.CYAN} Command:{Colors.ENDC} {' '.join(cmd)}\n")
    print(f"{Colors.YELLOW} Starting detailed build...{Colors.ENDC}\n")
    
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    current_step = 0
    total_steps = 20
    last_output = ""
    start_time = time.time()
    detail_lines = []
    show_details = False
    packages_installed = 0
    
    try:
        for line in process.stdout:
            line = line.strip()
            if not line:
                continue
            
            # Extract package details
            details = extract_package_info(line)
            if details:
                for detail in details:
                    if detail.startswith(''):
                        packages_installed += 1
                    print(f"\r{' '*100}\r  {detail}", flush=True)
                    time.sleep(0.1)  # Brief pause for visualization
            
            # Detect main progress
            step_match = re.search(r'\[\s*(\d+)/(\d+)\]', line)
            if step_match:
                current_step = int(step_match.group(1))
                total_steps = int(step_match.group(2))
                
                step_desc = steps_info.get(current_step, f"Step {current_step}")
                
                # Detect specific operations and show details
                if 'RUN pip3 install' in line:
                    show_details = True
                    if 'langchain' in line.lower():
                        step_desc = "Installing LangChain + OpenAI + Community"
                        print(f"\n{Colors.CYAN}   Components:{Colors.ENDC}")
                        print(f"     • langchain-core (framework base)")
                        print(f"     • langchain-community (integrations)")
                        print(f"     • langchain-openai (OpenAI/Ollama)")
                    elif 'chromadb' in line.lower():
                        step_desc = "Installing Vector Stores + Embeddings"
                        print(f"\n{Colors.CYAN}    Components:{Colors.ENDC}")
                        print(f"     • chromadb (vector database)")
                        print(f"     • faiss-cpu (Facebook AI Similarity Search)")
                        print(f"     • sentence-transformers (embeddings)")
                    elif 'cuquantum' in line.lower():
                        step_desc = "Installing NVIDIA cuQuantum SDK"
                        print(f"\n{Colors.CYAN}   GPU Computing:{Colors.ENDC}")
                        print(f"     • cuquantum-python-cu12 (Quantum GPU acceleration)")
                    elif 'requirements.txt' in line:
                        step_desc = "Installing Houdinis base dependencies"
                        print(f"\n{Colors.CYAN}   Base Packages:{Colors.ENDC}")
                        print(f"     • qiskit (IBM Quantum SDK)")
                        print(f"     • cirq (Google Quantum SDK)")
                        print(f"     • docker-py (container control)")
                        print(f"     • flask + socketio (web interface)")
                    else:
                        step_desc = "Installing Python packages"
                        show_details = True
                
                elif 'apt-get install' in line:
                    step_desc = "Installing system tools"
                    print(f"\n{Colors.CYAN}    System:{Colors.ENDC}")
                    if 'python3.11' in line:
                        print(f"     • Python 3.11 + pip")
                    if 'git' in line:
                        print(f"     • Git version control")
                    if 'curl' in line or 'wget' in line:
                        print(f"     • curl, wget (download tools)")
                    if 'build-essential' in line:
                        print(f"     • GCC, Make (C/C++ compilers)")
                    if 'cmake' in line:
                        print(f"     • CMake (build system)")
                    if 'ttyd' in line:
                        print(f"     • ttyd (web terminal)")
                
                elif 'ollama' in line.lower() and 'install' in line.lower():
                    step_desc = "Installing Ollama AI framework"
                    print(f"\n{Colors.CYAN}   Ollama:{Colors.ENDC}")
                    print(f"     • Local server for LLMs")
                    print(f"     • Support: Mistral, CodeLlama, Llama2")
                
                elif 'COPY' in line:
                    if 'requirements' in line:
                        step_desc = "Copying dependency files"
                    elif 'exploits' in line or 'scanners' in line:
                        step_desc = "Copying Houdinis modules"
                        print(f"\n{Colors.CYAN}   Source Code:{Colors.ENDC}")
                        print(f"     • exploits/ (quantum attacks)")
                        print(f"     • scanners/ (vulnerability scanners)")
                        print(f"     • quantum/ (simulators)")
                        print(f"     • langchain_agents/ (AI agents)")
                    else:
                        step_desc = "Copying project files"
                
                elif 'FROM' in line:
                    step_desc = "Downloading NVIDIA CUDA base image"
                    if 'nvidia/cuda' in line:
                        print(f"\n{Colors.CYAN}   Base Image:{Colors.ENDC}")
                        print(f"     • NVIDIA CUDA 12.4.1")
                        print(f"     • Ubuntu 22.04 LTS")
                        print(f"     • Size: ~5GB")
                
                elif 'exporting' in line.lower():
                    if 'layers' in line.lower():
                        step_desc = "Exporting Docker image layers"
                    elif 'manifest' in line.lower():
                        step_desc = "Saving image manifest"
                
                print_step(current_step, total_steps, step_desc, "⏳")
                last_output = step_desc
            
            # Show download progress
            elif re.search(r'#\d+\s+\d+\.\d+s', line):
                time_match = re.search(r'(\d+\.\d+)s', line)
                if time_match:
                    elapsed = time_match.group(1)
                    print(f"\r{' '*100}\r  ⏱  {elapsed}s elapsed...", end='', flush=True)
            
            # Detect critical errors
            elif 'ERROR' in line or ('error' in line.lower() and 'failed' in line.lower()):
                print(f"\n{Colors.RED} CRITICAL ERROR:{Colors.ENDC}")
                print(f"{Colors.RED}   {line}{Colors.ENDC}")
            
            # Detect warnings (but filter common pip warnings)
            elif 'WARNING' in line and 'Running pip as the' not in line:
                print(f"\n{Colors.YELLOW}  {line[:80]}{Colors.ENDC}")
            
            # Detect completion
            elif 'naming to docker.io' in line.lower():
                current_step = total_steps
                print_step(current_step, total_steps, "Build completed!", "")
        
        process.wait()
        elapsed = time.time() - start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        
        print()  # New line after progress bar
        
        if process.returncode == 0:
            print(f"\n\n{Colors.GREEN}{Colors.BOLD} BUILD COMPLETED SUCCESSFULLY!{Colors.ENDC}")
            print(f"{Colors.GREEN}   Total time: {minutes}m {seconds}s{Colors.ENDC}")
            if packages_installed > 0:
                print(f"{Colors.GREEN}   Packages installed: {packages_installed}+{Colors.ENDC}\n")
            
            print(f"{Colors.CYAN}{'='*70}{Colors.ENDC}")
            print(f"{Colors.BOLD} Image Summary:{Colors.ENDC}\n")
            
            # Show image size
            try:
                result = subprocess.run(
                    ['docker', 'images', 'houdinis-mistral:latest', '--format', '{{.Size}}'],
                    capture_output=True, text=True
                )
                if result.stdout.strip():
                    print(f"   Image: houdinis-mistral:latest")
                    print(f"   Size: {result.stdout.strip()}")
                    print()
            except:
                pass
            
            print(f"{Colors.CYAN}{'='*70}{Colors.ENDC}")
            print(f"{Colors.BOLD} Next Steps:{Colors.ENDC}\n")
            print(f"  1. Start Mistral AI container:")
            print(f"     {Colors.CYAN}docker compose -f docker/docker-compose-lite.yml up -d mistral{Colors.ENDC}\n")
            print(f"  2. Monitor initialization (downloads Mistral model 4.1GB):")
            print(f"     {Colors.CYAN}docker logs houdinis_mistral -f{Colors.ENDC}\n")
            print(f"  3. Check container status:")
            print(f"     {Colors.CYAN}docker ps{Colors.ENDC}\n")
            print(f"  4. Access Web UI:"
            print(f"     {Colors.CYAN}http://localhost:8080{Colors.ENDC} → Menu 'AI Assistant'\n")
            print(f"  5. Test Ollama API:")
            print(f"     {Colors.CYAN}curl http://localhost:11434/api/tags{Colors.ENDC}\n")
            print(f"{Colors.CYAN}{'='*70}{Colors.ENDC}\n")
            return True
        else:
            print(f"\n{Colors.RED}{Colors.BOLD} BUILD FAILED!{Colors.ENDC}")
            print(f"{Colors.RED}   Error code: {process.returncode}{Colors.ENDC}\n")
            return False
            
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}  Build interrupted by user{Colors.ENDC}")
        process.terminate()
        return False
    except Exception as e:
        print(f"\n{Colors.RED} Error: {str(e)}{Colors.ENDC}")
        return False

def check_requirements():
    """Check requirements before build"""
    print(f"{Colors.BOLD} Checking requirements...{Colors.ENDC}\n")
    
    # Check Docker
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        print(f"   Docker: {result.stdout.strip()}")
    except FileNotFoundError:
        print(f"  {Colors.RED} Docker not found{Colors.ENDC}")
        return False
    
    # Check NVIDIA GPU (optional)
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=name', '--format=csv,noheader'], 
                              capture_output=True, text=True, timeout=2)
        if result.returncode == 0:
            gpu_name = result.stdout.strip()
            print(f"   GPU NVIDIA: {gpu_name}")
        else:
            print(f"  {Colors.YELLOW}  NVIDIA GPU not detected (build will be slower){Colors.ENDC}")
    except:
        print(f"  {Colors.YELLOW}  nvidia-smi not available{Colors.ENDC}")
    
    # Check disk space
    try:
        result = subprocess.run(['df', '-h', '.'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            parts = lines[1].split()
            available = parts[3]
            print(f"  ℹ  Available space: {available}")
            print(f"     {Colors.YELLOW}(Requires ~15GB for complete build){Colors.ENDC}")
    except:
        pass
    
    print()
    return True

def main():
    print_header()
    
    if not check_requirements():
        sys.exit(1)
    
    # Confirm before starting
    print(f"{Colors.BOLD}Start build? [Y/n]{Colors.ENDC} ", end='', flush=True)
    response = input().strip().lower()
    
    if response and response not in ['s', 'sim', 'y', 'yes', '']:
        print(f"\n{Colors.YELLOW} Build cancelled{Colors.ENDC}")
        sys.exit(0)
    
    print()
    success = run_docker_build()
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
