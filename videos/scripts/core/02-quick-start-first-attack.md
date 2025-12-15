# Video Script: Quick Start - Your First Quantum Attack

**Video #:** 02  
**Duration:** 15 minutes  
**Difficulty:** Beginner  
**Prerequisites:** Houdinis installed (Video 01)

---

## Learning Objectives
1. Run your first quantum cryptanalysis attack
2. Understand Shor's algorithm basics
3. Factor a small RSA key
4. Interpret quantum circuit results
5. Navigate the framework CLI

---

## Timestamps
```
00:00 - Introduction & Demo Preview
02:00 - RSA Cryptography Quick Primer
04:30 - Generating Test RSA Keys
06:00 - Running Shor's Algorithm
09:00 - Understanding the Results
11:30 - Trying Different Backends
13:30 - Next Steps & Resources
```

---

## Script Outline

### Introduction (0:00-2:00)
- Welcome back, recap of installation
- Today: Break RSA encryption using quantum computing
- Demo preview: Show successful factorization
- "Don't worry if quantum physics seems complex - we'll take it step by step"

### RSA Primer (2:00-4:30)
- What is RSA? Public key cryptography
- Security based on factoring being hard (classically)
- Example: Factor 15 = 3 × 5 (easy), factor 2048-bit number (impossible classically)
- Quantum computers change everything: Shor's algorithm = polynomial time
- Visual: Show key generation, encryption, decryption flow

### Generate Test Keys (4:30-6:00)
```bash
# Generate small RSA key for demo
python -c "
from Crypto.PublicKey import RSA
key = RSA.generate(512)  # Small for demo
with open('demo_key.pem', 'wb') as f:
    f.write(key.export_key())
print(f'N = {key.n}')
print(f'e = {key.e}')
"
```
- Explain n (modulus), e (public exponent)
- "In reality, use 2048-4096 bits. We're using 512 for demo speed"

### Run Attack (6:00-9:00)
```bash
python exploits/rsa_shor.py --key demo_key.pem --backend qasm_simulator --verbose
```
- Watch output in real-time
- Explain each step: circuit creation, execution, measurement, classical post-processing
- Show progress bar, estimated time
- Success! Factors found

### Results Analysis (9:00-11:30)
- Display factors: p and q
- Verify: p × q = N
- Show private key reconstruction
- Time comparison: Classical vs Quantum
- Visualization: Circuit diagram, histogram

### Try Different Backends (11:30-13:30)
```bash
# Try different simulators
python exploits/rsa_shor.py --backend statevector_simulator --key demo_key.pem
python exploits/rsa_shor.py --backend aer_simulator --key demo_key.pem
```
- Compare execution times
- Discuss trade-offs: speed vs accuracy vs resource usage

### Conclusion (13:30-15:00)
- Recap: You just broke RSA encryption using quantum computing
- In next video: Grover's algorithm for symmetric keys
- Resources: Documentation, notebooks, Binder
- Call to action: Like, subscribe, try it yourself

---

## Visual Elements
- [ ] RSA encryption animation
- [ ] Shor's algorithm flowchart
- [ ] Quantum circuit diagram
- [ ] Measurement histogram
- [ ] Before/After comparison (encrypted → decrypted)

---

**Status:**  Ready for production
