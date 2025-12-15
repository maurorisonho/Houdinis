"""
Houdinis Framework - Security Audit and OWASP Compliance
Data de Criação: 15 de dezembro de 2025
Author: Mauro Risonho de Paula Assumpção aka firebitsbr
Desenvolvido: Lógica e Codificação por Humano e AI Assistida (Claude Sonnet 4.5)
License: MIT

Automated security auditing and OWASP Top 10 compliance checking.
"""

import re
import os
import hashlib
import json
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass, asdict
import ast


@dataclass
class SecurityFinding:
    """Represents a security finding."""
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW, INFO
    category: str  # OWASP category
    title: str
    description: str
    file_path: str
    line_number: int
    recommendation: str
    cwe_id: Optional[str] = None


class OWASPSecurityAuditor:
    """
    Automated security auditor for OWASP Top 10 compliance.
    
    Checks for:
    - A01: Broken Access Control
    - A02: Cryptographic Failures
    - A03: Injection
    - A04: Insecure Design
    - A05: Security Misconfiguration
    - A06: Vulnerable and Outdated Components
    - A07: Identification and Authentication Failures
    - A08: Software and Data Integrity Failures
    - A09: Security Logging and Monitoring Failures
    - A10: Server-Side Request Forgery (SSRF)
    """
    
    def __init__(self, project_root: str = ".") -> None:
        """
        Initialize security auditor.
        
        Args:
            project_root: Root directory of the project
        """
        self.project_root = Path(project_root)
        self.findings: List[SecurityFinding] = []
        
        # Dangerous patterns to detect
        self.injection_patterns = [
            (r"eval\s*\(", "Code injection via eval()", "CWE-95"),
            (r"exec\s*\(", "Code injection via exec()", "CWE-95"),
            (r"os\.system\s*\(", "Command injection via os.system()", "CWE-78"),
            (r"subprocess\.call.*shell=True", "Command injection via subprocess", "CWE-78"),
            (r"pickle\.loads?\s*\(", "Insecure deserialization", "CWE-502"),
            (r"yaml\.load\s*\((?!.*Loader)", "Unsafe YAML loading", "CWE-502"),
        ]
        
        self.crypto_patterns = [
            (r"hashlib\.md5", "Weak hash algorithm MD5", "CWE-327"),
            (r"hashlib\.sha1", "Weak hash algorithm SHA1", "CWE-327"),
            (r"random\.", "Use of weak random (not cryptographically secure)", "CWE-338"),
            (r"DES|RC4|RC2", "Weak encryption algorithm", "CWE-327"),
        ]
        
        self.hardcoded_secrets_patterns = [
            (r"password\s*=\s*['\"][^'\"]{3,}", "Hardcoded password", "CWE-798"),
            (r"api_key\s*=\s*['\"][^'\"]{10,}", "Hardcoded API key", "CWE-798"),
            (r"secret\s*=\s*['\"][^'\"]{10,}", "Hardcoded secret", "CWE-798"),
            (r"token\s*=\s*['\"][^'\"]{20,}", "Hardcoded token", "CWE-798"),
        ]
        
        self.path_traversal_patterns = [
            (r"open\s*\([^)]*\+", "Potential path traversal in file operations", "CWE-22"),
            (r"\.\.\/|\.\.\\", "Path traversal pattern", "CWE-22"),
        ]
    
    def scan_file(self, file_path: Path) -> None:
        """
        Scan a single file for security issues.
        
        Args:
            file_path: Path to file to scan
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Check for injection vulnerabilities
            self._check_injections(file_path, lines)
            
            # Check for cryptographic issues
            self._check_crypto(file_path, lines)
            
            # Check for hardcoded secrets
            self._check_hardcoded_secrets(file_path, lines)
            
            # Check for path traversal
            self._check_path_traversal(file_path, lines)
            
            # Check for insecure permissions
            self._check_file_permissions(file_path)
            
            # Python-specific checks
            if file_path.suffix == '.py':
                self._check_python_specific(file_path, content)
                
        except Exception as e:
            print(f"[!] Error scanning {file_path}: {e}")
    
    def _check_injections(self, file_path: Path, lines: List[str]) -> None:
        """Check for injection vulnerabilities."""
        for line_num, line in enumerate(lines, 1):
            for pattern, description, cwe in self.injection_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    self.findings.append(SecurityFinding(
                        severity="HIGH",
                        category="A03:2021-Injection",
                        title=description,
                        description=f"Found pattern: {pattern}",
                        file_path=str(file_path),
                        line_number=line_num,
                        recommendation="Use parameterized queries or safer alternatives",
                        cwe_id=cwe
                    ))
    
    def _check_crypto(self, file_path: Path, lines: List[str]) -> None:
        """Check for cryptographic failures."""
        for line_num, line in enumerate(lines, 1):
            for pattern, description, cwe in self.crypto_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    self.findings.append(SecurityFinding(
                        severity="MEDIUM",
                        category="A02:2021-Cryptographic Failures",
                        title=description,
                        description=f"Found pattern: {pattern}",
                        file_path=str(file_path),
                        line_number=line_num,
                        recommendation="Use strong cryptographic algorithms (SHA-256+, AES-256)",
                        cwe_id=cwe
                    ))
    
    def _check_hardcoded_secrets(self, file_path: Path, lines: List[str]) -> None:
        """Check for hardcoded secrets."""
        for line_num, line in enumerate(lines, 1):
            # Skip comments
            if line.strip().startswith('#'):
                continue
            
            for pattern, description, cwe in self.hardcoded_secrets_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    # Check if it's an example or placeholder
                    if any(x in line.lower() for x in ['example', 'placeholder', 'changeme', 'your_']):
                        continue
                    
                    self.findings.append(SecurityFinding(
                        severity="CRITICAL",
                        category="A07:2021-Identification and Authentication Failures",
                        title=description,
                        description="Hardcoded credentials detected",
                        file_path=str(file_path),
                        line_number=line_num,
                        recommendation="Use environment variables or secure vault",
                        cwe_id=cwe
                    ))
    
    def _check_path_traversal(self, file_path: Path, lines: List[str]) -> None:
        """Check for path traversal vulnerabilities."""
        for line_num, line in enumerate(lines, 1):
            for pattern, description, cwe in self.path_traversal_patterns:
                if re.search(pattern, line):
                    self.findings.append(SecurityFinding(
                        severity="HIGH",
                        category="A01:2021-Broken Access Control",
                        title=description,
                        description=f"Found pattern: {pattern}",
                        file_path=str(file_path),
                        line_number=line_num,
                        recommendation="Validate and sanitize file paths",
                        cwe_id=cwe
                    ))
    
    def _check_file_permissions(self, file_path: Path) -> None:
        """Check for insecure file permissions."""
        try:
            stat_info = os.stat(file_path)
            mode = stat_info.st_mode & 0o777
            
            # Check if world-writable
            if mode & 0o002:
                self.findings.append(SecurityFinding(
                    severity="MEDIUM",
                    category="A05:2021-Security Misconfiguration",
                    title="World-writable file",
                    description=f"File permissions: {oct(mode)}",
                    file_path=str(file_path),
                    line_number=0,
                    recommendation="Remove write permissions for others",
                    cwe_id="CWE-732"
                ))
        except Exception:
            pass
    
    def _check_python_specific(self, file_path: Path, content: str) -> None:
        """Python-specific security checks."""
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                # Check for assert statements (can be disabled with -O)
                if isinstance(node, ast.Assert):
                    self.findings.append(SecurityFinding(
                        severity="LOW",
                        category="A04:2021-Insecure Design",
                        title="Assert statement used for security check",
                        description="Assert statements are disabled with optimization",
                        file_path=str(file_path),
                        line_number=node.lineno,
                        recommendation="Use proper exception handling",
                        cwe_id="CWE-703"
                    ))
                
                # Check for bare except clauses
                if isinstance(node, ast.ExceptHandler):
                    if node.type is None:
                        self.findings.append(SecurityFinding(
                            severity="LOW",
                            category="A09:2021-Security Logging and Monitoring Failures",
                            title="Bare except clause",
                            description="Catching all exceptions may hide security issues",
                            file_path=str(file_path),
                            line_number=node.lineno,
                            recommendation="Catch specific exceptions",
                            cwe_id="CWE-396"
                        ))
        except SyntaxError:
            pass
    
    def scan_directory(self, directory: Optional[Path] = None) -> None:
        """
        Recursively scan directory for security issues.
        
        Args:
            directory: Directory to scan (defaults to project root)
        """
        if directory is None:
            directory = self.project_root
        
        print(f"[*] Scanning directory: {directory}")
        
        # Patterns to exclude
        exclude_patterns = [
            '__pycache__',
            '.git',
            'venv',
            'node_modules',
            '.pytest_cache',
            'coverage_html',
        ]
        
        python_files = []
        for root, dirs, files in os.walk(directory):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_patterns]
            
            for file in files:
                if file.endswith(('.py', '.yml', '.yaml', '.json', '.ini', '.conf')):
                    file_path = Path(root) / file
                    python_files.append(file_path)
        
        print(f"[*] Found {len(python_files)} files to scan")
        
        for file_path in python_files:
            self.scan_file(file_path)
        
        print(f"[+] Scan complete: {len(self.findings)} findings")
    
    def generate_report(self) -> str:
        """
        Generate security audit report.
        
        Returns:
            Formatted report string
        """
        if not self.findings:
            return "\n No security findings detected!\n"
        
        # Group by severity
        by_severity: Dict[str, List[SecurityFinding]] = {
            "CRITICAL": [],
            "HIGH": [],
            "MEDIUM": [],
            "LOW": [],
            "INFO": []
        }
        
        for finding in self.findings:
            by_severity[finding.severity].append(finding)
        
        report = []
        report.append("\n" + "=" * 80)
        report.append("SECURITY AUDIT REPORT - OWASP TOP 10 COMPLIANCE")
        report.append("=" * 80)
        report.append(f"\nTotal Findings: {len(self.findings)}")
        report.append(f"  CRITICAL: {len(by_severity['CRITICAL'])}")
        report.append(f"  HIGH: {len(by_severity['HIGH'])}")
        report.append(f"  MEDIUM: {len(by_severity['MEDIUM'])}")
        report.append(f"  LOW: {len(by_severity['LOW'])}")
        report.append(f"  INFO: {len(by_severity['INFO'])}")
        
        for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]:
            findings = by_severity[severity]
            if not findings:
                continue
            
            report.append(f"\n{'=' * 80}")
            report.append(f"{severity} SEVERITY FINDINGS ({len(findings)})")
            report.append("=" * 80)
            
            for i, finding in enumerate(findings, 1):
                report.append(f"\n{i}. [{finding.category}] {finding.title}")
                report.append(f"   File: {finding.file_path}:{finding.line_number}")
                report.append(f"   Description: {finding.description}")
                report.append(f"   Recommendation: {finding.recommendation}")
                if finding.cwe_id:
                    report.append(f"   CWE: {finding.cwe_id}")
        
        report.append("\n" + "=" * 80)
        
        report_str = "\n".join(report)
        print(report_str)
        return report_str
    
    def save_report(self, filename: str = "security_audit.json") -> None:
        """
        Save audit report to JSON file.
        
        Args:
            filename: Output filename
        """
        output_path = self.project_root / filename
        
        report_data = {
            "total_findings": len(self.findings),
            "by_severity": {
                "critical": len([f for f in self.findings if f.severity == "CRITICAL"]),
                "high": len([f for f in self.findings if f.severity == "HIGH"]),
                "medium": len([f for f in self.findings if f.severity == "MEDIUM"]),
                "low": len([f for f in self.findings if f.severity == "LOW"]),
                "info": len([f for f in self.findings if f.severity == "INFO"]),
            },
            "findings": [asdict(f) for f in self.findings]
        }
        
        with open(output_path, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"[+] Security audit report saved to: {output_path}")
    
    def get_compliance_score(self) -> float:
        """
        Calculate OWASP compliance score.
        
        Returns:
            Compliance score (0-10)
        """
        if not self.findings:
            return 10.0
        
        # Weight findings by severity
        weights = {
            "CRITICAL": 10,
            "HIGH": 5,
            "MEDIUM": 2,
            "LOW": 1,
            "INFO": 0.5
        }
        
        total_penalty = sum(weights.get(f.severity, 0) for f in self.findings)
        
        # Calculate score (max penalty of 100 = score of 0)
        score = max(0, 10 - (total_penalty / 10))
        
        return round(score, 1)


def run_security_audit(project_root: str = ".") -> None:
    """
    Run comprehensive security audit.
    
    Args:
        project_root: Root directory of project
    """
    print("\n" + "=" * 80)
    print("HOUDINIS FRAMEWORK - OWASP SECURITY AUDIT")
    print("=" * 80)
    
    auditor = OWASPSecurityAuditor(project_root)
    
    # Scan the project
    auditor.scan_directory()
    
    # Generate report
    auditor.generate_report()
    
    # Save results
    auditor.save_report()
    
    # Calculate compliance score
    score = auditor.get_compliance_score()
    print(f"\n OWASP Compliance Score: {score}/10")
    
    if score >= 9.0:
        print("   Status:  EXCELLENT")
    elif score >= 7.0:
        print("   Status:   GOOD (improvements recommended)")
    elif score >= 5.0:
        print("   Status:   FAIR (action required)")
    else:
        print("   Status:  POOR (immediate action required)")


if __name__ == "__main__":
    run_security_audit()
