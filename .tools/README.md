# Development Tools

This directory contains utility scripts and tools used during development and maintenance of the Houdinis project.

##  Contents

### Header Management
- **`add_headers.py`** - Automated script to add development attribution headers to source files
- **`translate_headers.py`** - Script to translate headers from Portuguese to English

### Code Cleanup
- **`remove_emojis.py`** - Remove emojis from specific files
- **`remove_all_emojis.py`** - Remove all emojis from the entire codebase

### Git Utilities
- **`rewrite_git_history.py`** - Python script for git history rewriting operations

### Testing
- **`test_gpu_cuquantum.py`** - GPU and cuQuantum integration testing script

##  Usage

These tools are for development and maintenance purposes only. They are not part of the main application runtime.

### Example Usage

```bash
# Add headers to new files
python .tools/add_headers.py

# Translate headers to English
python .tools/translate_headers.py

# Test GPU acceleration
python .tools/test_gpu_cuquantum.py
```

##  Note

These scripts should be run from the project root directory to ensure correct paths.

---

**Developed by:** Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)
