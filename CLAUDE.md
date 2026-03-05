# CLAUDE.md

This file provides guidance for AI assistants working with the RATT repository.

## Repository Overview

**RATT (Reddit Account Transfer Tool)** transfers saved posts, subscriptions, multireddits, votes, blocked users, friends, and preferences from one Reddit account to another. Built with Python using PRAW (Python Reddit API Wrapper).

## Project Structure

```
RATT/
├── ratt.py                        # CLI entry point (argparse-based)
├── ratt/                          # Package directory
│   ├── __init__.py
│   ├── auth.py                    # PRAW authentication helpers
│   ├── phase1_export_saved.py     # Export saved posts/comments to JSON
│   ├── phase2_import_saved.py     # Re-save items on target account
│   ├── phase3_subscriptions.py    # Export/import subreddit subscriptions
│   ├── phase4_multireddits.py     # Export/import multireddits
│   ├── phase5_upvoted.py          # Export/import upvoted items
│   ├── phase6_downvoted.py        # Export/import downvoted items
│   ├── phase7_hidden.py           # Export/import hidden posts
│   ├── phase8_blocked.py          # Export/import blocked users
│   ├── phase9_friends.py          # Export/import friends list
│   └── phase10_preferences.py     # Export/import account preferences
├── config.example.ini             # Template for Reddit API credentials
├── transfer.example.ini           # Template for phase enable/disable
├── requirements.txt               # Python dependencies (praw)
├── README.md
└── CLAUDE.md
```

## Commands

```bash
pip install -r requirements.txt             # Install dependencies

python ratt.py all                          # Export + import everything
python ratt.py export                       # Export all phases
python ratt.py import                       # Import all phases
python ratt.py <phase>-export               # Export one phase
python ratt.py <phase>-import               # Import one phase

# Filtering
python ratt.py all --only saved,subscriptions
python ratt.py export --skip preferences
python ratt.py all --transfer-config transfer.ini
```

Available phases: `saved`, `subscriptions`, `multireddits`, `upvoted`, `downvoted`, `hidden`, `blocked`, `friends`, `preferences`

## Architecture

- **Config:** `config.ini` (gitignored) holds Reddit API credentials for `[source]` and `[target]` accounts. Copy from `config.example.ini`.
- **Transfer config:** `transfer.ini` (gitignored) optionally controls which phases are enabled. CLI `--only`/`--skip` flags provide the same control inline.
- **Phases are independent:** Each phase reads/writes its own JSON files and tracks progress separately. If interrupted, re-running the same command resumes where it left off.
- **Progress tracking:** Import phases write `*_progress.json` files to track which items have been processed.
- **Rate limiting:** Small `time.sleep()` delays between API calls to respect Reddit rate limits.
- **Order matters for saved items:** Phase 1 exports in oldest-first order so Phase 2 re-saves in the same order, preserving chronological stacking.
- **Bulk commands run exports first, then imports:** The `all` command exports everything before importing anything, so all data is captured before any writes happen.

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
4. **No secrets in code** — Never commit credentials, API keys, or tokens; `config.ini`, `transfer.ini`, and `*.json` data files are gitignored
5. **Preserve existing patterns** — Match the phase-based module structure when adding new transfer capabilities
6. **Resumability** — All import operations must track progress and be safe to re-run
7. **Independence** — Each phase must work independently; don't create cross-phase dependencies
8. **Adding a new phase** — Create `ratt/phaseN_name.py` with `export_*` and `import_*` functions, add it to the `PHASES` list in `ratt.py`, add it to `transfer.example.ini`
