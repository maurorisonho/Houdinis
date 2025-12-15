/**
 * Houdinis Playground - Editor State Store
 * Desenvolvido: Lógica e Codificação por Humano e AI Assistida (Claude Sonnet 4.5)
 */
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface EditorState {
  code: string;
  isModified: boolean;
  language: string;
  theme: 'vs-dark' | 'vs-light';
  fontSize: number;
  setCode: (code: string) => void;
  setIsModified: (isModified: boolean) => void;
  setLanguage: (language: string) => void;
  setTheme: (theme: 'vs-dark' | 'vs-light') => void;
  setFontSize: (fontSize: number) => void;
  reset: () => void;
}

const DEFAULT_CODE = `# Houdinis Quantum Playground
# Write your quantum cryptanalysis code here

from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

# Create a simple quantum circuit
qc = QuantumCircuit(2, 2)
qc.h(0)  # Hadamard gate on qubit 0
qc.cx(0, 1)  # CNOT gate (control=0, target=1)
qc.measure([0, 1], [0, 1])  # Measure both qubits

# Draw the circuit
print(qc.draw(output='text'))

# Simulate the circuit
simulator = Aer.get_backend('qasm_simulator')
compiled_circuit = transpile(qc, simulator)
result = simulator.run(compiled_circuit, shots=1024).result()
counts = result.get_counts()

# Print results
print("\\nMeasurement results:")
for outcome, count in counts.items():
    print(f"{outcome}: {count}")
`;

export const useEditorStore = create<EditorState>()(
  persist(
    (set) => ({
      code: DEFAULT_CODE,
      isModified: false,
      language: 'python',
      theme: 'vs-dark',
      fontSize: 14,
      setCode: (code) => set({ code, isModified: true }),
      setIsModified: (isModified) => set({ isModified }),
      setLanguage: (language) => set({ language }),
      setTheme: (theme) => set({ theme }),
      setFontSize: (fontSize) => set({ fontSize }),
      reset: () => set({ code: DEFAULT_CODE, isModified: false }),
    }),
    {
      name: 'houdinis-editor-storage',
      partialize: (state) => ({
        theme: state.theme,
        fontSize: state.fontSize,
      }),
    }
  )
);
