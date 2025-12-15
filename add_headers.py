#!/usr/bin/env python3
"""
Script to add development headers to Python files
"""

import os
import re
from pathlib import Path

HEADER_TEXT = "Developed by: Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)"

def should_add_header(content: str) -> bool:
    """Check if file needs header added"""
    # Already has the header
    if HEADER_TEXT in content:
        return False
    
    # Has a docstring that can be updated
    if '"""' in content[:500] or "'''" in content[:500]:
        return True
    
    return False

def add_header_to_file(file_path: Path) -> bool:
    """Add development header to a Python file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not should_add_header(content):
            return False
        
        # Find docstring patterns
        patterns = [
            # Pattern 1: """...\nAuthor:...\nLicense:...\n"""
            (r'("""\n)([^"]*Author: Mauro[^\n]*\n)(License: MIT\n)',
             r'\1\2Developed by: Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)\n\3'),
            
            # Pattern 2: """...\nLicense: MIT\n..."""
            (r'("""\n[^"]*)(License: MIT\n)',
             r'\1Developed by: Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)\n\2'),
            
            # Pattern 3: # Author:...\n# License:...
            (r'(# Author: Mauro[^\n]*\n)(# License: MIT)',
             r'\1# Developed by: Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)\n\2'),
        ]
        
        new_content = content
        modified = False
        
        for pattern, replacement in patterns:
            if re.search(pattern, content):
                new_content = re.sub(pattern, replacement, content, count=1)
                if new_content != content:
                    modified = True
                    break
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    
    return False

def main():
    """Process all Python files in the project"""
    base_dir = Path(__file__).parent
    
    # Directories to process
    dirs_to_process = [
        'exploits',
        'quantum',
        'tests',
        'security',
        'auxiliary',
    ]
    
    files_updated = 0
    files_skipped = 0
    
    for dir_name in dirs_to_process:
        dir_path = base_dir / dir_name
        if not dir_path.exists():
            continue
        
        for py_file in dir_path.rglob('*.py'):
            if py_file.name.startswith('__'):
                continue
            
            if add_header_to_file(py_file):
                print(f" Updated: {py_file.relative_to(base_dir)}")
                files_updated += 1
            else:
                files_skipped += 1
    
    print(f"\n Summary:")
    print(f"   Files updated: {files_updated}")
    print(f"   Files skipped: {files_skipped}")

if __name__ == '__main__':
    main()
