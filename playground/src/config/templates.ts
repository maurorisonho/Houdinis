/**
 * Houdinis Playground - Quantum Circuit Templates
 * Desenvolvido: Lógica e Codificação por Humano e AI Assistida (Claude Sonnet 4.5)
 */

export interface QuantumTemplate {
  id: string;
  name: string;
  description: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  category: 'basics' | 'algorithms' | 'cryptanalysis' | 'qml';
  code: string;
  estimatedTime: string;
}

export const QUANTUM_TEMPLATES: QuantumTemplate[] = [
  // BEGINNER TEMPLATES
  {
    id: 'hello-quantum',
    name: 'Hello Quantum',
    description: 'Your first quantum circuit - create a superposition',
    difficulty: 'beginner',
    category: 'basics',
    estimatedTime: '2 min',
    code: `# Hello Quantum - Your First Circuit
from qiskit import QuantumCircuit
from qiskit_aer import Aer

# Create a quantum circuit with 1 qubit and 1 classical bit
qc = QuantumCircuit(1, 1)

# Apply Hadamard gate to create superposition
qc.h(0)

# Measure the qubit
qc.measure(0, 0)

# Draw the circuit
print(qc.draw(output='text'))

# Simulate
simulator = Aer.get_backend('qasm_simulator')
result = simulator.run(qc, shots=1024).result()
counts = result.get_counts()

print("\\nResults:")
print(counts)
`,
  },

  {
    id: 'bell-state',
    name: 'Bell State (Entanglement)',
    description: 'Create entangled qubits - the foundation of quantum computing',
    difficulty: 'beginner',
    category: 'basics',
    estimatedTime: '3 min',
    code: `# Bell State - Quantum Entanglement
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

# Create circuit with 2 qubits
qc = QuantumCircuit(2, 2)

# Create Bell state |Φ+ = (|00 + |11)/√2
qc.h(0)        # Hadamard on qubit 0
qc.cx(0, 1)    # CNOT gate (control=0, target=1)

# Measure both qubits
qc.measure([0, 1], [0, 1])

print(qc.draw(output='text'))

# Simulate
simulator = Aer.get_backend('qasm_simulator')
compiled = transpile(qc, simulator)
result = simulator.run(compiled, shots=1024).result()
counts = result.get_counts()

print("\\nMeasurement results:")
for state, count in counts.items():
    print(f"|{state}: {count} times ({count/1024*100:.1f}%)")
`,
  },

  {
    id: 'quantum-rng',
    name: 'Quantum Random Number Generator',
    description: 'Generate truly random numbers using quantum mechanics',
    difficulty: 'beginner',
    category: 'basics',
    estimatedTime: '3 min',
    code: `# Quantum Random Number Generator
from qiskit import QuantumCircuit
from qiskit_aer import Aer

def quantum_random_number(n_bits=8):
    """Generate n-bit random number using quantum superposition"""
    qc = QuantumCircuit(n_bits, n_bits)
    
    # Create superposition on all qubits
    for i in range(n_bits):
        qc.h(i)
    
    # Measure all qubits
    qc.measure(range(n_bits), range(n_bits))
    
    # Simulate
    simulator = Aer.get_backend('qasm_simulator')
    result = simulator.run(qc, shots=1).result()
    counts = result.get_counts()
    
    # Convert binary string to integer
    binary_string = list(counts.keys())[0]
    random_number = int(binary_string, 2)
    
    return random_number

# Generate 10 random 8-bit numbers
print("Quantum Random Numbers (0-255):")
for i in range(10):
    num = quantum_random_number(8)
    print(f"  #{i+1}: {num}")
`,
  },

  // INTERMEDIATE TEMPLATES
  {
    id: 'grover-search',
    name: "Grover's Algorithm",
    description: 'Quantum search with quadratic speedup - find marked items',
    difficulty: 'intermediate',
    category: 'algorithms',
    estimatedTime: '10 min',
    code: `# Grover's Algorithm - Quantum Search
from qiskit import QuantumCircuit
from qiskit_aer import Aer
import numpy as np

def grover_oracle(n, marked_states):
    """Create oracle that marks specific states"""
    qc = QuantumCircuit(n)
    
    for target in marked_states:
        # Convert target to binary
        binary = format(target, f'0{n}b')
        
        # Flip qubits that should be 0
        for i, bit in enumerate(binary):
            if bit == '0':
                qc.x(i)
        
        # Multi-controlled Z gate
        qc.h(n-1)
        qc.mcx(list(range(n-1)), n-1)
        qc.h(n-1)
        
        # Flip back
        for i, bit in enumerate(binary):
            if bit == '0':
                qc.x(i)
    
    return qc

def grover_diffusion(n):
    """Diffusion operator (inversion about average)"""
    qc = QuantumCircuit(n)
    
    # Apply H-gates
    qc.h(range(n))
    
    # Apply X-gates
    qc.x(range(n))
    
    # Multi-controlled Z
    qc.h(n-1)
    qc.mcx(list(range(n-1)), n-1)
    qc.h(n-1)
    
    # Apply X-gates
    qc.x(range(n))
    
    # Apply H-gates
    qc.h(range(n))
    
    return qc

# Search for item 3 in database of 8 items (3 qubits)
n = 3
marked = [3]  # Looking for |011

# Calculate optimal iterations
N = 2**n
iterations = int(np.pi/4 * np.sqrt(N))

# Build circuit
qc = QuantumCircuit(n, n)

# Initialize superposition
qc.h(range(n))

# Apply Grover operator
for _ in range(iterations):
    qc.compose(grover_oracle(n, marked), inplace=True)
    qc.compose(grover_diffusion(n), inplace=True)

# Measure
qc.measure(range(n), range(n))

print(f"Searching for item {marked[0]} in database of {N} items")
print(f"Grover iterations: {iterations}\\n")
print(qc.draw(output='text'))

# Simulate
simulator = Aer.get_backend('qasm_simulator')
result = simulator.run(qc, shots=1024).result()
counts = result.get_counts()

print("\\nSearch results:")
for state, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
    decimal = int(state, 2)
    prob = count/1024*100
    marker = " ← TARGET!" if decimal in marked else ""
    print(f"|{state} (decimal {decimal}): {prob:.1f}%{marker}")
`,
  },

  {
    id: 'shor-factorization',
    name: "Shor's Algorithm",
    description: 'Factor large numbers exponentially faster - break RSA',
    difficulty: 'advanced',
    category: 'cryptanalysis',
    estimatedTime: '15 min',
    code: `# Shor's Algorithm - Integer Factorization
from qiskit import QuantumCircuit
from qiskit_aer import Aer
import numpy as np
from math import gcd
from fractions import Fraction

def qft(n):
    """Quantum Fourier Transform"""
    qc = QuantumCircuit(n)
    for j in range(n):
        qc.h(j)
        for k in range(j+1, n):
            qc.cp(np.pi/2**(k-j), k, j)
    # Swap qubits
    for i in range(n//2):
        qc.swap(i, n-i-1)
    return qc

def c_amod15(a, power):
    """Controlled U gate: |y → |ay mod 15"""
    U = QuantumCircuit(4)
    for _ in range(power):
        if a == 2:
            U.swap(0, 1)
            U.swap(1, 2)
            U.swap(2, 3)
        elif a == 7:
            U.swap(2, 3)
            U.swap(1, 2)
            U.swap(0, 1)
        elif a == 8:
            U.swap(0, 1)
            U.swap(1, 2)
            U.swap(2, 3)
        elif a == 11:
            U.swap(1, 3)
            U.swap(0, 2)
        elif a == 13:
            U.swap(0, 3)
            U.swap(1, 2)
    U = U.to_gate()
    U.name = f"{a}^{power} mod 15"
    c_U = U.control()
    return c_U

# Shor's algorithm to factor N = 15
N = 15
a = 7  # Random coprime to 15

n_count = 8  # Counting qubits
qc = QuantumCircuit(n_count + 4, n_count)

# Initialize |1 in auxiliary register
qc.x(n_count)

# Apply Hadamard gates to counting register
for q in range(n_count):
    qc.h(q)

# Apply controlled-U operations
for q in range(n_count):
    qc.append(
        c_amod15(a, 2**q),
        [q] + list(range(n_count, n_count + 4))
    )

# Apply inverse QFT
qc.append(qft(n_count).inverse(), range(n_count))

# Measure
qc.measure(range(n_count), range(n_count))

print(f"Shor's Algorithm: Factoring N = {N}")
print(f"Using a = {a}\\n")

# Simulate
simulator = Aer.get_backend('qasm_simulator')
result = simulator.run(qc, shots=2048).result()
counts = result.get_counts()

# Find period from measurement results
measured_phases = []
for output in counts:
    decimal = int(output, 2)
    phase = decimal / (2**n_count)
    measured_phases.append(phase)

print("Top measurement results:")
for output, count in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:5]:
    decimal = int(output, 2)
    phase = decimal / (2**n_count)
    print(f"  {output}: {count} times (phase = {phase:.3f})")

# Find period from phase
from fractions import Fraction
phases = [Fraction(int(output, 2), 2**n_count).limit_denominator(N) 
          for output in counts.keys()]
periods = [frac.denominator for frac in phases]

print(f"\\nEstimated periods: {set(periods)}")

# Factor N using period
for r in set(periods):
    if r % 2 == 0:
        guesses = [gcd(a**(r//2) - 1, N), gcd(a**(r//2) + 1, N)]
        for guess in guesses:
            if guess not in [1, N] and N % guess == 0:
                print(f"\\n SUCCESS! Factors found: {guess} × {N//guess} = {N}")
                break
`,
  },
];

export function getTemplateById(id: string): QuantumTemplate | undefined {
  return QUANTUM_TEMPLATES.find((t) => t.id === id);
}

export function getTemplatesByCategory(category: string): QuantumTemplate[] {
  return QUANTUM_TEMPLATES.filter((t) => t.category === category);
}

export function getTemplatesByDifficulty(difficulty: string): QuantumTemplate[] {
  return QUANTUM_TEMPLATES.filter((t) => t.difficulty === difficulty);
}
