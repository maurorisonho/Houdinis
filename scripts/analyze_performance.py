#!/usr/bin/env python3
"""
# Houdinis Framework - Quantum Cryptography Testing Platform
# Author: Mauro Risonho de Paula Assumpção aka firebitsbr
# Developed by: Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)
# License: MIT

Performance Analysis Script
Analyzes performance benchmark results and detects regressions.
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class BenchmarkResult:
    """Individual benchmark result."""
    name: str
    mean: float
    stddev: float
    min: float
    max: float
    rounds: int


@dataclass
class ComparisonResult:
    """Comparison between current and baseline."""
    name: str
    current_mean: float
    baseline_mean: float
    change_percent: float
    is_regression: bool
    is_improvement: bool
    threshold_exceeded: bool


@dataclass
class AnalysisReport:
    """Complete analysis report."""
    has_regression: bool
    regression_count: int
    improvement_count: int
    total_tests: int
    comparisons: List[ComparisonResult]
    summary: Dict[str, Any]


class PerformanceAnalyzer:
    """Analyzes performance benchmark results."""

    def __init__(self, threshold_percent: float = 10.0):
        """
        Initialize analyzer.

        Args:
            threshold_percent: Percentage threshold for regression detection
        """
        self.threshold_percent = threshold_percent

    def load_benchmark_results(self, file_path: Path) -> Dict[str, BenchmarkResult]:
        """
        Load benchmark results from JSON file.

        Args:
            file_path: Path to benchmark results JSON

        Returns:
            Dictionary of benchmark results
        """
        if not file_path.exists():
            print(f"  Benchmark file not found: {file_path}")
            return {}

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            results = {}
            for benchmark in data.get('benchmarks', []):
                name = benchmark['name']
                stats = benchmark['stats']

                results[name] = BenchmarkResult(
                    name=name,
                    mean=stats['mean'],
                    stddev=stats['stddev'],
                    min=stats['min'],
                    max=stats['max'],
                    rounds=stats['rounds']
                )

            return results

        except Exception as e:
            print(f" Error loading benchmark results: {e}")
            return {}

    def compare_results(
        self,
        current: Dict[str, BenchmarkResult],
        baseline: Dict[str, BenchmarkResult]
    ) -> List[ComparisonResult]:
        """
        Compare current results with baseline.

        Args:
            current: Current benchmark results
            baseline: Baseline benchmark results

        Returns:
            List of comparison results
        """
        comparisons = []

        for name, current_result in current.items():
            if name not in baseline:
                print(f"ℹ  New benchmark (no baseline): {name}")
                continue

            baseline_result = baseline[name]

            # Calculate percentage change
            change = ((current_result.mean - baseline_result.mean) / baseline_result.mean) * 100

            # Determine if regression or improvement
            is_regression = change > self.threshold_percent
            is_improvement = change < -self.threshold_percent
            threshold_exceeded = abs(change) > self.threshold_percent

            comparison = ComparisonResult(
                name=name,
                current_mean=current_result.mean,
                baseline_mean=baseline_result.mean,
                change_percent=change,
                is_regression=is_regression,
                is_improvement=is_improvement,
                threshold_exceeded=threshold_exceeded
            )

            comparisons.append(comparison)

        return comparisons

    def generate_analysis(
        self,
        current_path: Path,
        baseline_path: Optional[Path] = None
    ) -> AnalysisReport:
        """
        Generate complete analysis report.

        Args:
            current_path: Path to current benchmark results
            baseline_path: Path to baseline benchmark results (optional)

        Returns:
            Analysis report
        """
        print(" Loading benchmark results...")
        current_results = self.load_benchmark_results(current_path)

        if not current_results:
            print(" No current results found")
            return AnalysisReport(
                has_regression=False,
                regression_count=0,
                improvement_count=0,
                total_tests=0,
                comparisons=[],
                summary={'error': 'No current results'}
            )

        # Load baseline if provided
        comparisons = []
        if baseline_path and baseline_path.exists():
            print(" Loading baseline results...")
            baseline_results = self.load_benchmark_results(baseline_path)

            if baseline_results:
                print(" Comparing with baseline...")
                comparisons = self.compare_results(current_results, baseline_results)
        else:
            print("ℹ  No baseline found, skipping comparison")

        # Generate summary
        regression_count = sum(1 for c in comparisons if c.is_regression)
        improvement_count = sum(1 for c in comparisons if c.is_improvement)
        has_regression = regression_count > 0

        # Calculate statistics
        if comparisons:
            avg_change = sum(c.change_percent for c in comparisons) / len(comparisons)
            max_regression = max((c.change_percent for c in comparisons if c.is_regression), default=0)
            max_improvement = min((c.change_percent for c in comparisons if c.is_improvement), default=0)
        else:
            avg_change = 0
            max_regression = 0
            max_improvement = 0

        summary = {
            'threshold_percent': self.threshold_percent,
            'total_current': len(current_results),
            'total_compared': len(comparisons),
            'avg_change_percent': round(avg_change, 2),
            'max_regression_percent': round(max_regression, 2),
            'max_improvement_percent': round(max_improvement, 2)
        }

        report = AnalysisReport(
            has_regression=has_regression,
            regression_count=regression_count,
            improvement_count=improvement_count,
            total_tests=len(current_results),
            comparisons=comparisons,
            summary=summary
        )

        return report

    def save_analysis(self, report: AnalysisReport, output_path: Path):
        """
        Save analysis report to JSON file.

        Args:
            report: Analysis report
            output_path: Output file path
        """
        try:
            # Convert to dict
            data = {
                'has_regression': report.has_regression,
                'regression_count': report.regression_count,
                'improvement_count': report.improvement_count,
                'total_tests': report.total_tests,
                'comparisons': [
                    {
                        'name': c.name,
                        'current_mean': c.current_mean,
                        'baseline_mean': c.baseline_mean,
                        'change_percent': round(c.change_percent, 2),
                        'is_regression': c.is_regression,
                        'is_improvement': c.is_improvement,
                        'threshold_exceeded': c.threshold_exceeded
                    }
                    for c in report.comparisons
                ],
                'summary': report.summary
            }

            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2)

            print(f" Analysis saved to: {output_path}")

        except Exception as e:
            print(f" Error saving analysis: {e}")
            sys.exit(1)

    def print_summary(self, report: AnalysisReport):
        """
        Print analysis summary to console.

        Args:
            report: Analysis report
        """
        print("\n" + "=" * 60)
        print(" PERFORMANCE ANALYSIS SUMMARY")
        print("=" * 60)

        print(f"\n Total Tests: {report.total_tests}")
        print(f" Compared: {len(report.comparisons)}")

        if report.comparisons:
            print(f"\n Threshold: {report.summary['threshold_percent']}%")
            print(f" Average Change: {report.summary['avg_change_percent']}%")

            if report.regression_count > 0:
                print(f"\n REGRESSIONS: {report.regression_count}")
                print(f"   Worst: {report.summary['max_regression_percent']}%")

                print("\n   Regressed tests:")
                for comp in sorted(
                    [c for c in report.comparisons if c.is_regression],
                    key=lambda x: x.change_percent,
                    reverse=True
                ):
                    print(f"   - {comp.name}: +{comp.change_percent:.2f}% "
                          f"({comp.baseline_mean:.4f}s → {comp.current_mean:.4f}s)")

            if report.improvement_count > 0:
                print(f"\n IMPROVEMENTS: {report.improvement_count}")
                print(f"   Best: {report.summary['max_improvement_percent']}%")

                print("\n   Improved tests:")
                for comp in sorted(
                    [c for c in report.comparisons if c.is_improvement],
                    key=lambda x: x.change_percent
                )[:5]:  # Top 5
                    print(f"   - {comp.name}: {comp.change_percent:.2f}% "
                          f"({comp.baseline_mean:.4f}s → {comp.current_mean:.4f}s)")

            stable_count = len(report.comparisons) - report.regression_count - report.improvement_count
            if stable_count > 0:
                print(f"\n STABLE: {stable_count}")

        else:
            print("\nℹ  No baseline comparison available")

        print("\n" + "=" * 60)

        if report.has_regression:
            print(" PERFORMANCE REGRESSION DETECTED!")
            print("=" * 60)
            return 1
        else:
            print(" NO PERFORMANCE REGRESSION DETECTED")
            print("=" * 60)
            return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Analyze performance benchmark results')
    parser.add_argument('--current', type=Path, required=True,
                        help='Path to current benchmark results JSON')
    parser.add_argument('--baseline', type=Path,
                        help='Path to baseline benchmark results JSON')
    parser.add_argument('--threshold', type=float, default=10.0,
                        help='Regression threshold percentage (default: 10)')
    parser.add_argument('--output', type=Path, required=True,
                        help='Path to output analysis JSON')

    args = parser.parse_args()

    # Create analyzer
    analyzer = PerformanceAnalyzer(threshold_percent=args.threshold)

    # Generate analysis
    report = analyzer.generate_analysis(args.current, args.baseline)

    # Save results
    analyzer.save_analysis(report, args.output)

    # Print summary
    exit_code = analyzer.print_summary(report)

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
