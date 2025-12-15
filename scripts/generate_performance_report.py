"""
Performance Report Generator
Author: Mauro Risonho de Paula Assumpção aka firebitsbr
License: MIT

Generates markdown performance reports for CI/CD.
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


class PerformanceReportGenerator:
    """Generates markdown performance reports."""

    def __init__(self):
        """Initialize report generator."""
        pass

    def load_analysis(self, analysis_path: Path) -> Dict[str, Any]:
        """
        Load analysis results from JSON file.

        Args:
            analysis_path: Path to analysis JSON

        Returns:
            Analysis data dictionary
        """
        if not analysis_path.exists():
            return {
                'error': 'Analysis file not found',
                'has_regression': False,
                'regression_count': 0,
                'improvement_count': 0,
                'total_tests': 0,
                'comparisons': [],
                'summary': {}
            }

        try:
            with open(analysis_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            return {
                'error': f'Failed to load analysis: {e}',
                'has_regression': False,
                'regression_count': 0,
                'improvement_count': 0,
                'total_tests': 0,
                'comparisons': [],
                'summary': {}
            }

    def generate_report(self, analysis: Dict[str, Any]) -> str:
        """
        Generate markdown report from analysis.

        Args:
            analysis: Analysis data

        Returns:
            Markdown formatted report
        """
        report = []

        # Header
        report.append("###  Performance Benchmark Results\n")
        report.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}*\n")

        # Check for errors
        if 'error' in analysis:
            report.append(f"\n **Warning:** {analysis['error']}\n")
            return '\n'.join(report)

        # Summary
        total_tests = analysis['total_tests']
        comparisons = analysis.get('comparisons', [])
        regression_count = analysis['regression_count']
        improvement_count = analysis['improvement_count']
        summary = analysis.get('summary', {})

        report.append(f"\n#### Summary\n")
        report.append(f"- **Total Tests:** {total_tests}")
        report.append(f"- **Compared with Baseline:** {len(comparisons)}")

        if comparisons:
            threshold = summary.get('threshold_percent', 10)
            avg_change = summary.get('avg_change_percent', 0)

            report.append(f"- **Regression Threshold:** {threshold}%")
            report.append(f"- **Average Change:** {avg_change:+.2f}%")

            # Overall status
            report.append(f"\n#### Status\n")

            if regression_count > 0:
                report.append(f" **{regression_count} Performance Regression(s) Detected**\n")
                max_regression = summary.get('max_regression_percent', 0)
                report.append(f"*Worst regression: +{max_regression:.2f}%*\n")
            else:
                report.append(f" **No Performance Regressions Detected**\n")

            if improvement_count > 0:
                report.append(f" **{improvement_count} Performance Improvement(s)**\n")
                max_improvement = summary.get('max_improvement_percent', 0)
                report.append(f"*Best improvement: {max_improvement:.2f}%*\n")

            stable_count = len(comparisons) - regression_count - improvement_count
            if stable_count > 0:
                report.append(f" **{stable_count} Test(s) Stable**\n")

            # Detailed results
            if regression_count > 0:
                report.append(f"\n####  Regressions\n")
                report.append("| Test | Baseline | Current | Change |\n")
                report.append("|------|----------|---------|--------|\n")

                regressions = sorted(
                    [c for c in comparisons if c.get('is_regression', False)],
                    key=lambda x: x['change_percent'],
                    reverse=True
                )

                for comp in regressions:
                    name = comp['name'].replace('test_', '')
                    baseline = comp['baseline_mean']
                    current = comp['current_mean']
                    change = comp['change_percent']

                    report.append(
                        f"| `{name}` | {baseline:.4f}s | {current:.4f}s | "
                        f"+{change:.2f}%  |\n"
                    )

            if improvement_count > 0:
                report.append(f"\n####  Improvements\n")
                report.append("| Test | Baseline | Current | Change |\n")
                report.append("|------|----------|---------|--------|\n")

                improvements = sorted(
                    [c for c in comparisons if c.get('is_improvement', False)],
                    key=lambda x: x['change_percent']
                )[:10]  # Top 10

                for comp in improvements:
                    name = comp['name'].replace('test_', '')
                    baseline = comp['baseline_mean']
                    current = comp['current_mean']
                    change = comp['change_percent']

                    report.append(
                        f"| `{name}` | {baseline:.4f}s | {current:.4f}s | "
                        f"{change:.2f}%  |\n"
                    )

            # Stable tests (sample)
            stable_tests = [
                c for c in comparisons
                if not c.get('is_regression', False) and not c.get('is_improvement', False)
            ]

            if stable_tests and len(stable_tests) <= 10:
                report.append(f"\n####  Stable Tests\n")
                report.append("| Test | Baseline | Current | Change |\n")
                report.append("|------|----------|---------|--------|\n")

                for comp in stable_tests[:10]:
                    name = comp['name'].replace('test_', '')
                    baseline = comp['baseline_mean']
                    current = comp['current_mean']
                    change = comp['change_percent']

                    report.append(
                        f"| `{name}` | {baseline:.4f}s | {current:.4f}s | "
                        f"{change:+.2f}% |\n"
                    )

        else:
            report.append(f"\nℹ *No baseline comparison available. This is the first benchmark run.*\n")
            report.append(f"\n All {total_tests} tests executed successfully.\n")

        # Footer
        report.append(f"\n---\n")
        report.append(f"*Benchmark powered by pytest-benchmark*\n")

        return ''.join(report)

    def save_report(self, report: str, output_path: Path):
        """
        Save report to markdown file.

        Args:
            report: Markdown formatted report
            output_path: Output file path
        """
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w') as f:
                f.write(report)

            print(f" Report saved to: {output_path}")

        except Exception as e:
            print(f" Error saving report: {e}")
            raise


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Generate performance report')
    parser.add_argument('--analysis', type=Path, required=True,
                        help='Path to analysis JSON')
    parser.add_argument('--output', type=Path, required=True,
                        help='Path to output markdown report')

    args = parser.parse_args()

    # Create generator
    generator = PerformanceReportGenerator()

    # Load analysis
    print(" Loading analysis results...")
    analysis = generator.load_analysis(args.analysis)

    # Generate report
    print(" Generating report...")
    report = generator.generate_report(analysis)

    # Save report
    generator.save_report(report, args.output)

    # Print to console
    print("\n" + "=" * 60)
    print(report)
    print("=" * 60)


if __name__ == '__main__':
    main()
