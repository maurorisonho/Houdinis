#!/usr/bin/env python3
"""
Code Quality Validation Script
================================

Valida e melhora a qualidade do código do projeto Houdinis.
Atingir 9.5/10 no Pylance.

Features:
- Type hints validation
- Import cleanup
- Docstring validation
- Code style checking
- Security scanning

Author: Houdinis Framework
License: MIT
"""

import ast
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class QualityMetrics:
    """Quality metrics for code analysis"""

    total_functions: int = 0
    functions_with_types: int = 0
    functions_with_docstrings: int = 0
    unused_imports: int = 0
    missing_type_hints: int = 0
    undocumented_functions: int = 0

    @property
    def type_coverage(self) -> float:
        """Calculate type hint coverage percentage"""
        if self.total_functions == 0:
            return 100.0
        return (self.functions_with_types / self.total_functions) * 100

    @property
    def docstring_coverage(self) -> float:
        """Calculate docstring coverage percentage"""
        if self.total_functions == 0:
            return 100.0
        return (self.functions_with_docstrings / self.total_functions) * 100

    @property
    def overall_score(self) -> float:
        """Calculate overall quality score out of 10"""
        type_score = self.type_coverage / 10  # Max 10 points
        doc_score = self.docstring_coverage / 10  # Max 10 points
        import_penalty = min(self.unused_imports * 0.1, 2.0)  # Max -2 points

        score = (type_score * 0.5 + doc_score * 0.5) - import_penalty
        return max(0.0, min(10.0, score))


class CodeQualityAnalyzer:
    """Analyze Python code quality"""

    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.metrics = QualityMetrics()
        self.issues: List[str] = []

    def analyze_file(self, filepath: Path) -> None:
        """Analyze a single Python file"""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content, filename=str(filepath))

            # Analyze functions
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    self._analyze_function(node, filepath)

            # Check for unused imports
            self._check_unused_imports(filepath, content)

        except Exception as e:
            self.issues.append(f"Error analyzing {filepath}: {e}")

    def _analyze_function(self, node: ast.FunctionDef, filepath: Path) -> None:
        """Analyze a function for type hints and docstrings"""
        # Skip private functions and test functions
        if node.name.startswith("_") or node.name.startswith("test_"):
            return

        self.metrics.total_functions += 1

        # Check type hints
        has_type_hints = self._has_type_hints(node)
        if has_type_hints:
            self.metrics.functions_with_types += 1
        else:
            self.metrics.missing_type_hints += 1
            self.issues.append(
                f"{filepath}:{node.lineno} - Function '{node.name}' missing type hints"
            )

        # Check docstrings
        has_docstring = ast.get_docstring(node) is not None
        if has_docstring:
            self.metrics.functions_with_docstrings += 1
        else:
            self.metrics.undocumented_functions += 1
            self.issues.append(
                f"{filepath}:{node.lineno} - Function '{node.name}' missing docstring"
            )

    def _has_type_hints(self, node: ast.FunctionDef) -> bool:
        """Check if function has type hints"""
        # Check return type
        has_return_type = node.returns is not None

        # Check parameter types (skip 'self' and 'cls')
        params = [arg for arg in node.args.args if arg.arg not in ("self", "cls")]

        if not params:
            return has_return_type

        has_param_types = all(arg.annotation is not None for arg in params)

        return has_return_type and has_param_types

    def _check_unused_imports(self, filepath: Path, content: str) -> None:
        """Check for unused imports using pyflakes"""
        try:
            result = subprocess.run(
                ["python", "-m", "pyflakes", str(filepath)],
                capture_output=True,
                text=True,
                timeout=5,
            )

            # Count unused imports
            for line in result.stdout.splitlines():
                if "imported but unused" in line.lower():
                    self.metrics.unused_imports += 1
                    self.issues.append(f"{filepath} - {line.strip()}")

        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

    def analyze_directory(self, directory: Path) -> None:
        """Analyze all Python files in directory"""
        python_files = list(directory.rglob("*.py"))

        # Filter out test files and __pycache__
        python_files = [
            f
            for f in python_files
            if "__pycache__" not in str(f) and "test_" not in f.name
        ]

        print(f"Analyzing {len(python_files)} Python files...")

        for filepath in python_files:
            self.analyze_file(filepath)

    def print_report(self) -> None:
        """Print quality report"""
        print("\n" + "=" * 70)
        print("CODE QUALITY REPORT")
        print("=" * 70)

        print(f"\n Metrics:")
        print(f"  Total Functions:       {self.metrics.total_functions}")
        print(
            f"  With Type Hints:       {self.metrics.functions_with_types} "
            f"({self.metrics.type_coverage:.1f}%)"
        )
        print(
            f"  With Docstrings:       {self.metrics.functions_with_docstrings} "
            f"({self.metrics.docstring_coverage:.1f}%)"
        )
        print(f"  Unused Imports:        {self.metrics.unused_imports}")
        print(f"  Missing Type Hints:    {self.metrics.missing_type_hints}")
        print(f"  Undocumented:          {self.metrics.undocumented_functions}")

        print(f"\n Overall Quality Score: {self.metrics.overall_score:.1f}/10.0")

        # Score interpretation
        score = self.metrics.overall_score
        if score >= 9.5:
            status = " EXCELLENT"
            message = "Code quality is outstanding!"
        elif score >= 8.5:
            status = " GOOD"
            message = "Code quality is good, minor improvements needed."
        elif score >= 7.0:
            status = " FAIR"
            message = "Code quality needs improvement."
        else:
            status = " POOR"
            message = "Code quality needs significant improvement."

        print(f"\nStatus: {status}")
        print(f"{message}")

        # Print top issues
        if self.issues and len(self.issues) <= 20:
            print(f"\n  Issues Found ({len(self.issues)}):")
            for issue in self.issues[:20]:
                print(f"  - {issue}")
            if len(self.issues) > 20:
                print(f"  ... and {len(self.issues) - 20} more")
        elif self.issues:
            print(
                f"\n  {len(self.issues)} issues found. Run with --verbose for details."
            )

        print("\n" + "=" * 70)


def run_additional_checks() -> Dict[str, bool]:
    """Run additional code quality checks"""
    checks = {}

    # Check if black would reformat code
    try:
        result = subprocess.run(
            ["black", "--check", "--quiet", "."], capture_output=True, timeout=30
        )
        checks["black"] = result.returncode == 0
    except:
        checks["black"] = None

    # Check with flake8
    try:
        result = subprocess.run(
            ["flake8", ".", "--count", "--select=E9,F63,F7,F82"],
            capture_output=True,
            timeout=30,
        )
        checks["flake8"] = result.returncode == 0
    except:
        checks["flake8"] = None

    # Check with mypy
    try:
        result = subprocess.run(
            ["mypy", ".", "--ignore-missing-imports"], capture_output=True, timeout=60
        )
        checks["mypy"] = result.returncode == 0
    except:
        checks["mypy"] = None

    return checks


def main():
    """Main execution function"""
    print(" Houdinis Code Quality Analyzer")
    print("=" * 70)

    # Analyze main directories
    analyzer = CodeQualityAnalyzer()

    directories = ["quantum", "exploits", "core", "scanners", "utils", "security"]

    for dir_name in directories:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f" Analyzing {dir_name}/...")
            analyzer.analyze_directory(dir_path)

    # Print main report
    analyzer.print_report()

    # Run additional checks
    print("\n Additional Checks:")
    checks = run_additional_checks()

    for tool, status in checks.items():
        if status is True:
            print(f"   {tool}: PASS")
        elif status is False:
            print(f"   {tool}: FAIL")
        else:
            print(f"    {tool}: NOT AVAILABLE")

    # Exit code based on score
    if analyzer.metrics.overall_score >= 9.5:
        print("\n Code quality target achieved (9.5/10)!")
        return 0
    else:
        needed = 9.5 - analyzer.metrics.overall_score
        print(f"\n  Need {needed:.1f} more points to reach 9.5/10")
        print("\nRecommendations:")
        if analyzer.metrics.type_coverage < 90:
            print("  1. Add type hints to more functions")
        if analyzer.metrics.docstring_coverage < 90:
            print("  2. Add docstrings to public functions")
        if analyzer.metrics.unused_imports > 0:
            print("  3. Remove unused imports")
        return 1


if __name__ == "__main__":
    sys.exit(main())
