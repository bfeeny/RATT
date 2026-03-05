"""Phase 9: Transfer friends list from source to target account.

Exports the friends list to JSON, then adds them as friends on the target account.
"""

import json
import os
import time

from .auth import get_source, get_target


EXPORT_FILE = "friends.json"
PROGRESS_FILE = "friends_import_progress.json"


def export_friends(config_path="config.ini", output_file=EXPORT_FILE):
    """Export all friends from the source account."""
    reddit = get_source(config_path)
    user = reddit.user.me()
    print(f"Logged in as: {user.name}")
    print("Fetching friends list...")

    friends = []
    for friend in user.friends():
        friends.append({
            "name": friend.name,
            "id": friend.id,
        })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(friends, f, indent=2)

    print(f"Exported {len(friends)} friends to {output_file}")
    return friends


def import_friends(
    config_path="config.ini",
    input_file=EXPORT_FILE,
    progress_file=PROGRESS_FILE,
):
    """Add exported friends on the target account."""
    reddit = get_target(config_path)
    user = reddit.user.me()
    print(f"Logged in as: {user.name}")

    with open(input_file, "r", encoding="utf-8") as f:
        friends = json.load(f)

    done = set()
    if os.path.exists(progress_file):
        with open(progress_file, "r") as f:
            done = set(json.load(f))

    total = len(friends)
    added = 0
    errors = 0

    print(f"Total friends to add: {total} ({len(done)} already done)")

    for i, friend in enumerate(friends, 1):
        name = friend["name"]
        if name in done:
            continue

        try:
            redditor = reddit.redditor(name)
            redditor.friend()
            added += 1
            done.add(name)
        except Exception as e:
            print(f"  [{i}/{total}] Error adding u/{name}: {e}")
            errors += 1

        if added % 25 == 0 and added > 0:
            with open(progress_file, "w") as f:
                json.dump(sorted(done), f)

        time.sleep(0.5)

    with open(progress_file, "w") as f:
        json.dump(sorted(done), f)

    print(f"Done. Added: {added}, Errors: {errors}, Total: {total}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "import":
        import_friends()
    else:
        export_friends()
