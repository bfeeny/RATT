# RATT — Reddit Account Transfer Tool

Transfer saved posts, subscriptions, multireddits, votes, blocked users, friends, and preferences from one Reddit account to another.

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

### Run everything

```bash
python ratt.py all                                   # export + import all phases
python ratt.py export                                # export all phases
python ratt.py import                                # import all phases
```

### Run specific phases

```bash
python ratt.py saved-export          # export saved posts/comments
python ratt.py saved-import          # re-save on target account
python ratt.py subscriptions-export  # export subreddit subscriptions
python ratt.py subscriptions-import  # subscribe on target
python ratt.py multireddits-export   # export multireddits
python ratt.py multireddits-import   # create on target
python ratt.py upvoted-export        # export upvoted items
python ratt.py upvoted-import        # re-upvote on target
python ratt.py downvoted-export      # export downvoted items
python ratt.py downvoted-import      # re-downvote on target
python ratt.py hidden-export         # export hidden posts
python ratt.py hidden-import         # re-hide on target
python ratt.py blocked-export        # export blocked users
python ratt.py blocked-import        # block on target
python ratt.py friends-export        # export friends list
python ratt.py friends-import        # add friends on target
python ratt.py preferences-export    # export account preferences
python ratt.py preferences-import    # apply preferences on target
```

### Filter phases

Use `--only` or `--skip` to control which phases run with bulk commands:

```bash
python ratt.py all --only saved,subscriptions,multireddits
python ratt.py export --skip preferences,downvoted
python ratt.py import --only blocked,friends
```

### Transfer config file

For repeatable setups, use a transfer config file instead of CLI flags:

```bash
cp transfer.example.ini transfer.ini
# Edit transfer.ini to enable/disable phases
python ratt.py all --transfer-config transfer.ini
```

The `--only`/`--skip` flags can further narrow what the config enables.

## Phases

| Phase | Export file | Progress file | What it does |
|-------|-----------|--------------|-------------|
| saved | `saved_items.json` | `saved_import_progress.json` | Saved posts/comments (oldest first) |
| subscriptions | `subscriptions.json` | `subscriptions_progress.json` | Subreddit subscriptions |
| multireddits | `multireddits.json` | `multireddits_progress.json` | Custom feeds with sub lists |
| upvoted | `upvoted_items.json` | `upvoted_import_progress.json` | Upvoted posts/comments |
| downvoted | `downvoted_items.json` | `downvoted_import_progress.json` | Downvoted posts/comments |
| hidden | `hidden_items.json` | `hidden_import_progress.json` | Hidden posts |
| blocked | `blocked_users.json` | `blocked_import_progress.json` | Blocked users |
| friends | `friends.json` | `friends_import_progress.json` | Friends list |
| preferences | `preferences.json` | — | Account preferences/settings |

## Notes

- Reddit API rate limits apply — the script adds small delays between requests
- Deleted posts/comments cannot be re-saved/re-voted (they'll be logged and skipped)
- `config.ini` and `transfer.ini` contain secrets — they are gitignored and should never be committed
- Progress files are JSON and also gitignored — they allow resuming interrupted transfers
- Upvote/downvote history requires the account to have the "make my votes public" preference, or you must be authenticated as that user (which RATT does)
