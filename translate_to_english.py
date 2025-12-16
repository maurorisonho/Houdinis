#!/usr/bin/env python3
"""
# Houdinis Framework - Quantum Cryptography Testing Platform
# Author: Mauro Risonho de Paula Assumpção aka firebitsbr
# Developed by: Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)
# License: MIT

Script to translate Portuguese comments and strings to English in Python files
"""

import os
import re
from pathlib import Path
from typing import List, Tuple

# Translation dictionary for common Portuguese terms
TRANSLATIONS = {
    # Comment patterns to translate
    r'# Configuração': '# Configuration',
    r'# Configurações': '# Settings',
    r'# Inicialização': '# Initialization',
    r'# Inicializar': '# Initialize',
    r'# Execução': '# Execution',
    r'# Executar': '# Execute',
    r'# Validação': '# Validation',
    r'# Validar': '# Validate',
    r'# Verificação': '# Verification',
    r'# Verificar': '# Verify',
    r'# Processamento': '# Processing',
    r'# Processar': '# Process',
    r'# Atualização': '# Update',
    r'# Atualizar': '# Update',
    r'# Criação': '# Creation',
    r'# Criar': '# Create',
    r'# Remoção': '# Removal',
    r'# Remover': '# Remove',
    r'# Instalação': '# Installation',
    r'# Instalar': '# Install',
    r'# Carregamento': '# Loading',
    r'# Carregar': '# Load',
    r'# Salvamento': '# Saving',
    r'# Salvar': '# Save',
    r'# Análise': '# Analysis',
    r'# Analisar': '# Analyze',
    r'# Resultado': '# Result',
    r'# Resultados': '# Results',
    r'# Erro': '# Error',
    r'# Erros': '# Errors',
    r'# Sucesso': '# Success',
    r'# Aviso': '# Warning',
    r'# Informação': '# Information',
    r'# Depuração': '# Debug',
    
    # Docstring patterns
    r'"""Configuração': '"""Configuration',
    r'"""Configurações': '"""Settings',
    r'"""Inicialização': '"""Initialization',
    r'"""Execução': '"""Execution',
    r'"""Validação': '"""Validation',
    r'"""Verificação': '"""Verification',
    r'"""Processamento': '"""Processing',
    r'"""Análise': '"""Analysis',
    
    # Common phrases to translate
    r'arquivo não encontrado': 'file not found',
    r'operação bem-sucedida': 'operation successful',
    r'erro ao processar': 'error processing',
    r'dados inválidos': 'invalid data',
    r'parâmetro obrigatório': 'required parameter',
    r'parâmetros inválidos': 'invalid parameters',
    r'caminho inválido': 'invalid path',
    r'formato inválido': 'invalid format',
}

def find_portuguese_patterns(content: str) -> List[Tuple[str, int]]:
    """Find Portuguese words and phrases in content"""
    portuguese_indicators = [
        # Common Portuguese nouns
        r'\b(?:configuração|configurações|inicialização|execução|validação|verificação)\b',
        r'\b(?:processamento|análise|resultado|resultados|erro|erros|sucesso)\b',
        r'\b(?:arquivo|diretório|caminho|dados|parâmetro|parâmetros)\b',
        r'\b(?:criar|remover|atualizar|instalar|carregar|salvar|processar)\b',
        r'\b(?:válido|inválido|obrigatório|opcional)\b',
        
        # Common Portuguese phrases
        r'não encontrado',
        r'bem-sucedida',
        r'ao processar',
    
    
    matches = []
    for i, line in enumerate(content.split('\n'), 1):
        for pattern in portuguese_indicators:
            if re.search(pattern, line, re.IGNORECASE):
                matches.append((line.strip(), i))
                break
    
    return matches

def translate_content(content: str) -> Tuple[str, int]:
    """Translate Portuguese content to English"""
    modified = content
    changes = 0
    
    for pt_pattern, en_text in TRANSLATIONS.items():
        new_content = re.sub(pt_pattern, en_text, modified, flags=re.IGNORECASE)
        if new_content != modified:
            changes += 1
            modified = new_content
    
    return modified, changes

def process_file(filepath: Path) -> Tuple[str, int, List[str]]:
    """Process a single Python file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original = f.read()
        
        # Skip very small files
        if len(original) < 50:
            return "SKIPPED", 0, []
        
        # Detect Portuguese patterns
        pt_matches = find_portuguese_patterns(original)
        
        if not pt_matches:
            return "NO_PT", 0, []
        
        # Apply translations
        translated, changes = translate_content(original)
        
        if changes == 0:
            return "NO_CHANGES", 0, [line for line, _ in pt_matches]
        
        # Save translated content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(translated)
        
        return "TRANSLATED", changes, [line for line, _ in pt_matches]
    
    except Exception as e:
        return f"ERROR: {e}", 0, []

def main():
    """Main translation process"""
    project_root = Path(__file__).parent
    
    # Priority directories to scan
    dirs = [
        'core',
        'exploits',
        'quantum',
        'security',
        'scanners',
        'utils',
        'payloads',
        'langchain_agents',
        'mcp_servers',
        'webui',
        'scripts',
        'tests',
        'auxiliary'
    ]
    
    results = {}
    total_changes = 0
    files_with_pt = []
    
    print("\n" + "="*80)
    print("TRANSLATION SCAN: Portuguese to English")
    print("="*80 + "\n")
    
    # Scan all Python files
    for dir_name in dirs:
        dir_path = project_root / dir_name
        if not dir_path.exists():
            continue
        
        for py_file in dir_path.rglob('*.py'):
            status, changes, pt_lines = process_file(py_file)
            rel_path = str(py_file.relative_to(project_root))
            
            if status == "TRANSLATED":
                results[rel_path] = (status, changes)
                total_changes += changes
                print(f" {rel_path}: {changes} translations")
            elif status == "NO_CHANGES" and pt_lines:
                files_with_pt.append((rel_path, pt_lines))
                print(f" {rel_path}: Portuguese found but not auto-translated")
    
    # Display summary
    print("\n" + "="*80)
    print("TRANSLATION SUMMARY")
    print("="*80 + "\n")
    
    translated_files = len([r for r in results.values() if r[0] == "TRANSLATED"])
    
    print(f" Files translated: {translated_files}")
    print(f" Total changes: {total_changes}")
    print(f"  Files needing manual review: {len(files_with_pt)}")
    
    if files_with_pt:
        print("\n" + "-"*80)
        print("Files with Portuguese requiring manual translation:")
        print("-"*80)
        for filepath, lines in files_with_pt[:10]:  # Display first 10
            print(f"\n {filepath}")
            for line in lines[:3]:  # Display first 3 lines
                print(f"   {line}")
    
    print("\n" + "="*80 + "\n")

if __name__ == '__main__':
    main()
