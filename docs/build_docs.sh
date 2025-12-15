#!/bin/bash
# Build Sphinx documentation

set -e

echo "[+] Building Houdinis Documentation"

# Change to docs directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "../venv" ]; then
    echo "[!] Virtual environment not found. Creating..."
    python3 -m venv ../venv
fi

# Activate virtual environment
source ../venv/bin/activate

# Install documentation requirements
echo "[*] Installing documentation dependencies..."
pip install -r requirements.txt

# Clean previous build
echo "[*] Cleaning previous build..."
rm -rf _build/

# Build HTML documentation
echo "[*] Building HTML documentation..."
sphinx-build -b html . _build/html

echo "[+] Documentation built successfully!"
echo "[*] Open _build/html/index.html in your browser"
echo "[*] Or run: python -m http.server --directory _build/html 8000"
