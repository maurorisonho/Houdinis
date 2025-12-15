# Project Reports

This directory contains various reports, logs, and analysis results generated during development and testing.

##  Contents

### Translation & Headers Reports
- **`header_update_report.txt`** - Report of header additions across the project
- **`translation_report.txt`** - Detailed translation report (Portuguese → English)

### Performance Reports
- **`performance_report.md`** - Performance analysis and benchmarks
- **`performance_dashboard.html`** - Interactive performance dashboard
- **`performance_history.json`** - Historical performance data

### Analysis Results
- **`analysis_results.json`** - Code analysis results
- **`baseline_results.json`** - Baseline metrics for comparisons
- **`qml_attacks_report.json`** - Quantum Machine Learning attacks analysis
- **`side_channel_report.json`** - Side-channel attacks analysis

### Build & Operation Logs
- **`build.log`** - Build process logs
- **`file_operations.log`** - File operation tracking logs

##  Usage

These reports are generated automatically during various project operations and provide insights into:
- Code quality and coverage
- Performance metrics
- Security analysis
- Translation and documentation updates

##  Viewing Reports

### JSON Reports
```bash
# Pretty print JSON reports
cat .reports/analysis_results.json | python -m json.tool
```

### HTML Dashboard
```bash
# Open performance dashboard
xdg-open .reports/performance_dashboard.html  # Linux
open .reports/performance_dashboard.html      # macOS
```

### Text Reports
```bash
# View text reports
cat .reports/header_update_report.txt
cat .reports/translation_report.txt
```

---

**Developed by:** Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)
