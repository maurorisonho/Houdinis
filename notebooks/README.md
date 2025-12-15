#  Houdinis Jupyter Notebooks

##  Try Interactive Notebooks Now!

**Run all notebooks in your browser without installation:**

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/maurorisonho/Houdinis/main?labpath=notebooks%2Fplayground.ipynb)

 **Quick Start:** 5-minute interactive tutorial  
 **Full Access:** All 9 comprehensive notebooks available

---

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

###  Quick Start
**[`playground.ipynb`](playground.ipynb)** - **START HERE!**   
5-minute interactive tutorial covering:
- Your first quantum circuit
- Bell state entanglement demo
- Grover's search algorithm
- RSA security analysis widget

[ Launch playground.ipynb in Binder](https://mybinder.org/v2/gh/maurorisonho/Houdinis/main?labpath=notebooks%2Fplayground.ipynb)

---

###  Comprehensive Tutorials

### 1. `01-IBM_Quantum_Experience_Integration.ipynb`
Connect to real IBM quantum hardware:
- IBM Quantum account setup
- Access real quantum processors
- Run circuits on actual quantum computers
- Compare simulator vs hardware results

[ Launch in Binder](https://mybinder.org/v2/gh/maurorisonho/Houdinis/main?labpath=notebooks%2F01-IBM_Quantum_Experience_Integration.ipynb)

### 2. `02-Shors_Algorithm_RSA_Exploitation.ipynb`
RSA factorization using Shor's algorithm:
- Integer factorization theory
- Quantum Fourier Transform
- Period finding algorithm
- Break RSA encryption

[ Launch in Binder](https://mybinder.org/v2/gh/maurorisonho/Houdinis/main?labpath=notebooks%2F02-Shors_Algorithm_RSA_Exploitation.ipynb)

### 3. `03-Grovers_Algorithm_Symmetric_Key_Attacks.ipynb`
Grover's algorithm for symmetric key attacks:
- AES key recovery with quadratic speedup
- SSH password cracking acceleration
- TLS/RSA vulnerability analysis
- Real attacks against vulnerable Docker container

[ Launch in Binder](https://mybinder.org/v2/gh/maurorisonho/Houdinis/main?labpath=notebooks%2F03-Grovers_Algorithm_Symmetric_Key_Attacks.ipynb)

### 4. `04-Quantum_Network_Scanning.ipynb`
Quantum-enhanced network reconnaissance:
- Identify quantum-vulnerable systems
- Protocol analysis and detection
- Network mapping strategies
- Vulnerability scoring

[ Launch in Binder](https://mybinder.org/v2/gh/maurorisonho/Houdinis/main?labpath=notebooks%2F04-Quantum_Network_Scanning.ipynb)

### 5. `05-Harvest_Now_Decrypt_Later_Attacks.ipynb`
Future quantum threat assessment:
- Store encrypted data now, decrypt later
- Timeline to quantum threats
- Risk assessment frameworks
- Migration strategies

[ Launch in Binder](https://mybinder.org/v2/gh/maurorisonho/Houdinis/main?labpath=notebooks%2F05-Harvest_Now_Decrypt_Later_Attacks.ipynb)

### 6. `06-Post_Quantum_Cryptography_Analysis.ipynb`
Post-quantum cryptography solutions:
- NIST PQC standards (Kyber, Dilithium)
- Lattice-based cryptography
- Hash-based signatures
- Migration guides

[ Launch in Binder](https://mybinder.org/v2/gh/maurorisonho/Houdinis/main?labpath=notebooks%2F06-Post_Quantum_Cryptography_Analysis.ipynb)

### 7. `07-Quantum_Machine_Learning_Cryptanalysis.ipynb`
QML-based cryptanalysis:
- Quantum neural networks
- Adversarial attacks
- Pattern recognition
- Cryptographic weaknesses

[ Launch in Binder](https://mybinder.org/v2/gh/maurorisonho/Houdinis/main?labpath=notebooks%2F07-Quantum_Machine_Learning_Cryptanalysis.ipynb)

### 8. `08-Houdinis_Advanced_Features.ipynb`
Framework deep dive:
- Multi-backend configuration
- Performance benchmarking
- Custom exploit development
- Best practices

[ Launch in Binder](https://mybinder.org/v2/gh/maurorisonho/Houdinis/main?labpath=notebooks%2F08-Houdinis_Advanced_Features.ipynb)

### 9. `09-Houdinis_Framework_Conclusion.ipynb`
Summary and next steps:
- Framework capabilities review
- Real-world applications
- Research directions
- Contributing guide

[ Launch in Binder](https://mybinder.org/v2/gh/maurorisonho/Houdinis/main?labpath=notebooks%2F09-Houdinis_Framework_Conclusion.ipynb)

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
