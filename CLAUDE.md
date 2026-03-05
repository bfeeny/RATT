# CLAUDE.md

This file provides guidance for AI assistants working with the RATT repository.

## Repository Overview

**RATT (Reddit Account Transfer Tool)** transfers saved posts, subscriptions, and multireddits from one Reddit account to another. Built with Python using PRAW (Python Reddit API Wrapper).

## Project Structure

```
RATT/
├── ratt.py                        # CLI entry point
├── ratt/                          # Package directory
│   ├── __init__.py
│   ├── auth.py                    # PRAW authentication helpers
│   ├── phase1_export_saved.py     # Export saved posts/comments to JSON
│   ├── phase2_import_saved.py     # Re-save items on target account
│   ├── phase3_subscriptions.py    # Export/import subreddit subscriptions
│   └── phase4_multireddits.py     # Export/import multireddits
├── config.example.ini             # Template for Reddit API credentials
├── requirements.txt               # Python dependencies (praw)
├── README.md
└── CLAUDE.md
```

## Commands

```bash
pip install -r requirements.txt        # Install dependencies

python ratt.py phase1                  # Export saved posts/comments from source
python ratt.py phase2                  # Re-save items on target account
python ratt.py phase3-export           # Export subscriptions from source
python ratt.py phase3-import           # Subscribe on target account
python ratt.py phase4-export           # Export multireddits from source
python ratt.py phase4-import           # Create multireddits on target
python ratt.py all                     # Run all phases in sequence
```

## Architecture

- **Config:** `config.ini` (gitignored) holds Reddit API credentials for `[source]` and `[target]` accounts. Copy from `config.example.ini`.
- **Phases are independent:** Each phase reads/writes its own JSON files and tracks progress separately. If interrupted, re-running the same command resumes where it left off.
- **Progress tracking:** Import phases (2, 3-import, 4-import) write `*_progress.json` files to track which items have been processed.
- **Rate limiting:** Small `time.sleep()` delays between API calls to respect Reddit rate limits.
- **Order matters for saved items:** Phase 1 exports in oldest-first order so Phase 2 re-saves in the same order, preserving chronological stacking.

## Code Style

- Python 3, no type annotations enforced yet
- Standard library + PRAW only — keep dependencies minimal
- Each phase module is runnable standalone (`if __name__ == "__main__"`)
- Functions should be small and focused
- Use `snake_case` for functions/variables

## Key Conventions for AI Assistants

1. **Read before editing** — Always read a file before modifying it
2. **Minimal changes** — Only change what is necessary to accomplish the task
3. **No over-engineering** — Keep solutions simple; avoid premature abstractions
4. **No secrets in code** — Never commit credentials, API keys, or tokens; `config.ini` and `*.json` data files are gitignored
5. **Preserve existing patterns** — Match the phase-based module structure when adding new transfer capabilities
6. **Resumability** — All import operations must track progress and be safe to re-run
7. **Independence** — Each phase must work independently; don't create cross-phase dependencies
