#!/usr/bin/env python3
"""
Script to translate development headers from Portuguese to English
"""

import os
import re
from pathlib import Path

# Translation mapping
TRANSLATIONS = {
    "Developed by: Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)": 
        "Developed by: Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)",
}

def translate_file(file_path: Path) -> bool:
    """Translate headers in a file from Portuguese to English"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file needs translation
        if "Desenvolvido:" not in content:
            return False
        
        new_content = content
        modified = False
        
        for pt_text, en_text in TRANSLATIONS.items():
            if pt_text in new_content:
                new_content = new_content.replace(pt_text, en_text)
                modified = True
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    
    return False

def main():
    """Process all files in the project"""
    base_dir = Path(__file__).parent
    
    # File patterns to process
    patterns = ['**/*.py', '**/*.ts', '**/*.tsx', '**/*.js', '**/*.jsx']
    
    # Directories to exclude
    exclude_dirs = {
        'node_modules', '.next', '__pycache__', '.git', 
        'venv', 'env', 'build', 'dist', '.venv'
    }
    
    files_updated = 0
    files_skipped = 0
    
    for pattern in patterns:
        for file_path in base_dir.rglob(pattern):
            # Skip excluded directories
            if any(excluded in file_path.parts for excluded in exclude_dirs):
                continue
            
            # Skip __init__.py and similar
            if file_path.name.startswith('__'):
                continue
            
            if translate_file(file_path):
                print(f" Translated: {file_path.relative_to(base_dir)}")
                files_updated += 1
            else:
                files_skipped += 1
    
    print(f"\n Translation Summary:")
    print(f"   Files translated: {files_updated}")
    print(f"   Files skipped: {files_skipped}")
    print(f"\n Translation complete!")

if __name__ == '__main__':
    main()
