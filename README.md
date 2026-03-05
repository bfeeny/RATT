# RATT — Reddit Account Transfer Tool

Transfer saved posts, subscriptions, and multireddits from one Reddit account to another.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create Reddit API apps** for both accounts at https://www.reddit.com/prefs/apps/
   - Choose "script" as the app type for each

3. **Configure credentials:**
   ```bash
   cp config.example.ini config.ini
   # Edit config.ini with your client IDs, secrets, and passwords
   ```

## Usage

Each phase can be run independently. If something fails mid-way, re-run the same command — progress is tracked and it will resume where it left off.

```bash
# Phase 1: Export saved posts/comments from source account
python ratt.py phase1

# Phase 2: Re-save those items on the target account
python ratt.py phase2

# Phase 3: Copy subscriptions
python ratt.py phase3-export    # export from source
python ratt.py phase3-import    # subscribe on target

# Phase 4: Copy multireddits
python ratt.py phase4-export    # export from source
python ratt.py phase4-import    # create on target

# Or run everything at once
python ratt.py all
```

## How It Works

| Phase | Export file | Progress file | What it does |
|-------|-----------|--------------|-------------|
| 1 | `saved_items.json` | — | Exports all saved posts/comments (oldest first) |
| 2 | reads `saved_items.json` | `saved_import_progress.json` | Saves each item on target account |
| 3 | `subscriptions.json` | `subscriptions_progress.json` | Copies subreddit subscriptions |
| 4 | `multireddits.json` | `multireddits_progress.json` | Copies multireddits with their subreddit lists |

## Notes

- Reddit API rate limits apply — the script adds small delays between requests
- Deleted posts/comments cannot be re-saved (they'll be logged and skipped)
- The `config.ini` file contains secrets — it is gitignored and should never be committed
- Progress files are JSON and also gitignored — they allow resuming interrupted transfers
