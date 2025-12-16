#!/usr/bin/env python3
"""Script to add standardized headers to all Python files in Houdinis project"""

import os
import re
from pathlib import Path

HEADER_STANDARD = '''#!/usr/bin/env python3
"""
# Houdinis Framework - Quantum Cryptography Testing Platform
# Author: Mauro Risonho de Paula Assumpção aka firebitsbr
# Developed by: Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)
# License: MIT
'''

def has_standard_header(content):
    """Check if file already has standard header"""
    return "# Houdinis Framework - Quantum Cryptography Testing Platform" in content[:500]

def extract_description(content):
    """Extract additional description from docstring"""
    # Skip shebang and initial docstring
    lines = content.split('\n')
    in_docstring = False
    description_lines = []
    
    for i, line in enumerate(lines):
        if i == 0 and line.startswith('#!'):
            continue
        if line.strip().startswith('"""'):
            if not in_docstring:
                in_docstring = True
                continue
            else:
                break
        if in_docstring:
            # Skip old header lines
            if any(skip in line for skip in ['Author:', 'Developed by:', 'License:', 'Houdinis Framework']):
                continue
            if line.strip():
                description_lines.append(line)
    
    return '\n'.join(description_lines).strip()

def process_file(filepath):
    """Process a single Python file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip empty or very small files
        if len(content) < 50:
            return "SKIPPED (too small)"
        
        # Skip __init__.py
        if filepath.name == '__init__.py':
            return "SKIPPED (__init__.py)"
        
        # Already has standard header
        if has_standard_header(content):
            return "ALREADY HAS"
        
        # Extract existing description
        description = extract_description(content)
        
        # Remove old shebang and docstring
        lines = content.split('\n')
        code_start = 0
        
        # Skip shebang
        if lines and lines[0].startswith('#!'):
            code_start = 1
        
        # Skip docstring
        if code_start < len(lines) and lines[code_start].strip().startswith('"""'):
            code_start += 1
            while code_start < len(lines):
                if '"""' in lines[code_start]:
                    code_start += 1
                    break
                code_start += 1
        
        # Skip empty lines
        while code_start < len(lines) and not lines[code_start].strip():
            code_start += 1
        
        # Build new content
        new_content = HEADER_STANDARD
        if description:
            new_content += '\n' + description + '\n'
        new_content += '"""\n\n'
        new_content += '\n'.join(lines[code_start:])
        
        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return "UPDATED"
    
    except Exception as e:
        return f"ERROR: {e}"

def main():
    """Process all Python files"""
    project_root = Path(__file__).parent
    
    # Priority directories
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
        'tests'
    ]
    
    # Individual files
    individual_files = [
        'setup.py',
        'main.py'
    ]
    
    results = {}
    
    # Process directories
    for dir_name in dirs:
        dir_path = project_root / dir_name
        if not dir_path.exists():
            continue
        
        for py_file in dir_path.rglob('*.py'):
            status = process_file(py_file)
            rel_path = py_file.relative_to(project_root)
            results[str(rel_path)] = status
    
    # Process individual files
    for filename in individual_files:
        filepath = project_root / filename
        if filepath.exists():
            status = process_file(filepath)
            results[filename] = status
    
    # Display results
    print("\n" + "="*80)
    print("HEADER UPDATE SUMMARY")
    print("="*80 + "\n")
    
    updated = sum(1 for s in results.values() if s == "UPDATED")
    already = sum(1 for s in results.values() if s == "ALREADY HAS")
    ignored = sum(1 for s in results.values() if s.startswith("SKIPPED"))
    errors = sum(1 for s in results.values() if s.startswith("ERROR"))
    
    print(f" Updated: {updated}")
    print(f"  Already had: {already}")
    print(f"⊘  Skipped: {ignored}")
    print(f" Errors: {errors}")
    print(f"\nTotal processed: {len(results)} files\n")
    
    # List updated
    if updated > 0:
        print(" Updated files:")
        for file, status in sorted(results.items()):
            if status == "UPDATED":
                print(f"  • {file}")
    
    print("\n" + "="*80 + "\n")

if __name__ == '__main__':
    main()
