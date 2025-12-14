#!/usr/bin/env python3
"""
Script para remover todos os emojis de todos os arquivos do projeto Houdinis.
"""

import os
import re
from pathlib import Path

# Padrão regex expandido para capturar todos os emojis Unicode
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "\U000024C2-\U0001F251"
    "\U00002600-\U000026FF"  # Miscellaneous Symbols
    "\U00002700-\U000027BF"  # Dingbats
    "]+",
    flags=re.UNICODE
)

# Extensões de arquivo para processar
EXTENSIONS = {'.py', '.ipynb', '.md', '.txt', '.sh', '.yml', '.yaml', '.json', '.ini'}

# Diretórios a ignorar
IGNORE_DIRS = {'__pycache__', '.git', 'node_modules', 'venv', 'env', '.venv'}

def should_process_file(file_path):
    """Verifica se o arquivo deve ser processado."""
    # Ignora este script
    if file_path.name in ['remove_all_emojis.py', 'remove_emojis.py']:
        return False
    
    # Verifica extensão
    return file_path.suffix in EXTENSIONS

def remove_emojis_from_text(text):
    """Remove todos os emojis de um texto."""
    return EMOJI_PATTERN.sub('', text)

def process_file(file_path):
    """Processa um arquivo removendo todos os emojis."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Remove emojis
        cleaned_content = remove_emojis_from_text(original_content)
        
        # Se houve mudanças, salva o arquivo
        if original_content != cleaned_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            return True, len(original_content) - len(cleaned_content)
        
        return False, 0
    
    except Exception as e:
        print(f"Erro ao processar {file_path}: {e}")
        return False, 0

def main():
    """Função principal."""
    project_root = Path('/home/test/Downloads/github/portifolio/Houdinis')
    
    print(f"Removendo emojis de todos os arquivos em: {project_root}")
    print(f"Extensões processadas: {', '.join(sorted(EXTENSIONS))}")
    print("-" * 80)
    
    files_processed = 0
    files_modified = 0
    total_chars_removed = 0
    
    # Percorre todos os arquivos do projeto
    for root, dirs, files in os.walk(project_root):
        # Remove diretórios ignorados da busca
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            file_path = Path(root) / file
            
            if should_process_file(file_path):
                files_processed += 1
                modified, chars_removed = process_file(file_path)
                
                if modified:
                    files_modified += 1
                    total_chars_removed += chars_removed
                    print(f" {file_path.relative_to(project_root)} ({chars_removed} caracteres removidos)")
    
    print("-" * 80)
    print(f"\nResumo:")
    print(f"  Arquivos processados: {files_processed}")
    print(f"  Arquivos modificados: {files_modified}")
    print(f"  Total de caracteres removidos: {total_chars_removed}")
    print("\n Remoção de emojis concluída!")

if __name__ == '__main__':
    main()
