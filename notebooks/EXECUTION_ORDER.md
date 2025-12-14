#  Houdinis Notebooks - Execution Order Guide

**IMPORTANT:** Execute notebooks in this specific order to ensure proper dependencies and progressive learning.

---

##  Complete Execution Sequence

### 1⃣ IBM_Quantum_Experience_Integration.ipynb
**Category:** Foundation & Setup  
**Dependencies:** None (START HERE)  
**Execution Time:** ~10-15 minutes

**Purpose:**
- Configure quantum backends (Aer simulators, IBM Quantum)
- Establish Docker container integration  
- Test quantum circuit execution
- Validate Qiskit installation

**Why First:**
- Sets up all quantum computing infrastructure
- Required by ALL subsequent notebooks
- Establishes Docker network for attack simulations

**Key Outputs:**
-  Quantum backends configured
-  Docker containers running
-  Bell state execution verified

---

### 2⃣ Shors_Algorithm_RSA_Exploitation.ipynb
**Category:** Public-Key Cryptanalysis  
**Dependencies:** Notebook #1  
**Execution Time:** ~15-20 minutes

**Purpose:**
- Shor's algorithm for RSA factorization
- Quantum period finding demonstration
- Private key recovery from public keys
- Attack complexity analysis

**Why Second:**
- Most critical quantum threat to modern crypto
- Foundation for understanding quantum advantage
- Demonstrates exponential speedup

**Key Outputs:**
-  RSA factorization demonstrated
-  Quantum vs classical comparison
-  Attack complexity visualized

---

### 3⃣ Grovers_Algorithm_Symmetric_Key_Attacks.ipynb
**Category:** Symmetric Cryptanalysis  
**Dependencies:** Notebooks #1, #2  
**Execution Time:** ~15-20 minutes

**Purpose:**
- Grover's algorithm for key search
- AES key recovery demonstrations
- Quadratic speedup for brute-force
- Symmetric crypto vulnerability assessment

**Why Third:**
- Complements Shor's algorithm (asymmetric + symmetric)
- Establishes full quantum threat landscape
- Required for network scanning techniques

**Key Outputs:**
-  AES key search demonstrated
-  Grover's quadratic speedup verified
-  Oracle function implementations

---

### 4⃣ Quantum_Network_Scanning.ipynb
**Category:** Network Reconnaissance  
**Dependencies:** Notebooks #1-3, Docker containers  
**Execution Time:** ~20-25 minutes

**Purpose:**
- Quantum-enhanced network discovery
- Grover's algorithm for port scanning
- Parallel quantum reconnaissance
- Vulnerability assessment with quantum speedup

**Why Fourth:**
- Applies Grover's algorithm to practical scenarios
- Requires Docker targets configured
- Foundation for HNDL attacks

**Key Outputs:**
-  Quantum port scanning demonstrated
-  Network topology discovered
-  Vulnerability database queried

---

### 5⃣ Harvest_Now_Decrypt_Later_Attacks.ipynb
**Category:** Strategic Attack Planning  
**Dependencies:** Notebooks #1-4  
**Execution Time:** ~20-30 minutes

**Purpose:**
- HNDL attack strategy and timeline
- TLS/SSH traffic capture simulation
- Future decryption risk assessment
- Economic impact analysis

**Why Fifth:**
- Demonstrates real-world quantum threat
- Motivates PQC migration urgency
- Prepares context for PQC analysis

**Key Outputs:**
-  HNDL strategy timeline
-  Traffic capture simulation
-  Risk assessment matrix

---

### 6⃣ Post_Quantum_Cryptography_Analysis.ipynb
**Category:** Defense & Mitigation  
**Dependencies:** Notebooks #1-5, Docker containers  
**Execution Time:** ~25-30 minutes

**Purpose:**
- NIST PQC algorithms (Kyber, Dilithium, SPHINCS+)
- Migration strategies and timelines
- Performance: Classical vs PQC vs Hybrid
- Organization-specific recommendations

**Why Sixth:**
- Provides solutions to quantum threats
- Analyzes defense mechanisms
- Critical for security professionals

**Key Outputs:**
-  PQC algorithms compared
-  Migration roadmap created
-  Performance benchmarks
-  Crypto vulnerabilities discovered

---

### 7⃣ Quantum_Machine_Learning_Cryptanalysis.ipynb
**Category:** Advanced Techniques  
**Dependencies:** Notebooks #1-3  
**Execution Time:** ~30-40 minutes

**Purpose:**
- Quantum Neural Networks (QNN)
- Variational Quantum Classifiers (VQC)
- Quantum feature maps
- Advanced ML-based quantum attacks

**Why Seventh:**
- Requires understanding of basic quantum algorithms
- Advanced topic building on foundations
- Cutting-edge research area

**Key Outputs:**
-  QNN architecture demonstrated
-  Quantum classification results
-  Feature map visualizations

---

### 8⃣ Houdinis_Advanced_Features.ipynb
**Category:** Framework Integration  
**Dependencies:** ALL previous notebooks (#1-7)  
**Execution Time:** ~40-60 minutes

**Purpose:**
- Integration of all Houdinis modules
- Multi-algorithm attack scenarios
- Real-world exploitation demonstrations
- Framework optimization techniques

**Why Eighth:**
- Requires comprehensive understanding
- Demonstrates full framework capabilities
- Practical attack orchestration

**Key Outputs:**
-  Multi-attack scenarios executed
-  Framework modules integrated
-  Real-world exploits demonstrated

---

### 9⃣ Houdinis_Framework_Conclusion.ipynb
**Category:** Synthesis & Summary  
**Dependencies:** ALL previous notebooks (#1-8)  
**Execution Time:** ~20-30 minutes

**Purpose:**
- Comprehensive framework summary
- Synthesis of all attack methods
- Strategic recommendations
- Future quantum security landscape

**Why Last:**
- Synthesizes entire learning journey
- Provides big-picture perspective
- Final recommendations and conclusions

**Key Outputs:**
-  Complete framework summary
-  Strategic recommendations
-  Future roadmap

---

##  Dependency Graph

```
IBM_Quantum_Experience_Integration (#1)
    
     Shors_Algorithm_RSA_Exploitation (#2)
         
          Grovers_Algorithm_Symmetric_Key_Attacks (#3)
               
                Quantum_Network_Scanning (#4)
                    
                     Harvest_Now_Decrypt_Later_Attacks (#5)
                          
                           Post_Quantum_Cryptography_Analysis (#6)
               
                Quantum_Machine_Learning_Cryptanalysis (#7)
    
     All converge to:
          
           Houdinis_Advanced_Features (#8)
          
           Houdinis_Framework_Conclusion (#9)
```

---

##  Quick Start

### Prerequisites

```bash
# 1. Install Python dependencies
pip install qiskit qiskit-aer qiskit-algorithms matplotlib numpy pandas

# 2. Start Docker containers
cd /home/test/Downloads/github/portifolio/Houdinis/docker
docker-compose up -d

# 3. Verify containers are running
docker ps | grep houdinis
# Should show:
#   - houdinis_framework (quantum attack tools)
#   - houdinis_target (vulnerable services)

# 4. Check container IPs
docker inspect houdinis_framework | grep IPAddress
docker inspect houdinis_target | grep IPAddress
```

### Execute Notebooks

```bash
# Open Jupyter Lab
cd /home/test/Downloads/github/portifolio/Houdinis/notebooks
jupyter lab

# Execute notebooks IN ORDER:
# 1. IBM_Quantum_Experience_Integration.ipynb
# 2. Shors_Algorithm_RSA_Exploitation.ipynb
# 3. Grovers_Algorithm_Symmetric_Key_Attacks.ipynb
# 4. Quantum_Network_Scanning.ipynb
# 5. Harvest_Now_Decrypt_Later_Attacks.ipynb
# 6. Post_Quantum_Cryptography_Analysis.ipynb
# 7. Quantum_Machine_Learning_Cryptanalysis.ipynb
# 8. Houdinis_Advanced_Features.ipynb
# 9. Houdinis_Framework_Conclusion.ipynb
```

---

##  Execution Checklist

### Before Starting
- [ ] Docker installed and running
- [ ] Python 3.8+ installed
- [ ] Qiskit and dependencies installed
- [ ] Docker containers started
- [ ] Jupyter Lab/Notebook running

### Notebook #1 (IBM Quantum)
- [ ] Quantum backends configured
- [ ] Docker containers detected
- [ ] Bell state executed successfully
- [ ] Backend performance benchmarked

### Notebook #2 (Shor's Algorithm)
- [ ] Shor's algorithm demonstrated
- [ ] RSA factorization explained
- [ ] Quantum period finding shown
- [ ] Complexity comparison visualized

### Notebook #3 (Grover's Algorithm)
- [ ] Grover's search demonstrated
- [ ] AES key recovery shown
- [ ] Oracle functions implemented
- [ ] Quadratic speedup verified

### Notebook #4 (Network Scanning)
- [ ] Quantum port scan executed
- [ ] Docker targets scanned
- [ ] Vulnerabilities discovered
- [ ] Grover's applied to reconnaissance

### Notebook #5 (HNDL Attacks)
- [ ] HNDL strategy explained
- [ ] Traffic capture simulated
- [ ] Risk timeline created
- [ ] Economic impact assessed

### Notebook #6 (PQC Analysis)
- [ ] PQC algorithms compared
- [ ] Migration plan created
- [ ] Performance benchmarks run
- [ ] Docker target analyzed
- [ ] Crypto vulnerabilities assessed

### Notebook #7 (Quantum ML)
- [ ] QNN architecture created
- [ ] Quantum classifiers trained
- [ ] Feature maps demonstrated
- [ ] ML attacks explained

### Notebook #8 (Advanced Features)
- [ ] Multi-attack scenarios run
- [ ] All modules integrated
- [ ] Real-world exploits shown
- [ ] Framework optimized

### Notebook #9 (Conclusion)
- [ ] Framework summary reviewed
- [ ] All techniques synthesized
- [ ] Recommendations noted
- [ ] Future roadmap understood

---

## ⏱ Time Estimates

| Notebook | Execution Time | Cumulative |
|----------|---------------|------------|
| #1 IBM Quantum | 10-15 min | 0:15 |
| #2 Shor's Algorithm | 15-20 min | 0:35 |
| #3 Grover's Algorithm | 15-20 min | 0:55 |
| #4 Network Scanning | 20-25 min | 1:20 |
| #5 HNDL Attacks | 20-30 min | 1:50 |
| #6 PQC Analysis | 25-30 min | 2:20 |
| #7 Quantum ML | 30-40 min | 3:00 |
| #8 Advanced Features | 40-60 min | 4:00 |
| #9 Conclusion | 20-30 min | 4:30 |

**Total:** ~4-5 hours

**Recommended:** Split into 3 sessions:
- **Session 1:** Notebooks #1-3 (1 hour)
- **Session 2:** Notebooks #4-6 (1.5 hours)
- **Session 3:** Notebooks #7-9 (2 hours)

---

##  Important Notes

### Docker Requirements

Notebooks requiring Docker containers:
-  #1 - IBM Quantum (setup)
-  #4 - Network Scanning (attack target)
-  #5 - HNDL Attacks (traffic capture)
-  #6 - PQC Analysis (vulnerability assessment)

**Check container status before these notebooks:**
```bash
docker ps | grep houdinis
```

**Restart containers if needed:**
```bash
docker-compose down
docker-compose up -d
```

### Path Configuration

All notebooks use this path:
```python
sys.path.append('/home/test/Downloads/github/portifolio/Houdinis')
```

**Verify your installation path matches!**

### Common Issues

1. **"ModuleNotFoundError: No module named 'qiskit'"**
   ```bash
   pip install qiskit qiskit-aer
   ```

2. **"Docker containers not found"**
   ```bash
   cd docker && docker-compose up -d
   ```

3. **"Quantum backend not available"**
   - Run Notebook #1 first
   - Check Qiskit installation

4. **"Target IP not accessible"**
   ```bash
   docker inspect houdinis_target | grep IPAddress
   ```

---

##  Legal Disclaimer

These notebooks are for **authorized security testing and educational purposes only**.

-  Use only on systems you own
-  Get explicit permission for testing
-  Follow all applicable laws and regulations
-  Respect responsible disclosure practices

---

##  Support & Contact

**Author:** Mauro Risonho de Paula Assumpção (firebitsbr)  
**Email:** mauro.risonho@gmail.com  
**GitHub:** https://github.com/firebitsbr/Houdinis  
**License:** MIT

---

##  Learning Path

### Beginner Path (First-time users)
1. Start with Notebook #1 (IBM Quantum)
2. Read all explanations carefully
3. Execute cells one by one
4. Review visualizations
5. Take notes on key concepts

### Intermediate Path (Some quantum knowledge)
1. Quick review of Notebook #1
2. Focus on Notebooks #2-6
3. Experiment with parameters
4. Try modifying attack scenarios

### Advanced Path (Experienced users)
1. Quick verification of Notebook #1
2. Focus on Notebooks #7-9
3. Integrate with your own tools
4. Contribute improvements

---

##  Additional Resources

### Quantum Computing
- [Qiskit Textbook](https://qiskit.org/textbook/)
- [IBM Quantum Learning](https://learning.quantum.ibm.com/)
- [Quantum Computing for Computer Scientists](https://www.cambridge.org/core/books/quantum-computing-for-computer-scientists/)

### Cryptography
- [Post-Quantum Cryptography - NIST](https://csrc.nist.gov/projects/post-quantum-cryptography)
- [Cryptographic Right Answers](https://latacora.micro.blog/2018/04/03/cryptographic-right-answers.html)

### Security Research
- [IACR Cryptology ePrint Archive](https://eprint.iacr.org/)
- [Quantum Safe Security Working Group](https://www.etsi.org/committee/quantum-safe-security)

---

**Last Updated:** December 14, 2025  
**Version:** 2.0
