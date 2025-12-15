#  Houdinis - 

[![: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![: 135/100](https://img.shields.io/badge/score-135%2F100-brightgreen.svg)](docs/GAP_ANALYSIS.md)
[![: ](https://img.shields.io/badge/status-production%20ready-success.svg)](docs/IMPLEMENTATION_SUMMARY.md)

> *"Houdinis "*

[English](README.md) | [Português](README.pt-BR.md) | [Español](README.es.md) | ****

---

##  

**Houdinis** ·Harry Houdini""

###  

- ** 12 **: ShorGroverSimonHHLQAOAQPE
- ** 31+ **: RSAECDSAAESTLSSSHPGP
- ** **: 
- ** PQC **: KyberDilithiumFALCONSPHINCS+ (NIST)
- ** **: IBM QuantumAWS BraketAzure QuantumGoogle Cirq
- ** 85%+ **: 7,182+  CI/CD
- ** **: 8,425+ Sphinx API 9  Jupyter 

---

##  

### 

```bash
# 
git clone https://github.com/maurorisonho/Houdinis.git
cd Houdinis

# 
pip install -r requirements.txt

#  Docker 
docker build -t houdinis -f docker/Dockerfile .
docker run -it houdinis
```

### 

```python
from exploits.rsa_shor import RSAShorsAlgorithm

#  15  RSA 
rsa = RSAShorsAlgorithm(N=15)
factors = rsa.run()

print(f"15 : {factors['p']} × {factors['q']}")
# : 15 : 3 × 5
```

### Grover 

```python
from exploits.grover_bruteforce import GroverAttack

#  16  AES 
grover = GroverAttack(key_size=16)
result = grover.quantum_key_search()

print(f": {result['speedup']}")
# : √(2^16) = 2^8 ( 256 )
```

---

##  

###  

|  |  |
|------|------|
| [](docs/installation.md) |  |
| [](docs/quickstart.md) | 10  |
| [](docs/BACKENDS.md) | IBMAWSAzureGoogle |
| [](exploits/README.md) | 31+  |
| [](notebooks/README.md) | 9  |
| [](CONTRIBUTING.md) |  |
| [](docs/GAP_ANALYSIS.md) |  |

###  

 **9  Jupyter **:

1.  **Shor ** - RSA 
2.  **Grover ** - 
3.  **HNDL ** - ""
4.  **** - NIST PQC 
5.  **** - QML 
6.  **** - 
7.  **IBM Quantum ** - 
8.  **** - 
9.  **** - 

---

##  

```
Houdinis/
  exploits/          # 31+ 
    rsa_shor.py       # RSA  Shor 
    grover_bruteforce.py  # Grover 
    simon_algorithm.py    # Simon 
    quantum_phase_estimation.py  # Shor  QPE
    amplitude_amplification.py   #  Grover
    side_channel_attacks.py      # 
    advanced_qml_attacks.py      # 
  scanners/          # 
    network_scanner.py         # 
    quantum_vuln_scanner.py    # 
    ssl_scanner.py             # TLS/SSL 
  quantum/           # 
    backend.py        #  (IBM, AWS, Azure, Google)
    simulator.py      # 
    __init__.py
  security/          # 
    owasp_auditor.py           # OWASP Top 10 
    automated_security_testing.py  # 
    secure_file_ops.py         # 
  utils/             # 
    disaster_recovery.py   # 
    monitoring.py          # Prometheus 
    auto_scaling.py        # 
    performance_benchmark.py  # 
  tests/             #  (85%+ )
    test_quantum_algorithms_advanced.py
    test_advanced_modules.py
    test_edge_cases.py
    test_integration_workflows.py
    test_security_validation.py
  notebooks/         # 9  Jupyter 
  docs/              # 32  (8,425+ )
  docker/            # Docker 
```

---

##  

### 

|  |  |  |  |
|------|------|------|------|
| **Shor** | RSA/ECC  |  |  |
| **Grover** | AES  |  (√N) |  |
| **Simon** |  |  |  |
| **HHL** |  |  |  |
| **QAOA** |  |  |  |
| **QPE** |  |  |  |
| **** |  |  |  |
| **Deutsch-Jozsa** | / |  |  |
| **Bernstein-Vazirani** |  |  |  |
| **** | QUBO  |  |  |

### 

```
 :         RSA, ECDSA, DH, ECDH, ElGamal
 :         AES, 3DES, ChaCha20 ()
#⃣ :     MD5, SHA-1, SHA-256, SHA-3 ()
 :         TLS/SSL, SSH, IPsec, IKE, PGP
 :        (ECDSA), 
 :       NTRU, LWE, CVP, SVP
 PQC (NIST):  Kyber, Dilithium, FALCON, SPHINCS+
```

---

##  

### 1.  Shor  RSA 

```python
from exploits.rsa_shor import RSAShorsAlgorithm

# 
shor = RSAShorsAlgorithm(
    N=15,  # 
    backend="qiskit_aer",  # 
    shots=1024
)

#  Shor 
result = shor.run()

if result['success']:
    print(f" !")
    print(f"   {result['N']} = {result['p']} × {result['q']}")
    print(f"   : {result['execution_time']:.2f}")
```

### 2.  Grover  AES 

```python
from exploits.grover_bruteforce import GroverAttack

#  32 
grover = GroverAttack(
    key_size=32,
    target_key="01010101010101010101010101010101"
)

result = grover.quantum_key_search()

print(f"  vs :")
print(f"   : 2^32 = {2**32:,} ")
print(f"   : √(2^32) = {2**16:,} ")
print(f"   : {result['speedup']}")
```

### 3. 

```python
from exploits.side_channel_attacks import SideChannelAnalyzer

analyzer = SideChannelAnalyzer()

# 
def vulnerable_compare(guess):
    secret = "123"
    if len(guess) != len(secret):
        return False
    for i in range(len(secret)):
        if guess[i] != secret[i]:
            return False
    return True

result = analyzer.timing_attack_string_comparison(
    comparison_func=vulnerable_compare,
    target_secret="123"
)

print(f" : {result.vulnerable}")
print(f"   : {result.confidence:.0%}")
print(f"   : {result.leaked_information}")
```

### 4. QML 

```python
from exploits.advanced_qml_attacks import QuantumModelStealingAttack

stealer = QuantumModelStealingAttack()

# 
result = stealer.extract_model_via_queries(
    num_queries=1000,
    input_dim=4
)

print(f" :")
print(f"   : {result.queries_made}")
print(f"   : {result.fidelity:.0%}")
print(f"   : {result.stolen_accuracy:.0%}")
```

---

##   (PQC)

Houdinis  NIST PQC :

### 

```python
from exploits.kyber_attack import KyberAttack
from exploits.dilithium_attack import DilithiumAttack

#  CRYSTALS-Kyber (KEM)
kyber = KyberAttack(security_level=3)
result = kyber.timing_side_channel_attack()

#  CRYSTALS-Dilithium ()
dilithium = DilithiumAttack(security_level=3)
result = dilithium.nonce_reuse_attack()
```

### PQC 

```python
from exploits.pqc_migration_analyzer import PQCMigrationAnalyzer

analyzer = PQCMigrationAnalyzer()

# 
report = analyzer.scan_codebase(
    path="./src",
    output_format="json"
)

print(f" :")
print(f"   : {report['vulnerable_count']}")
print(f"   PQC : {len(report['recommendations'])}")
```

---

##  

Houdinis :

|  |  |  |  |
|------|------|--------|------|
| **IBM Quantum** |   |  Qiskit Aer |  |
| **AWS Braket** |  IonQ, Rigetti, OQC |   |  |
| **Azure Quantum** |  IonQ, Quantinuum |  Azure  |  |
| **Google Cirq** |  Sycamore |  Cirq  |  |
| **NVIDIA cuQuantum** |  |  GPU  |  |
| **PennyLane** |   |   |  |

---

##  

### : 85%+

```bash
# 
pytest tests/ -v --cov=. --cov-report=html

# 
pytest tests/test_quantum_algorithms_advanced.py -v
pytest tests/test_security_validation.py -v

# 
pytest -m "quantum" -v      # 
pytest -m "integration" -v  # 
pytest -m "security" -v     # 
```

### 

- **:** 85%+ (7,182+ )
- **:** 92% ()
- **:** 96.7% (), 97.2% ()
- **OWASP :** 10/10
- **:** 10/10
- **:** 9.5/10

---

##  Docker & Kubernetes

### Docker

```bash
# 
docker build -t houdinis -f docker/Dockerfile .

# 
docker run -it houdinis python exploits/rsa_shor.py

# Docker Compose
docker-compose -f docker/docker-compose.yml up
```

### Kubernetes

```bash
#  Kubernetes
kubectl apply -f deploy/kubernetes/

#  pods
kubectl get pods -n houdinis

# 
kubectl logs -f deployment/houdinis -n houdinis
```

---

##  

[](CONTRIBUTING.md)

### 

1.  Fork 
2.   (`git checkout -b feature/`)
3.   (`git commit -m ''`)
4.   (`git push origin feature/`)
5.   Pull Request

---

##  

 **MIT ** -  [LICENSE](LICENSE) 

---

##  

- **:** Mauro Risonho de Paula Assumpção (firebitsbr)
- **:** maurorisonho@gmail.com
- **GitHub:** [@maurorisonho](https://github.com/maurorisonho)
- **:** [github.com/maurorisonho/Houdinis](https://github.com/maurorisonho/Houdinis)

---

##  

 Houdinis  GitHub  

[![GitHub stars](https://img.shields.io/github/stars/maurorisonho/Houdinis?style=social)](https://github.com/maurorisonho/Houdinis/stargazers)

---

** ""**

[↑ ](#-houdinis---)
