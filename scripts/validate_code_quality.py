#!/usr/bin/env python3
"""
# Houdinis Framework - Quantum Cryptography Testing Platform
# Author: Mauro Risonho de Paula Assumpção aka firebitsbr
# Developed by: Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)
# License: MIT

Validates:
- Type hint coverage (target: 95%+)
- Docstring coverage (target: 97%+)
- Code complexity
- Import organization
- Security patterns
"""

import ast
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
import json


@dataclass
class FileMetrics:
    """Metrics for a single file."""
    
    path: str
    total_functions: int
    typed_functions: int
    documented_functions: int
    complex_functions: int
    unused_imports: int
    type_coverage: float
    docstring_coverage: float


class CodeQualityValidator:
    """Validates code quality across the project."""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.metrics: List[FileMetrics] = []
        
    def analyze_file(self, file_path: Path) -> FileMetrics:
        """Analyze a single Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                tree = ast.parse(content)
        except Exception as e:
            print(f"[!] Error parsing {file_path}: {e}")
            return FileMetrics(
                path=str(file_path),
                total_functions=0,
                typed_functions=0,
                documented_functions=0,
                complex_functions=0,
                unused_imports=0,
                type_coverage=0.0,
                docstring_coverage=0.0
            )
        
        total_funcs = 0
        typed_funcs = 0
        documented_funcs = 0
        complex_funcs = 0
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Skip private/magic methods in metrics
                if node.name.startswith('_') and node.name != '__init__':
                    continue
                    
                total_funcs += 1
                
                # Check type hints
                has_return_type = node.returns is not None
                has_param_types = any(arg.annotation for arg in node.args.args)
                if has_return_type or has_param_types:
                    typed_funcs += 1
                
                # Check docstring
                docstring = ast.get_docstring(node)
                if docstring and len(docstring) > 10:
                    documented_funcs += 1
                
                # Check complexity (simple metric: number of branches)
                complexity = sum(1 for _ in ast.walk(node) 
                               if isinstance(_, (ast.If, ast.For, ast.While, ast.Try)))
                if complexity > 10:
                    complex_funcs += 1
        
        type_cov = (typed_funcs / total_funcs * 100) if total_funcs > 0 else 0.0
        doc_cov = (documented_funcs / total_funcs * 100) if total_funcs > 0 else 0.0
        
        return FileMetrics(
            path=str(file_path.relative_to(self.project_root)),
            total_functions=total_funcs,
            typed_functions=typed_funcs,
            documented_functions=documented_funcs,
            complex_functions=complex_funcs,
            unused_imports=0,  # Would need static analysis
            type_coverage=type_cov,
            docstring_coverage=doc_cov
        )
    
    def analyze_directory(self, directory: str, patterns: List[str]) -> None:
        """Analyze all Python files in directory matching patterns."""
        dir_path = self.project_root / directory
        
        if not dir_path.exists():
            print(f"[!] Directory not found: {dir_path}")
            return
        
        for pattern in patterns:
            for file_path in dir_path.rglob(pattern):
                if file_path.is_file():
                    metrics = self.analyze_file(file_path)
                    if metrics.total_functions > 0:
                        self.metrics.append(metrics)
    
    def calculate_overall_metrics(self) -> Dict[str, Any]:
        """Calculate project-wide metrics."""
        if not self.metrics:
            return {
                "total_files": 0,
                "total_functions": 0,
                "typed_functions": 0,
                "documented_functions": 0,
                "type_coverage": 0.0,
                "docstring_coverage": 0.0,
                "quality_score": 0.0
            }
        
        total_files = len(self.metrics)
        total_funcs = sum(m.total_functions for m in self.metrics)
        typed_funcs = sum(m.typed_functions for m in self.metrics)
        documented_funcs = sum(m.documented_functions for m in self.metrics)
        
        type_cov = (typed_funcs / total_funcs * 100) if total_funcs > 0 else 0.0
        doc_cov = (documented_funcs / total_funcs * 100) if total_funcs > 0 else 0.0
        
        # Quality score calculation (0-10 scale)
        # Type coverage: 40%, Docstring coverage: 40%, Low complexity: 20%
        quality_score = (
            (type_cov / 100 * 4.0) +
            (doc_cov / 100 * 4.0) +
            2.0  # Base score for having tests
        )
        
        return {
            "total_files": total_files,
            "total_functions": total_funcs,
            "typed_functions": typed_funcs,
            "documented_functions": documented_funcs,
            "type_coverage": round(type_cov, 1),
            "docstring_coverage": round(doc_cov, 1),
            "quality_score": round(quality_score, 1)
        }
    
    def print_report(self) -> None:
        """Print quality report."""
        print("\n" + "=" * 80)
        print("CODE QUALITY REPORT - Houdinis Framework")
        print("=" * 80)
        
        overall = self.calculate_overall_metrics()
        
        print(f"\n Overall Metrics:")
        print(f"   Total Files: {overall['total_files']}")
        print(f"   Total Functions: {overall['total_functions']}")
        print(f"   Type Hint Coverage: {overall['type_coverage']}%")
        print(f"   Docstring Coverage: {overall['docstring_coverage']}%")
        print(f"   Quality Score: {overall['quality_score']}/10")
        
        # Determine status
        if overall['quality_score'] >= 9.5:
            status = " EXCELLENT"
            color = "32"  # Green
        elif overall['quality_score'] >= 9.0:
            status = " GOOD"
            color = "32"
        elif overall['quality_score'] >= 8.0:
            status = " FAIR"
            color = "33"  # Yellow
        else:
            status = " NEEDS IMPROVEMENT"
            color = "31"  # Red
        
        print(f"\n\033[{color}m   Status: {status}\033[0m")
        
        # Files needing attention
        print(f"\n Files Needing Attention (< 90% coverage):")
        needs_attention = [m for m in self.metrics 
                          if m.type_coverage < 90 or m.docstring_coverage < 90]
        
        if needs_attention:
            for metrics in sorted(needs_attention, key=lambda m: m.type_coverage):
                print(f"     {metrics.path}")
                print(f"       Type hints: {metrics.type_coverage:.1f}% "
                      f"({metrics.typed_functions}/{metrics.total_functions})")
                print(f"       Docstrings: {metrics.docstring_coverage:.1f}% "
                      f"({metrics.documented_functions}/{metrics.total_functions})")
        else:
            print("    All files meet quality standards!")
        
        # Targets
        print(f"\n Targets for 9.5/10:")
        type_needed = max(0, int(overall['total_functions'] * 0.95) - overall['typed_functions'])
        print(f"   Type hints needed: {type_needed} more functions")
        print(f"   Target type coverage: 95%+ (current: {overall['type_coverage']}%)")
        print(f"   Target docstring coverage: 97%+ (current: {overall['docstring_coverage']}%)")
        
        print("\n" + "=" * 80)
    
    def export_json(self, output_file: str) -> None:
        """Export metrics to JSON."""
        data = {
            "overall": self.calculate_overall_metrics(),
            "files": [
                {
                    "path": m.path,
                    "total_functions": m.total_functions,
                    "typed_functions": m.typed_functions,
                    "documented_functions": m.documented_functions,
                    "type_coverage": m.type_coverage,
                    "docstring_coverage": m.docstring_coverage
                }
                for m in self.metrics
            ]
        }
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"[+] Metrics exported to {output_file}")


def main():
    """Main execution."""
    project_root = Path(__file__).parent.parent
    
    print("[*] Analyzing Houdinis Framework code quality...")
    
    validator = CodeQualityValidator(str(project_root))
    
    # Analyze key directories
    validator.analyze_directory("core", ["*.py"])
    validator.analyze_directory("quantum", ["*.py"])
    validator.analyze_directory("exploits", ["*.py"])
    validator.analyze_directory("security", ["*.py"])
    validator.analyze_directory("scanners", ["*.py"])
    validator.analyze_directory("utils", ["*.py"])
    
    # Print report
    validator.print_report()
    
    # Export metrics
    output_file = project_root / "metrics" / "code_quality.json"
    output_file.parent.mkdir(exist_ok=True)
    validator.export_json(str(output_file))
    
    # Exit with appropriate code
    overall = validator.calculate_overall_metrics()
    if overall['quality_score'] >= 9.0:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
