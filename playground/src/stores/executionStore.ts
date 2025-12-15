/**
 * Houdinis Playground - Execution State Store
 * Developed by: Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)
 */
import { create } from 'zustand';

interface ExecutionState {
  output: string[];
  error: string | null;
  isExecuting: boolean;
  executionTime: number | null;
  circuitDiagram: string | null;
  measurementResults: Record<string, number> | null;
  addOutput: (line: string) => void;
  setError: (error: string | null) => void;
  setIsExecuting: (isExecuting: boolean) => void;
  setExecutionTime: (time: number | null) => void;
  setCircuitDiagram: (diagram: string | null) => void;
  setMeasurementResults: (results: Record<string, number> | null) => void;
  clearOutput: () => void;
  reset: () => void;
}

export const useExecutionStore = create<ExecutionState>((set) => ({
  output: [],
  error: null,
  isExecuting: false,
  executionTime: null,
  circuitDiagram: null,
  measurementResults: null,
  addOutput: (line) => set((state) => ({ output: [...state.output, line] })),
  setError: (error) => set({ error }),
  setIsExecuting: (isExecuting) => set({ isExecuting }),
  setExecutionTime: (executionTime) => set({ executionTime }),
  setCircuitDiagram: (circuitDiagram) => set({ circuitDiagram }),
  setMeasurementResults: (measurementResults) => set({ measurementResults }),
  clearOutput: () => set({ output: [], error: null, circuitDiagram: null, measurementResults: null }),
  reset: () =>
    set({
      output: [],
      error: null,
      isExecuting: false,
      executionTime: null,
      circuitDiagram: null,
      measurementResults: null,
    }),
}));
