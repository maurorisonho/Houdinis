# Performance Benchmarking System

## Overview

Automated performance benchmarking and regression detection system for the Houdinis Quantum Cryptanalysis Framework. Provides continuous performance monitoring through GitHub Actions CI/CD pipeline.

## Architecture

### Components

```
.github/workflows/performance.yml    # GitHub Actions workflow
tests/test_performance_benchmarks.py # Benchmark test suite (23 tests)
scripts/analyze_performance.py       # Performance analysis engine
scripts/generate_performance_report.py # Markdown report generator
scripts/update_performance_dashboard.py # Dashboard updater & HTML generator
performance_history.json             # Historical performance data
```

## Features

###  Automated Regression Detection
- Configurable performance threshold (default: 10%)
- Automatic PR blocking on performance regression
- Baseline caching for comparison
- Percentage change calculation

###  CI/CD Integration
- Triggers on: push, PR, schedule (daily 2 AM), manual
- Automatic PR comments with results
- Performance history tracking
- Artifact retention: 90 days

###  Comprehensive Test Coverage (23 Benchmarks)

**Categories:**
1. **Quantum Algorithms** (3 tests)
   - Shor's factorization
   - Grover's search
   - Simon's algorithm

2. **Quantum Simulator** (4 tests)
   - Initialization
   - Gate operations (Hadamard, CNOT)
   - Circuit execution

3. **Cryptographic Operations** (3 tests)
   - RSA key generation (2048-bit)
   - AES encryption (1KB)
   - SHA-256 hashing (1MB)

4. **Matrix Operations** (4 tests)
   - Multiplication (64x64)
   - Eigenvalues (32x32)
   - SVD decomposition
   - FFT (1024 points)

5. **Data Processing** (3 tests)
   - JSON serialization
   - NumPy operations
   - List comprehension

6. **File I/O** (2 tests)
   - Write/read 1MB files

7. **Memory Operations** (3 tests)
   - Array allocation
   - Memory copying
   - Dictionary creation

###  Historical Tracking & Visualization
- Performance trends over time
- HTML dashboard with Chart.js
- Commit-based history
- Category breakdown analysis

## Usage

### Running Benchmarks Locally

```bash
# Install dependencies
pip install pytest-benchmark

# Run all benchmarks
pytest tests/test_performance_benchmarks.py --benchmark-only

# Save results to JSON
pytest tests/test_performance_benchmarks.py --benchmark-only \
  --benchmark-json=benchmark_results.json

# Run specific test
pytest tests/test_performance_benchmarks.py::TestQuantumAlgorithmPerformance::test_shor_factorization_15 --benchmark-only
```

### Analyzing Results

```bash
# Compare with baseline
python scripts/analyze_performance.py \
  --current benchmark_results.json \
  --baseline baseline_results.json \
  --threshold 10

# Generate markdown report
python scripts/generate_performance_report.py \
  --analysis analysis_results.json \
  --output performance_report.md

# Update dashboard
python scripts/update_performance_dashboard.py \
  --results benchmark_results.json \
  --history performance_history.json \
  --generate-html
```

### Viewing Dashboard

```bash
# Generate HTML dashboard
python scripts/update_performance_dashboard.py \
  --results benchmark_results.json \
  --history performance_history.json \
  --generate-html

# Open in browser
open performance_dashboard.html
```

## CI/CD Workflow

### Workflow Execution

The GitHub Actions workflow runs automatically on:
- **Push** to main/develop branches
- **Pull Requests** to main/develop
- **Schedule**: Daily at 2 AM UTC
- **Manual** trigger via workflow_dispatch

### Workflow Steps

1. **Setup**: Checkout code, install Python & dependencies
2. **Execute**: Run benchmark test suite with pytest-benchmark
3. **Cache**: Download previous baseline from GitHub cache
4. **Analyze**: Compare current vs baseline, detect regressions
5. **Report**: Generate markdown report with tables
6. **Comment**: Post results to PR (if applicable)
7. **Validate**: Exit with error if regression detected
8. **Track**: Update performance history (main branch only)
9. **Persist**: Commit history back to repository

### Regression Detection Logic

```python
change_percentage = ((current_time - baseline_time) / baseline_time) * 100

if change_percentage > threshold:
    status = "REGRESSION "
    exit_code = 1  # Fail the workflow
elif change_percentage < -threshold:
    status = "IMPROVEMENT "
else:
    status = "STABLE "
```

### PR Comments

Example PR comment format:

```markdown
##  Performance Benchmark Results

**Timestamp:** 2025-12-15 10:30:00 UTC

### Summary
- Total tests: 23
- Compared: 23
- Threshold: 10%
- Average change: +2.3%

### Status
-  Regressions: 1
-  Improvements: 5
-  Stable: 17

###  Performance Regressions

| Test | Baseline | Current | Change |
|------|----------|---------|--------|
| quantum_shor_factorization | 0.1234s | 0.1456s | +18.0%  |

###  Performance Improvements (Top 10)

| Test | Baseline | Current | Change |
|------|----------|---------|--------|
| matrix_multiplication | 0.0500s | 0.0425s | -15.0%  |
| aes_encryption | 0.0120s | 0.0108s | -10.0%  |

###  Stable Tests (Sample)

| Test | Baseline | Current | Change |
|------|----------|---------|--------|
| grover_search | 0.0800s | 0.0820s | +2.5%  |
| ... | ... | ... | ... |
```

## Configuration

### Customizing Threshold

Edit `.github/workflows/performance.yml`:

```yaml
- name: Analyze performance
  run: |
    python scripts/analyze_performance.py \
      --current benchmark_results.json \
      --baseline baseline_results.json \
      --threshold 15  # Change from 10 to 15%
```

### Adjusting Test Parameters

Edit `tests/test_performance_benchmarks.py`:

```python
# Change number of warmup iterations
def test_example(benchmark):
    benchmark.pedantic(
        function_to_test,
        iterations=10,  # Change iterations
        rounds=5,       # Change rounds
        warmup_rounds=2 # Change warmup
    )
```

### Modifying History Retention

Edit `scripts/update_performance_dashboard.py`:

```python
updater = PerformanceDashboardUpdater(
    max_entries=200  # Change from 100 to 200
)
```

## Dashboard

### HTML Dashboard Features

- **Average Performance Chart**: Line chart showing average execution time over commits
- **Total Time Chart**: Bar chart showing total execution time per run
- **Category Breakdown**: Doughnut chart showing performance by category
- **Statistics Cards**: 
  - Total benchmark runs
  - Total tests
  - Latest average time

### Generating Dashboard

```bash
python scripts/update_performance_dashboard.py \
  --results benchmark_results.json \
  --history performance_history.json \
  --generate-html
```

### Dashboard File

`performance_dashboard.html` - Self-contained HTML file with:
- Chart.js for interactive visualizations
- Responsive design
- Modern styling with gradients
- Real-time data from `performance_history.json`

## Troubleshooting

### Missing Dependencies

```bash
pip install pytest-benchmark
```

### Workflow Failing

Check workflow logs in GitHub Actions:
1. Go to repository → Actions tab
2. Click on failed workflow run
3. Expand failed job step
4. Look for regression detection output

### Local Testing Issues

```bash
# Verify test syntax
pytest tests/test_performance_benchmarks.py --collect-only

# Run without benchmarking
pytest tests/test_performance_benchmarks.py -v

# Generate baseline
pytest tests/test_performance_benchmarks.py --benchmark-only \
  --benchmark-json=baseline_results.json
```

### Dashboard Not Generating

```bash
# Check history file exists
cat performance_history.json

# Verify results file format
python -m json.tool benchmark_results.json

# Run updater with debug output
python scripts/update_performance_dashboard.py \
  --results benchmark_results.json \
  --history performance_history.json \
  --generate-html
```

## Best Practices

### Adding New Benchmarks

1. Add test function to `tests/test_performance_benchmarks.py`
2. Use appropriate test class for category
3. Set realistic performance thresholds
4. Document test purpose in docstring

```python
def test_new_operation(benchmark):
    """Benchmark new quantum operation."""
    result = benchmark(new_operation, args)
    assert result is not None
```

### Monitoring Performance

1. Check daily scheduled runs for trends
2. Review PR comments for immediate feedback
3. Analyze dashboard for long-term patterns
4. Investigate regressions immediately

### Maintaining Baselines

1. Update baseline after intentional optimizations
2. Regenerate baseline if test suite changes
3. Keep baseline in sync with main branch
4. Document baseline updates in commit messages

## Architecture Details

### Test Suite Design

**pytest-benchmark Integration:**
- Uses `benchmark` fixture for timing
- Automatic warmup iterations
- Statistical analysis (mean, stddev, min, max)
- Multiple rounds for reliability

**Test Organization:**
- Grouped by category (7 classes)
- Independent test isolation
- Reproducible results
- Minimal setup overhead

### Analysis Engine

**PerformanceAnalyzer Class:**
- Load benchmark results from JSON
- Compare current vs baseline
- Calculate percentage changes
- Detect regressions/improvements
- Generate analysis report
- Export to JSON for reporting

**Algorithm:**
```python
for test in current_results:
    baseline_time = baseline[test.name]
    change = ((test.mean - baseline_time) / baseline_time) * 100
    
    if change > threshold:
        regression_detected = True
    elif change < -threshold:
        improvement_detected = True
```

### Report Generator

**PerformanceReportGenerator Class:**
- Load analysis results
- Format markdown tables
- Separate sections (regressions/improvements/stable)
- Summary statistics
- Emoji indicators (  )
- Sorted by impact

### Dashboard Updater

**PerformanceDashboardUpdater Class:**
- Load historical data
- Extract summary statistics
- Add new entry with commit info
- Maintain rolling window (max 100 entries)
- Generate HTML dashboard with Chart.js
- Save updated history

**Dashboard Visualizations:**
- Line chart: Average performance over time
- Bar chart: Total execution time per run
- Doughnut chart: Performance by category

## Future Enhancements

- [ ] Add percentile tracking (p50, p95, p99)
- [ ] Implement performance regression alerts (Slack/Email)
- [ ] Add memory profiling benchmarks
- [ ] Create performance badges for README
- [ ] Integrate with external monitoring (Datadog, New Relic)
- [ ] Add A/B testing for optimizations
- [ ] Implement automated performance tuning recommendations

## Contributing

When contributing performance-related changes:

1. Run benchmarks locally before submitting PR
2. Ensure no regressions introduced
3. Document performance improvements in PR description
4. Add benchmarks for new features
5. Update thresholds if test characteristics change

## License

MIT License - Same as Houdinis Framework

## Authors

- Mauro Risonho de Paula Assumpção (aka firebitsbr)

---

**Status**:  Production Ready  
**Coverage**: 23 benchmark tests across 7 categories  
**Automation**: Full CI/CD integration  
**Visualization**: Interactive HTML dashboard
