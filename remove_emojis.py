#!/usr/bin/env python3
"""
Remove all emojis from Houdinis project files
Safe operation - only modifies current files, not git history
"""

import os
import re
import sys
from pathlib import Path

# Emoji pattern - matches most Unicode emojis
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002600-\U000026FF"  # Miscellaneous Symbols
    "\U00002700-\U000027BF"  # Dingbats
    "]+",
    flags=re.UNICODE
)

def remove_emojis(text):
    """Remove emojis from text"""
    return EMOJI_PATTERN.sub('', text)

def should_process_file(filepath):
    """Check if file should be processed"""
    # Skip binary files, images, etc
    skip_extensions = {'.pyc', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf', 
                      '.zip', '.tar', '.gz', '.whl', '.egg'}
    skip_dirs = {'__pycache__', '.git', 'node_modules', '.venv', 'venv'}
    
    # Check extension
    if filepath.suffix.lower() in skip_extensions:
        return False
    
    # Check if in skip directory
    for part in filepath.parts:
        if part in skip_dirs:
            return False
    
    return True

def process_file(filepath):
    """Remove emojis from a file"""
    try:
        # Try to read as text
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            original_content = f.read()
        
        # Remove emojis
        new_content = remove_emojis(original_content)
        
        # Only write if changed
        if original_content != new_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            emoji_count = len(original_content) - len(new_content)
            return True, emoji_count
        
        return False, 0
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}", file=sys.stderr)
        return False, 0

def main():
    project_root = Path('/home/test/Downloads/github/portifolio/Houdinis')
    
    if not project_root.exists():
        print(f"Error: Project root not found: {project_root}")
        return 1
    
    print(f"Removing emojis from: {project_root}")
    print("=" * 70)
    
    processed_count = 0
    modified_count = 0
    total_emojis_removed = 0
    
    # Process all files recursively
    for filepath in project_root.rglob('*'):
        if filepath.is_file() and should_process_file(filepath):
            processed_count += 1
            modified, emoji_count = process_file(filepath)
            
            if modified:
                modified_count += 1
                total_emojis_removed += emoji_count
                rel_path = filepath.relative_to(project_root)
                print(f"Modified: {rel_path} ({emoji_count} chars removed)")
    
    print("=" * 70)
    print(f"Summary:")
    print(f"  Files processed: {processed_count}")
    print(f"  Files modified: {modified_count}")
    print(f"  Characters removed: {total_emojis_removed}")
    print(f"\nDone! You can now commit these changes.")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
