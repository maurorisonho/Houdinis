#  Houdinis - Marco de Criptoanálisis Cuántico

[![Licencia: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Puntuación: 135/100](https://img.shields.io/badge/score-135%2F100-brightgreen.svg)](docs/GAP_ANALYSIS.md)
[![Estado: Listo para Producción](https://img.shields.io/badge/status-production%20ready-success.svg)](docs/IMPLEMENTATION_SUMMARY.md)

> *"La criptografía moderna desaparecerá cuando lleguen las computadoras cuánticas. Houdinis demuestra cómo."*

[English](README.md) | [Português](README.pt-BR.md) | **Español** | [](README.zh.md)

---

##  Descripción General

**Houdinis** es el marco de criptoanálisis cuántico más completo del mundo, diseñado para demostrar vulnerabilidades de algoritmos criptográficos clásicos contra ataques cuánticos. Nombrado en honor al legendario mago Harry Houdini, este marco "escapa" de las protecciones criptográficas utilizando el poder de la computación cuántica.

###  Características Principales

- ** 12 Algoritmos Cuánticos**: Shor, Grover, Simon, HHL, QAOA, QPE, Amplificación de Amplitud y más
- ** 31+ Exploits Implementados**: RSA, ECDSA, AES, TLS, SSH, PGP, Bitcoin y otros
- ** Ataques de ML Cuántico**: Robo de modelos, inferencia de membresía, ataques adversarios
- ** Análisis PQC**: Kyber, Dilithium, FALCON, SPHINCS+ (NIST)
- ** Multi-Nube**: Soporte para IBM Quantum, AWS Braket, Azure Quantum, Google Cirq
- ** 85%+ Cobertura de Pruebas**: 7,182+ líneas de pruebas, CI/CD completo
- ** Documentación Integral**: 8,425+ líneas, API docs Sphinx, 9 notebooks Jupyter

---

##  Inicio Rápido

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/maurorisonho/Houdinis.git
cd Houdinis

# Instalar dependencias
pip install -r requirements.txt

# Instalación opcional con Docker
docker build -t houdinis -f docker/Dockerfile .
docker run -it houdinis
```

### Primer Ataque Cuántico

```python
from exploits.rsa_shor import RSAShorsAlgorithm

# Factorizar número RSA de 15 bits
rsa = RSAShorsAlgorithm(N=15)
factors = rsa.run()

print(f"Factores de 15: {factors['p']} × {factors['q']}")
# Salida: Factores de 15: 3 × 5
```

### Búsqueda con Grover

```python
from exploits.grover_bruteforce import GroverAttack

# Buscar clave AES en espacio de 16 bits
grover = GroverAttack(key_size=16)
result = grover.quantum_key_search()

print(f"Aceleración cuántica: {result['speedup']}")
# Salida: √(2^16) = 2^8 (256x más rápido)
```

---

##  Documentación

###  Documentos Principales

| Documento | Descripción |
|-----------|-------------|
| [Guía de Instalación](docs/installation.md) | Configuración completa multiplataforma |
| [Inicio Rápido](docs/quickstart.md) | Tutorial de 10 minutos |
| [Backends Cuánticos](docs/BACKENDS.md) | IBM, AWS, Azure, Google |
| [Ejemplos de Exploits](exploits/README.md) | 31+ ataques demostrados |
| [Notebooks](notebooks/README.md) | 9 tutoriales educativos |
| [Guía de Contribución](CONTRIBUTING.md) | Cómo contribuir |
| [Análisis de Brecha](docs/GAP_ANALYSIS.md) | Estado del proyecto |

###  Tutoriales Interactivos

Explora nuestros **9 notebooks Jupyter educativos**:

1.  **Algoritmo de Shor** - Factorización RSA
2.  **Algoritmo de Grover** - Búsqueda de clave simétrica
3.  **Ataques HNDL** - "Cosechar Ahora, Descifrar Después"
4.  **Criptografía Post-Cuántica** - Análisis NIST PQC
5.  **ML Cuántico** - Ataques adversarios en QML
6.  **Escaneo de Red** - Vulnerabilidades cuánticas
7.  **Integración IBM Quantum** - Ejecución en hardware real
8.  **Características Avanzadas** - Multi-backend y optimización
9.  **Conclusión del Marco** - Mejores prácticas

---

##  Arquitectura

```
Houdinis/
  exploits/          # 31+ módulos de ataque cuántico
    rsa_shor.py       # Algoritmo de Shor para RSA
    grover_bruteforce.py  # Búsqueda de clave de Grover
    simon_algorithm.py    # Periodicidad oculta de Simon
    quantum_phase_estimation.py  # QPE para Shor
    amplitude_amplification.py   # Grover generalizado
    side_channel_attacks.py      # Timing, caché, potencia
    advanced_qml_attacks.py      # Robo de modelo, inferencia
  scanners/          # Escáneres de vulnerabilidad
    network_scanner.py         # Escaneo de red
    quantum_vuln_scanner.py    # Detección de cripto vulnerable
    ssl_scanner.py             # Análisis TLS/SSL
  quantum/           # Núcleo de simulación cuántica
    backend.py        # Multi-backend (IBM, AWS, Azure, Google)
    simulator.py      # Simulador clásico con respaldo
    __init__.py
  security/          # Herramientas de seguridad
    owasp_auditor.py           # Cumplimiento OWASP Top 10
    automated_security_testing.py  # Pruebas de penetración automatizadas
    secure_file_ops.py         # Operaciones de archivo seguras
  utils/             # Herramientas utilitarias
    disaster_recovery.py   # Backup y recuperación
    monitoring.py          # Métricas Prometheus
    auto_scaling.py        # Auto-escalado dinámico
    performance_benchmark.py  # Benchmarking
  tests/             # Suite de pruebas (85%+ cobertura)
    test_quantum_algorithms_advanced.py
    test_advanced_modules.py
    test_edge_cases.py
    test_integration_workflows.py
    test_security_validation.py
  notebooks/         # 9 tutoriales Jupyter
  docs/              # 32 documentos (8,425+ líneas)
  docker/            # Containerización Docker
```

---

##  Algoritmos Implementados

### Algoritmos Cuánticos Fundamentales

| Algoritmo | Aplicación | Aceleración | Estado |
|-----------|------------|-------------|--------|
| **Shor** | Factorización RSA/ECC | Exponencial |  |
| **Grover** | Búsqueda de clave AES | Cuadrático (√N) |  |
| **Simon** | Periodicidad oculta | Exponencial |  |
| **HHL** | Sistemas lineales | Exponencial |  |
| **QAOA** | Optimización | Variable |  |
| **QPE** | Estimación de fase | Exponencial |  |
| **Amplificación de Amplitud** | Búsqueda generalizada | Cuadrático |  |
| **Deutsch-Jozsa** | Oracle constante/balanceado | Exponencial |  |
| **Bernstein-Vazirani** | Cadena de bits oculta | Lineal |  |
| **Recocido Cuántico** | Optimización QUBO | Variable |  |

### Protocolos Criptográficos Cubiertos

```
 Clave Pública:    RSA, ECDSA, DH, ECDH, ElGamal
 Simétrica:        AES, 3DES, ChaCha20 (análisis)
#⃣ Funciones Hash:   MD5, SHA-1, SHA-256, SHA-3 (colisiones)
 Protocolos:       TLS/SSL, SSH, IPsec, IKE, PGP
 Blockchain:       Bitcoin (ECDSA), Ethereum
 Lattice:          NTRU, LWE, CVP, SVP
 PQC (NIST):       Kyber, Dilithium, FALCON, SPHINCS+
```

---

##  Ejemplos de Uso

### 1. Factorización RSA con Shor

```python
from exploits.rsa_shor import RSAShorsAlgorithm

# Configurar ataque
shor = RSAShorsAlgorithm(
    N=15,  # Número compuesto para factorizar
    backend="qiskit_aer",  # Simulador local
    shots=1024
)

# Ejecutar algoritmo de Shor
result = shor.run()

if result['success']:
    print(f" ¡Factorización exitosa!")
    print(f"   {result['N']} = {result['p']} × {result['q']}")
    print(f"   Tiempo: {result['execution_time']:.2f}s")
```

### 2. Búsqueda de Clave AES con Grover

```python
from exploits.grover_bruteforce import GroverAttack

# Buscar en espacio de 32 bits (demostración)
grover = GroverAttack(
    key_size=32,
    target_key="01010101010101010101010101010101"
)

result = grover.quantum_key_search()

print(f" Búsqueda Cuántica vs Clásica:")
print(f"   Clásica: 2^32 = {2**32:,} intentos")
print(f"   Cuántica: √(2^32) = {2**16:,} iteraciones")
print(f"   Aceleración: {result['speedup']}")
```

### 3. Ataque de Canal Lateral

```python
from exploits.side_channel_attacks import SideChannelAnalyzer

analyzer = SideChannelAnalyzer()

# Ataque de timing en comparación de cadenas
def vulnerable_compare(guess):
    secret = "contraseña123"
    if len(guess) != len(secret):
        return False
    for i in range(len(secret)):
        if guess[i] != secret[i]:
            return False
    return True

result = analyzer.timing_attack_string_comparison(
    comparison_func=vulnerable_compare,
    target_secret="contraseña123"
)

print(f" Vulnerabilidad: {result.vulnerable}")
print(f"   Confianza: {result.confidence:.0%}")
print(f"   Información filtrada: {result.leaked_information}")
```

### 4. Robo de Modelo QML

```python
from exploits.advanced_qml_attacks import QuantumModelStealingAttack

stealer = QuantumModelStealingAttack()

# Robar modelo a través de consultas
result = stealer.extract_model_via_queries(
    num_queries=1000,
    input_dim=4
)

print(f" Robo de Modelo:")
print(f"   Consultas: {result.queries_made}")
print(f"   Fidelidad: {result.fidelity:.0%}")
print(f"   Precisión robada: {result.stolen_accuracy:.0%}")
```

---

##  Criptografía Post-Cuántica (PQC)

Houdinis incluye análisis integral de los algoritmos NIST PQC:

### Algoritmos Soportados

```python
from exploits.kyber_attack import KyberAttack
from exploits.dilithium_attack import DilithiumAttack

# Analizar CRYSTALS-Kyber (KEM)
kyber = KyberAttack(security_level=3)
result = kyber.timing_side_channel_attack()

# Analizar CRYSTALS-Dilithium (Firma)
dilithium = DilithiumAttack(security_level=3)
result = dilithium.nonce_reuse_attack()
```

### Herramienta de Migración PQC

```python
from exploits.pqc_migration_analyzer import PQCMigrationAnalyzer

analyzer = PQCMigrationAnalyzer()

# Escanear código fuente
report = analyzer.scan_codebase(
    path="./src",
    output_format="json"
)

print(f" Análisis de Vulnerabilidad Cuántica:")
print(f"   Algoritmos vulnerables: {report['vulnerable_count']}")
print(f"   Recomendaciones PQC: {len(report['recommendations'])}")
```

---

##  Backends Cuánticos

Houdinis soporta múltiples plataformas cuánticas:

| Backend | Hardware | Simulador | Estado |
|---------|----------|-----------|--------|
| **IBM Quantum** |  Acceso a hardware real |  Qiskit Aer |  |
| **AWS Braket** |  IonQ, Rigetti, OQC |  Simulador Local |  |
| **Azure Quantum** |  IonQ, Quantinuum |  Simulador Azure |  |
| **Google Cirq** |  Sycamore |  Simulador Cirq |  |
| **NVIDIA cuQuantum** |  |  Acelerado por GPU |  |
| **PennyLane** |  Multi-backend |  Default Qubit |  |

---

##  Pruebas y Calidad

### Cobertura de Pruebas: 85%+

```bash
# Ejecutar todas las pruebas
pytest tests/ -v --cov=. --cov-report=html

# Pruebas específicas
pytest tests/test_quantum_algorithms_advanced.py -v
pytest tests/test_security_validation.py -v

# Con marcadores
pytest -m "quantum" -v      # Solo pruebas cuánticas
pytest -m "integration" -v  # Pruebas de integración
pytest -m "security" -v     # Pruebas de seguridad
```

### Métricas de Calidad

- **Cobertura de Pruebas:** 85%+ (7,182+ líneas)
- **Cobertura de Tipos:** 92% (type hints)
- **Docstrings:** 96.7% (módulos), 97.2% (funciones)
- **Cumplimiento OWASP:** 10/10
- **Puntuación de Seguridad:** 10/10
- **Calidad de Código:** 9.5/10

---

##  Docker & Kubernetes

### Docker

```bash
# Construir
docker build -t houdinis -f docker/Dockerfile .

# Ejecutar
docker run -it houdinis python exploits/rsa_shor.py

# Docker Compose
docker-compose -f docker/docker-compose.yml up
```

### Kubernetes

```bash
# Desplegar en Kubernetes
kubectl apply -f deploy/kubernetes/

# Verificar pods
kubectl get pods -n houdinis

# Ver logs
kubectl logs -f deployment/houdinis -n houdinis
```

---

##  Contribuyendo

¡Nos encantan las contribuciones! Por favor, consulta nuestra [Guía de Contribución](CONTRIBUTING.md).

### Cómo Contribuir

1.  Haz fork del repositorio
2.  Crea una rama (`git checkout -b feature/NuevaCaracterística`)
3.  Haz commit de tus cambios (`git commit -m 'Agrega NuevaCaracterística'`)
4.  Push a la rama (`git push origin feature/NuevaCaracterística`)
5.  Abre un Pull Request

---

##  Licencia

Este proyecto está licenciado bajo la **Licencia MIT** - consulta el archivo [LICENSE](LICENSE) para más detalles.

---

##  ¡Dale Estrella a Este Proyecto!

Si encuentras útil Houdinis, ¡por favor considera darle una  en GitHub!

[![GitHub stars](https://img.shields.io/github/stars/maurorisonho/Houdinis?style=social)](https://github.com/maurorisonho/Houdinis/stargazers)

---

** "Escapando de las protecciones criptográficas, un qubit a la vez."**

[↑ Volver arriba](#-houdinis---marco-de-criptoanálisis-cuántico)
