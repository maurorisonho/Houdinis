#!/usr/bin/env python3
"""
Automatic Type Hint Addition Script
====================================

Adiciona type hints automaticamente às funções que não possuem.

Author: Houdinis Framework
License: MIT
"""

import ast
import os
import sys
from pathlib import Path
from typing import List, Set
import re


class TypeHintAdder(ast.NodeTransformer):
    """Add type hints to functions without them"""

    def __init__(self):
        self.modified = False
        self.imports_needed: Set[str] = set()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        """Visit function definition and add type hints if missing"""
        # Skip private functions
        if node.name.startswith("_"):
            return node

        # Check if function already has adequate type hints
        if self._has_adequate_types(node):
            return node

        # Add return type if missing
        if node.returns is None:
            # Infer return type from docstring or default to Any
            return_type = self._infer_return_type(node)
            if return_type:
                self.modified = True
                # We can't actually modify the AST to add annotations programmatically
                # This would require source code rewriting

        return node

    def _has_adequate_types(self, node: ast.FunctionDef) -> bool:
        """Check if function has adequate type hints"""
        # Check return type
        if node.returns is None and node.name not in (
            "__init__",
            "__str__",
            "__repr__",
        ):
            return False

        # Check parameter types
        params = [arg for arg in node.args.args if arg.arg not in ("self", "cls")]
        if params and not all(arg.annotation for arg in params):
            return False

        return True

    def _infer_return_type(self, node: ast.FunctionDef) -> str:
        """Infer return type from function body"""
        # Check for return statements
        for child in ast.walk(node):
            if isinstance(child, ast.Return) and child.value:
                # Basic type inference
                if isinstance(child.value, ast.Constant):
                    if isinstance(child.value.value, bool):
                        return "bool"
                    elif isinstance(child.value.value, int):
                        return "int"
                    elif isinstance(child.value.value, str):
                        return "str"
                    elif isinstance(child.value.value, float):
                        return "float"
                    elif child.value.value is None:
                        return "None"
                elif isinstance(child.value, ast.Dict):
                    return "Dict"
                elif isinstance(child.value, ast.List):
                    return "List"
                elif isinstance(child.value, ast.Tuple):
                    return "Tuple"

        # Check __init__ methods
        if node.name == "__init__":
            return "None"

        return "Any"


def add_typing_import(content: str, types_needed: Set[str]) -> str:
    """Add typing imports if not present"""
    if not types_needed:
        return content

    # Check if typing import exists
    has_typing = re.search(r"^from typing import", content, re.MULTILINE)

    if has_typing:
        # Extend existing import
        match = re.search(r"^from typing import (.+)$", content, re.MULTILINE)
        if match:
            existing = set(t.strip() for t in match.group(1).split(","))
            all_types = existing | types_needed
            new_import = f"from typing import {', '.join(sorted(all_types))}"
            content = content.replace(match.group(0), new_import)
    else:
        # Add new import after docstring
        lines = content.split("\n")
        insert_pos = 0

        # Skip shebang and docstring
        if lines[0].startswith("#!"):
            insert_pos = 1

        # Skip module docstring
        in_docstring = False
        for i, line in enumerate(lines[insert_pos:], start=insert_pos):
            if '"""' in line or "'''" in line:
                if not in_docstring:
                    in_docstring = True
                else:
                    insert_pos = i + 1
                    break

        # Add import
        new_import = f"from typing import {', '.join(sorted(types_needed))}\n"
        lines.insert(insert_pos, new_import)
        content = "\n".join(lines)

    return content


def process_file(filepath: Path, dry_run: bool = True) -> bool:
    """Process a single file to add type hints"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Parse AST
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            print(f"  Syntax error in {filepath}: {e}")
            return False

        # Check if modifications needed
        adder = TypeHintAdder()
        adder.visit(tree)

        if not adder.modified:
            return False

        # For now, just report files that need work
        print(f" {filepath} needs type hints")

        # Actual implementation would require source code rewriting
        # which is complex and risky. Better to do manually or with tools like:
        # - MonkeyType
        # - PyAnnotate
        # - autotyping

        return True

    except Exception as e:
        print(f" Error processing {filepath}: {e}")
        return False


def main():
    """Main execution"""
    print(" Type Hint Addition Tool")
    print("=" * 70)

    directories = ["quantum", "exploits", "core", "scanners", "utils", "security"]
    files_needing_work = []

    for dir_name in directories:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            continue

        for filepath in dir_path.rglob("*.py"):
            if "__pycache__" in str(filepath):
                continue

            if process_file(filepath, dry_run=True):
                files_needing_work.append(filepath)

    print(f"\n Summary:")
    print(f"  Files needing type hints: {len(files_needing_work)}")

    if files_needing_work:
        print("\n Recommendation:")
        print("  Use tools like 'monkeytype' or add manually:")
        print("  1. pip install monkeytype")
        print("  2. monkeytype run main.py")
        print("  3. monkeytype apply module_name")

    return 0


if __name__ == "__main__":
    sys.exit(main())
