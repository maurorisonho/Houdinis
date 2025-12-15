# Binder Configuration for Houdinis

This directory contains configuration files for [MyBinder.org](https://mybinder.org/) integration, enabling zero-installation interactive Jupyter notebooks in your browser.

## Files

### `environment.yml`
Conda environment specification with all required dependencies:
- Python 3.11
- Quantum computing libraries (Qiskit, Cirq, PennyLane)
- Cryptography tools
- Network analysis tools
- Jupyter and visualization libraries

### `postBuild`
Post-installation script that runs after the environment is created:
- Installs Houdinis in editable mode
- Pre-caches quantum backends for faster first run
- Enables JupyterLab extensions (ipywidgets)
- Creates welcome message

## Usage

### Launch Binder
Click the badge in the main README.md to launch an interactive environment:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/maurorisonho/Houdinis/main?labpath=notebooks%2Fplayground.ipynb)

### What to Expect
- **Build Time:** 5-10 minutes (first time), ~1 minute (cached)
- **Resources:** 2GB RAM, 1-2 CPU cores, 10GB disk
- **Persistence:** Session data is NOT saved when you close the browser
- **Timeout:** Sessions expire after 10 minutes of inactivity

### Limitations
- No GPU acceleration (WASM/cloud limitations)
- Limited to small quantum circuits (< 15 qubits recommended)
- No access to real quantum hardware (IBM Quantum requires API key)
- Best for learning and demos, not production workloads

## Local Testing

To test the Binder environment locally using `repo2docker`:

```bash
# Install repo2docker
pip install jupyter-repo2docker

# Build and run the environment
repo2docker --editable .

# Or build without running
repo2docker --no-run --image-name houdinis-binder .
```

## Troubleshooting

### Build Fails
- Check `environment.yml` for syntax errors
- Verify all package versions are compatible
- Check MyBinder.org status page

### Slow Startup
- First build takes 5-10 minutes (normal)
- Subsequent launches use cached images (~1 minute)
- Try refreshing if stuck > 15 minutes

### Notebooks Don't Work
- Ensure all cells have compatible dependencies
- Check kernel status (should show "Python 3")
- Restart kernel if needed (Kernel → Restart)

### Resource Limits Exceeded
- Reduce quantum circuit size (< 15 qubits)
- Use fewer shots (< 1024)
- Simplify visualizations

## Configuration Options

### Custom Start Command
Create a `start` file to customize the Jupyter launch command:

```bash
#!/bin/bash
exec jupyter lab --ip=0.0.0.0 --port=8888 --NotebookApp.default_url=/lab/tree/playground.ipynb
```

### System Packages
Create an `apt.txt` file to install system packages:

```
graphviz
libgraphviz-dev
```

### Additional Configuration
See [Binder documentation](https://mybinder.readthedocs.io/en/latest/using/config_files.html) for more options.

## Resources

- [MyBinder.org](https://mybinder.org/)
- [Binder Documentation](https://mybinder.readthedocs.io/)
- [repo2docker](https://repo2docker.readthedocs.io/)
- [Example repositories](https://github.com/binder-examples)

## Support

For issues specific to the Binder environment, please:
1. Check this README for troubleshooting
2. Review [Binder documentation](https://mybinder.readthedocs.io/)
3. Open an issue on our [GitHub repository](https://github.com/maurorisonho/Houdinis/issues)

---

**Note:** MyBinder.org is a free service. Please be respectful of resources and avoid running long computations that could impact other users.
