# Legacy Files

This directory contains deprecated files and scripts that are kept for historical reference but are no longer actively used in the project.

##  Contents

### Git History Scripts (Deprecated)
- **`rewrite_git_history.sh`** - Legacy bash script for git history rewriting
- **`rewrite_history_simple.sh`** - Simplified version of history rewriting script

### Documentation (Archived)
- **`EMOJI_REMOVAL.md`** - Documentation about emoji removal process (completed)
- **`IMPLEMENTATION_SUMMARY.md`** - Old implementation summary (superseded)

##  Warning

These files are **no longer maintained** and should not be used in production or development workflows. They are preserved for:
- Historical reference
- Understanding past decisions
- Potential future insights

##  Replacements

| Legacy File | Current Alternative |
|-------------|---------------------|
| `rewrite_git_history.sh` | `.tools/rewrite_git_history.py` |
| `EMOJI_REMOVAL.md` | Completed - see `.reports/` for results |
| `IMPLEMENTATION_SUMMARY.md` | See `docs/IMPLEMENTATION_SUMMARY.md` |

##  Cleanup

These files may be permanently removed in future major releases. If you need any of this functionality:
1. Check the replacements listed above
2. Review current documentation in `docs/`
3. Consult git history for implementation details

---

**Note:** This directory is hidden (`.legacy`) to avoid cluttering the main project structure.

**Developed by:** Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)
