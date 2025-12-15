/**
 * Houdinis Playground - Code Execution Hook
 * Developed by: Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)
 */
import { useCallback, useRef, useEffect } from 'react';
import { useExecutionStore } from '@/stores/executionStore';
import { loadPyodide } from '@/lib/jupyter/pyodide';

export function useCodeExecution() {
  const {
    addOutput,
    setError,
    setIsExecuting,
    setExecutionTime,
    clearOutput,
  } = useExecutionStore();

  const pyodideRef = useRef<any>(null);
  const isInitializedRef = useRef(false);

  // Initialize Pyodide once
  useEffect(() => {
    if (!isInitializedRef.current) {
      isInitializedRef.current = true;
      loadPyodide().then((pyodide) => {
        pyodideRef.current = pyodide;
        addOutput('Python kernel ready!');
      });
    }
  }, [addOutput]);

  const execute = useCallback(
    async (code: string) => {
      if (!pyodideRef.current) {
        setError('Python kernel not initialized. Please wait...');
        return;
      }

      clearOutput();
      setIsExecuting(true);
      setError(null);

      const startTime = performance.now();

      try {
        // Redirect stdout
        const output: string[] = [];
        pyodideRef.current.setStdout({
          batched: (msg: string) => {
            output.push(msg);
            addOutput(msg);
          },
        });

        // Execute code
        await pyodideRef.current.runPythonAsync(code);

        const endTime = performance.now();
        setExecutionTime((endTime - startTime) / 1000);
      } catch (err: any) {
        setError(err.message || 'Unknown error occurred');
        console.error('Execution error:', err);
      } finally {
        setIsExecuting(false);
      }
    },
    [addOutput, setError, setIsExecuting, setExecutionTime, clearOutput]
  );

  const stop = useCallback(() => {
    // Pyodide doesn't support interrupting execution directly
    // We would need to implement a worker-based solution for this
    setIsExecuting(false);
    setError('Execution interrupted (refresh page to reset kernel)');
  }, [setIsExecuting, setError]);

  return {
    execute,
    stop,
    isExecuting: useExecutionStore((state) => state.isExecuting),
  };
}
