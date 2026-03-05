"""Phase 3: Copy subreddit subscriptions from source to target account.

Exports source subscriptions to JSON, then subscribes on the target account.
Tracks progress for resumability.
"""

import json
import os
import time

from .auth import get_source, get_target


EXPORT_FILE = "subscriptions.json"
PROGRESS_FILE = "subscriptions_progress.json"


def export_subscriptions(config_path="config.ini", output_file=EXPORT_FILE):
    """Export all subreddit subscriptions from the source account."""
    reddit = get_source(config_path)
    user = reddit.user.me()
    print(f"Logged in as: {user.name}")
    print("Fetching subscriptions...")

    subs = []
    for subreddit in user.subreddits(limit=None):
        subs.append({
            "name": subreddit.display_name,
            "id": subreddit.id,
            "over18": subreddit.over18,
        })

    subs.sort(key=lambda s: s["name"].lower())

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(subs, f, indent=2)

    print(f"Exported {len(subs)} subscriptions to {output_file}")
    return subs


def import_subscriptions(
    config_path="config.ini",
    input_file=EXPORT_FILE,
    progress_file=PROGRESS_FILE,
):
    """Subscribe to all exported subreddits on the target account."""
    reddit = get_target(config_path)
    user = reddit.user.me()
    print(f"Logged in as: {user.name}")

    with open(input_file, "r", encoding="utf-8") as f:
        subs = json.load(f)

    # Load progress
    done = set()
    if os.path.exists(progress_file):
        with open(progress_file, "r") as f:
            done = set(json.load(f))

    total = len(subs)
    subscribed = 0
    errors = 0

    print(f"Total subreddits to subscribe: {total} ({len(done)} already done)")

    for i, sub in enumerate(subs, 1):
        name = sub["name"]
        if name in done:
            continue

        try:
            subreddit = reddit.subreddit(name)
            subreddit.subscribe()
            subscribed += 1
            done.add(name)
        except Exception as e:
            print(f"  [{i}/{total}] Error subscribing to r/{name}: {e}")
            errors += 1

        if subscribed % 25 == 0 and subscribed > 0:
            with open(progress_file, "w") as f:
                json.dump(sorted(done), f)

        time.sleep(0.5)

        if i % 100 == 0:
            print(f"  ...processed {i}/{total}")

    with open(progress_file, "w") as f:
        json.dump(sorted(done), f)

    print(f"Done. Subscribed: {subscribed}, Errors: {errors}, Total: {total}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "import":
        import_subscriptions()
    else:
        export_subscriptions()
