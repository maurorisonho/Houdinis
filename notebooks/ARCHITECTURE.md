# Houdinis Notebook-Docker Integration Architecture

##  Complete Setup

```

                    HOST MACHINE (Linux)                          
                                                                  
      
           Jupyter Notebook Environment                        
    - Grovers_Algorithm_Symmetric_Key_Attacks.ipynb           
    - docker_helpers.py (connection library)                  
    - test_docker_integration.py (verification)               
      
                                                                
                       Python subprocess.run()                  
                       docker exec commands                     
                      ↓                                          
     
                Docker Daemon                                  
                                                               
          
       Container: houdinis_framework                        
                
         Image: nvidia/cuda:12.4.1-devel                  
         - Python 3.10                                    
         - Qiskit (quantum computing)                     
         - CuPy (GPU arrays)                              
         - cuQuantum (quantum simulation)                 
         - Houdinis framework (/app)                      
         - CUDA 12.4.1 + GPU support                      
                
                                                              
       Exposed: 127.0.0.1:7681 (ttyd web terminal)          
       Network: houdinis_net (172.x.x.x)                    
          
                                                                
                      TCP/IP over Docker network               
                      hostname: "target"                       
                     ↓                                           
           
       Container: houdinis_target                            
                 
         Image: ubuntu:20.04                               
         - OpenSSH Server (port 22)                        
           * root:vulnerable                               
         - Apache HTTP (port 80)                           
         - Apache HTTPS (port 443)                         
           * RSA 2048-bit certificate                      
           * Self-signed SSL                               
                 
                                                               
       Network: houdinis_net (172.x.x.x)                     
       Isolated: No external network access                   
           
                                                                 
     
                                                                    
         
                NVIDIA GPU (Optional)                             
    - GeForce GTX 1060 (6GB)                                    
    - CUDA 13.0 Driver                                          
    - Passed through to houdinis_framework                      
         
                                                                    

```

##  Attack Execution Flow

```
Step 1: User runs notebook cell
   ↓
[Jupyter Notebook]
   
    execute: run_grover_attack_via_docker(key_length=6)
   ↓
[docker_helpers.py]
   
    mgr.exec_in_framework(python_attack_script)
   ↓
[subprocess.run]
   
    docker exec houdinis_framework bash -c "python3 ..."
   ↓
[houdinis_framework container]
   
    Import Houdinis modules
    from quantum.backend import QuantumBackendManager
    from exploits.grover_bruteforce import GroverBruteforceExploit
   ↓
[Quantum Attack Execution]
   
    - Initialize quantum circuit
    - Apply Grover iterations
    - Measure quantum states
    - Recover key/password
   ↓
[Target Attack]
   
    socket.connect(('target', 22))  # SSH
    ssl.connect(('target', 443))     # HTTPS
   ↓
[houdinis_target container]
   
    Services respond:
    - SSH accepts 'vulnerable' password
    - HTTPS exposes RSA certificate
   ↓
[Results Return Path]
   
    Container stdout/stderr captured
   ↓
[subprocess result]
   
    {'stdout': '...', 'stderr': '...', 'returncode': 0}
   ↓
[Jupyter Notebook]
   
    Display results with formatting
   >  Attack complete: Key found in 6 iterations!
```

##  Data Flow

```
Notebook Variable → JSON → Docker Exec → Container Python → Attack
     ↓                                                         ↓
Parameters                                              Target Service
key_length=6                                          (SSH/HTTPS/HTTP)
method='aes'                                                  ↓
target='target'                                         Vulnerable Response
                                                              ↓
Result ← JSON ← Docker Stdout ← Container Output ← Attack Complete
     ↓
Display in Notebook:
  - Success/Failure
  - Keys recovered
  - Iterations count
  - Quantum speedup
```

##  Security Isolation

```

  Internet                                    
    ↑                                         
      BLOCKED                              
                                             

     
      Firewall
     ↓

  Host Network (192.168.x.x)                 
    ↑                                        
      Port 7681 (localhost only)          
                                            

     
     ↓

  Docker Bridge: houdinis_net               
  Type: internal (no external routing)      
    ↑                                        
      Inter-container communication      
                                            
    
   houdinis_framework   houdinis_target 
      172.20.0.2      →   172.20.0.3    
    
                                            

```

##  Use Cases

### 1. Educational Demonstrations
```python
# In notebook cell:
run_grover_attack_via_docker(
    key_length=4,
    method='aes'
)
```
Shows quantum speedup for small key spaces.

### 2. Real Service Testing
```python
# Test SSH with quantum-accelerated password cracking
attack_ssh_password()

# Analyze TLS certificate vulnerability
attack_tls_rsa()
```
Demonstrates attacks on actual services.

### 3. Full Attack Chain
```python
# Execute complete demonstration
run_full_attack_demo()
```
Runs all attacks sequentially with reporting.

##  File Structure

```
Houdinis/
 docker/
    docker-compose.yml      # Container orchestration
    Dockerfile              # Framework image (CUDA + Houdinis)
    Dockerfile.vulnerable   # Target image (vulnerable services)

 notebooks/
    Grovers_Algorithm_Symmetric_Key_Attacks.ipynb  # Main notebook 
    docker_helpers.py       # Connection library 
    test_docker_integration.py  # Verification script 
    README.md               # Notebook documentation 

 quantum/
    backend.py              # Quantum backend management
    simulator.py            # Quantum simulators

 exploits/
     grover_bruteforce.py    # Grover's algorithm implementation
     ssh_quantum_attack.py   # SSH attack module
     tls_sndl.py            # TLS/HTTPS attack module
```

 = Files created/modified for notebook-docker integration

##  Quick Start Commands

```bash
# 1. Start Docker containers
cd docker
docker compose up -d

# 2. Verify integration
cd ../notebooks
python3 test_docker_integration.py

# 3. Start Jupyter
jupyter lab

# 4. Open notebook
# Grovers_Algorithm_Symmetric_Key_Attacks.ipynb

# 5. Run cells sequentially
# Cell 1: Check Docker status
# Cell 2: Verify connectivity
# Cell 3-7: Individual attacks
# Cell 8: Full demonstration
```

##  Integration Complete!

All components are now connected and ready to use.
