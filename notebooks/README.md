#  Houdinis Jupyter Notebooks

## Overview

This directory contains Jupyter notebooks demonstrating quantum cryptographic attacks using the Houdinis framework with Docker containers.

##  Docker Architecture

```

      Jupyter Notebook (Host)            
  - Execute Python code                  
  - Control Docker containers            

                docker exec
               ↓

   houdinis_framework Container          
  - CUDA 12.4.1 + GPU support            
  - Qiskit + cuQuantum                   
  - Quantum attack tools                 

                network: houdinis_net
               ↓

   houdinis_target Container             
  - SSH (vulnerable password)            
  - HTTPS (RSA 2048-bit)                 
  - HTTP services                        

```

##  Available Notebooks

### 1. `Grovers_Algorithm_Symmetric_Key_Attacks.ipynb`
Demonstrates Grover's algorithm for symmetric key attacks:
- AES key recovery with quadratic speedup
- SSH password cracking acceleration
- TLS/RSA vulnerability analysis
- Real attacks against vulnerable Docker container

### 2. `Shors_Algorithm_RSA_Exploitation.ipynb`
RSA factorization using Shor's algorithm

### 3. `Quantum_Network_Scanning.ipynb`
Quantum-enhanced network reconnaissance

### 4. Other notebooks...
See individual notebooks for specific demonstrations

##  Quick Start

### Prerequisites
```bash
# Ensure Docker and Docker Compose are installed
docker --version
docker compose version

# Start containers
cd ../docker
docker compose up -d

# Verify containers are running
docker ps | grep houdinis
```

### Using the Notebooks

1. **Start Jupyter Lab/Notebook**
   ```bash
   cd notebooks
   jupyter lab
   # or
   jupyter notebook
   ```

2. **Open a notebook** (e.g., `Grovers_Algorithm_Symmetric_Key_Attacks.ipynb`)

3. **Run the setup cells** to:
   - Check Docker container status
   - Verify connectivity to target
   - Import required libraries

4. **Execute attack demonstrations**
   - Individual attacks or full demo
   - All attacks run in isolated Docker environment

##  Helper Functions

The `docker_helpers.py` module provides:

```python
from docker_helpers import get_docker_manager

# Create manager
mgr = get_docker_manager()

# Check status
mgr.print_status()

# Start/stop containers
mgr.start_containers()
mgr.stop_containers()

# Execute commands in framework container
result = mgr.exec_in_framework("python3 -c 'print(\"Hello\")'")
print(result['stdout'])

# Test target services
ssh_reachable = mgr.test_service(target_ip, 22)
```

##  Attack Workflow

1. **Notebook initiates attack**
   ```python
   run_grover_attack_via_docker(key_length=6)
   ```

2. **Command sent to houdinis_framework container**
   ```bash
   docker exec houdinis_framework python3 /app/exploit.py
   ```

3. **Framework attacks houdinis_target**
   - Target hostname: `target` (DNS within Docker network)
   - Services: SSH (22), HTTP (80), HTTPS (443)

4. **Results returned to notebook**
   - Success/failure status
   - Attack metrics (iterations, speedup)
   - Recovered keys/passwords

##  Example Output

```
 Launching Grover's Algorithm Attack
============================================================
  Target: target
  Method: aes
  Key Length: 6 bits
============================================================

 Starting Grover attack simulation...

 Attack Results:
  Found Key: 0x2f
  Iterations: 6
  Success Rate: 95.00%
  Quantum Speedup: 8.00x

 Attack completed successfully!
```

##  Security & Legal

- **All attacks are contained** within isolated Docker network
- **No external network access** from containers
- **For educational purposes only**
- **Authorized testing only** - Do not use against production systems
- See `LICENSE` and `SECURITY.md` for more information

##  Troubleshooting

### Containers not starting
```bash
# Check Docker daemon
sudo systemctl status docker

# View container logs
docker logs houdinis_framework
docker logs houdinis_target

# Rebuild containers
cd ../docker
docker compose down
docker compose build --no-cache
docker compose up -d
```

### Connection errors
```python
# In notebook, verify connectivity
from docker_helpers import get_docker_manager
mgr = get_docker_manager()
mgr.print_status()
```

### Import errors
```bash
# Ensure Houdinis modules are in framework container
docker exec houdinis_framework ls -la /app/quantum
docker exec houdinis_framework python3 -c "import quantum; print('OK')"
```

##  Documentation

- Main project: `../README.md`
- Docker setup: `../docker/README.md`
- Security: `../docs/SECURITY.md`
- API docs: `../docs/README.md`

##  Contributing

See main `CONTRIBUTING.md` for guidelines on:
- Adding new notebooks
- Improving demonstrations
- Bug reports
- Feature requests

##  License

MIT License - see `../LICENSE` for details

---

**Author:** Mauro Risonho de Paula Assumpção (firebitsbr)  
**Project:** Houdinis Quantum Cryptography Testing Framework
