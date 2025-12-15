/**
 * Houdinis Playground - Pyodide Loader and Manager
 * Desenvolvido: Lógica e Codificação por Humano e AI Assistida (Claude Sonnet 4.5)
 */

let pyodideInstance: any = null;
let loadingPromise: Promise<any> | null = null;

export async function loadPyodide() {
  // Return cached instance if already loaded
  if (pyodideInstance) {
    return pyodideInstance;
  }

  // Return existing promise if loading is in progress
  if (loadingPromise) {
    return loadingPromise;
  }

  // Start loading Pyodide
  loadingPromise = (async () => {
    try {
      // Import Pyodide dynamically
      const { loadPyodide: load } = await import('pyodide');

      // Load Pyodide with CDN
      const pyodide = await load({
        indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.25.0/full/',
      });

      // Install required packages
      console.log('Installing Python packages...');
      await pyodide.loadPackage(['numpy', 'micropip']);

      // Install Qiskit via micropip (if available in Pyodide)
      const micropip = pyodide.pyimport('micropip');
      try {
        await micropip.install('qiskit');
        console.log('Qiskit installed successfully');
      } catch (e) {
        console.warn('Could not install Qiskit via micropip:', e);
      }

      pyodideInstance = pyodide;
      console.log('Pyodide initialized successfully');
      return pyodide;
    } catch (error) {
      console.error('Failed to load Pyodide:', error);
      loadingPromise = null; // Reset on error
      throw error;
    }
  })();

  return loadingPromise;
}

export function getPyodide() {
  return pyodideInstance;
}
