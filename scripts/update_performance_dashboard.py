"""
Performance Dashboard Data Updater
Author: Mauro Risonho de Paula Assumpção aka firebitsbr
License: MIT

Updates historical performance tracking data for dashboard visualization.
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import hashlib


class PerformanceDashboardUpdater:
    """Updates performance dashboard historical data."""

    def __init__(self, max_entries: int = 100):
        """
        Initialize dashboard updater.

        Args:
            max_entries: Maximum number of historical entries to keep
        """
        self.max_entries = max_entries

    def load_history(self, history_path: Path) -> Dict[str, Any]:
        """
        Load historical performance data.

        Args:
            history_path: Path to history JSON file

        Returns:
            Historical data dictionary
        """
        if not history_path.exists():
            return {
                'version': '1.0',
                'created_at': datetime.now().isoformat(),
                'entries': []
            }

        try:
            with open(history_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"  Error loading history: {e}")
            return {
                'version': '1.0',
                'created_at': datetime.now().isoformat(),
                'entries': []
            }

    def load_results(self, results_path: Path) -> Dict[str, Any]:
        """
        Load benchmark results.

        Args:
            results_path: Path to benchmark results JSON

        Returns:
            Results dictionary
        """
        if not results_path.exists():
            print(f" Results file not found: {results_path}")
            return {}

        try:
            with open(results_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f" Error loading results: {e}")
            return {}

    def extract_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract summary statistics from results.

        Args:
            results: Benchmark results

        Returns:
            Summary dictionary
        """
        benchmarks = results.get('benchmarks', [])

        if not benchmarks:
            return {}

        # Calculate aggregate statistics
        total_tests = len(benchmarks)
        mean_times = [b['stats']['mean'] for b in benchmarks]
        total_mean = sum(mean_times)
        avg_mean = total_mean / total_tests if total_tests > 0 else 0

        # Group by category (prefix before first underscore)
        categories = {}
        for benchmark in benchmarks:
            name = benchmark['name']
            category = name.split('_')[1] if '_' in name else 'other'

            if category not in categories:
                categories[category] = {
                    'count': 0,
                    'total_mean': 0.0,
                    'tests': []
                }

            categories[category]['count'] += 1
            categories[category]['total_mean'] += benchmark['stats']['mean']
            categories[category]['tests'].append({
                'name': name,
                'mean': benchmark['stats']['mean']
            })

        # Calculate category averages
        for category, data in categories.items():
            data['avg_mean'] = data['total_mean'] / data['count'] if data['count'] > 0 else 0

        summary = {
            'total_tests': total_tests,
            'total_mean': round(total_mean, 4),
            'avg_mean': round(avg_mean, 4),
            'categories': {
                cat: {
                    'count': data['count'],
                    'avg_mean': round(data['avg_mean'], 4)
                }
                for cat, data in categories.items()
            },
            'top_slowest': sorted(
                [
                    {'name': b['name'], 'mean': b['stats']['mean']}
                    for b in benchmarks
                ],
                key=lambda x: x['mean'],
                reverse=True
            )[:10]
        }

        return summary

    def add_entry(
        self,
        history: Dict[str, Any],
        results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Add new entry to history.

        Args:
            history: Historical data
            results: Current benchmark results

        Returns:
            Updated history
        """
        # Extract summary
        summary = self.extract_summary(results)

        if not summary:
            print("  No summary to add")
            return history

        # Get commit info from results
        commit_info = results.get('commit_info', {})
        commit_hash = commit_info.get('id', 'unknown')
        branch = commit_info.get('branch', 'unknown')

        # Create entry
        entry = {
            'timestamp': datetime.now().isoformat(),
            'commit': commit_hash[:8] if len(commit_hash) > 8 else commit_hash,
            'branch': branch,
            'summary': summary
        }

        # Add to entries
        entries = history.get('entries', [])
        entries.append(entry)

        # Trim to max entries (keep most recent)
        if len(entries) > self.max_entries:
            entries = entries[-self.max_entries:]

        # Update history
        history['entries'] = entries
        history['updated_at'] = datetime.now().isoformat()
        history['total_entries'] = len(entries)

        return history

    def save_history(self, history: Dict[str, Any], output_path: Path):
        """
        Save updated history to file.

        Args:
            history: Historical data
            output_path: Output file path
        """
        try:
            with open(output_path, 'w') as f:
                json.dump(history, f, indent=2)

            print(f" History saved to: {output_path}")
            print(f"   Total entries: {len(history.get('entries', []))}")

        except Exception as e:
            print(f" Error saving history: {e}")
            raise

    def generate_dashboard_html(self, history: Dict[str, Any], output_path: Path):
        """
        Generate HTML dashboard visualization.

        Args:
            history: Historical data
            output_path: Output HTML file path
        """
        entries = history.get('entries', [])

        if not entries:
            print("  No entries to visualize")
            return

        # Generate Chart.js visualization
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Houdinis Performance Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1> Houdinis Performance Dashboard</h1>
        <p>Historical performance tracking for Houdinis Quantum Cryptanalysis Framework</p>
        <p>Last updated: {history.get('updated_at', 'N/A')}</p>
    </div>

    <div class="stats">
        <div class="stat-card">
            <div class="stat-value">{len(entries)}</div>
            <div class="stat-label">Total Benchmark Runs</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{entries[-1]['summary']['total_tests'] if entries else 0}</div>
            <div class="stat-label">Total Tests</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{entries[-1]['summary']['avg_mean']:.4f}s</div>
            <div class="stat-label">Latest Avg Time</div>
        </div>
    </div>

    <div class="chart-container">
        <h2> Average Performance Over Time</h2>
        <canvas id="avgChart"></canvas>
    </div>

    <div class="chart-container">
        <h2> Total Execution Time Trend</h2>
        <canvas id="totalChart"></canvas>
    </div>

    <div class="chart-container">
        <h2> Performance by Category</h2>
        <canvas id="categoryChart"></canvas>
    </div>

    <script>
        const data = {json.dumps(entries, indent=2)};

        // Average performance chart
        new Chart(document.getElementById('avgChart'), {{
            type: 'line',
            data: {{
                labels: data.map(e => e.commit),
                datasets: [{{
                    label: 'Average Time (seconds)',
                    data: data.map(e => e.summary.avg_mean),
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ display: true }},
                    tooltip: {{ mode: 'index' }}
                }},
                scales: {{
                    y: {{ beginAtZero: true }}
                }}
            }}
        }});

        // Total time chart
        new Chart(document.getElementById('totalChart'), {{
            type: 'bar',
            data: {{
                labels: data.map(e => e.commit),
                datasets: [{{
                    label: 'Total Time (seconds)',
                    data: data.map(e => e.summary.total_mean),
                    backgroundColor: '#764ba2',
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ display: true }}
                }},
                scales: {{
                    y: {{ beginAtZero: true }}
                }}
            }}
        }});

        // Category breakdown (latest)
        const latestCategories = data[data.length - 1].summary.categories;
        new Chart(document.getElementById('categoryChart'), {{
            type: 'doughnut',
            data: {{
                labels: Object.keys(latestCategories),
                datasets: [{{
                    data: Object.values(latestCategories).map(c => c.avg_mean),
                    backgroundColor: [
                        '#667eea', '#764ba2', '#f093fb', '#4facfe',
                        '#43e97b', '#fa709a', '#fee140', '#30cfd0'
                    ]
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ position: 'right' }}
                }}
            }}
        }});
    </script>
</body>
</html>"""

        try:
            with open(output_path, 'w') as f:
                f.write(html)

            print(f" Dashboard HTML generated: {output_path}")

        except Exception as e:
            print(f" Error generating dashboard: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Update performance dashboard data')
    parser.add_argument('--results', type=Path, required=True,
                        help='Path to current benchmark results JSON')
    parser.add_argument('--history', type=Path, required=True,
                        help='Path to performance history JSON')
    parser.add_argument('--max-entries', type=int, default=100,
                        help='Maximum historical entries to keep (default: 100)')
    parser.add_argument('--generate-html', action='store_true',
                        help='Generate HTML dashboard')

    args = parser.parse_args()

    # Create updater
    updater = PerformanceDashboardUpdater(max_entries=args.max_entries)

    # Load history
    print(" Loading performance history...")
    history = updater.load_history(args.history)

    # Load current results
    print(" Loading current results...")
    results = updater.load_results(args.results)

    if not results:
        print(" No results to process")
        return

    # Add new entry
    print(" Adding new entry to history...")
    history = updater.add_entry(history, results)

    # Save updated history
    updater.save_history(history, args.history)

    # Generate HTML dashboard if requested
    if args.generate_html:
        html_path = args.history.parent / 'performance_dashboard.html'
        print(" Generating HTML dashboard...")
        updater.generate_dashboard_html(history, html_path)


if __name__ == '__main__':
    main()
