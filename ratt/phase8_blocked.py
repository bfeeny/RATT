"""Phase 8: Transfer blocked users from source to target account.

Exports the block list to JSON, then blocks those users on the target account.
"""

import json
import os
import time

from .auth import get_source, get_target


EXPORT_FILE = "blocked_users.json"
PROGRESS_FILE = "blocked_import_progress.json"


def export_blocked(config_path="config.ini", output_file=EXPORT_FILE):
    """Export all blocked users from the source account."""
    reddit = get_source(config_path)
    user = reddit.user.me()
    print(f"Logged in as: {user.name}")
    print("Fetching blocked users...")

    blocked = []
    for redditor in user.blocked():
        blocked.append({
            "name": redditor.name,
            "id": redditor.id,
        })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(blocked, f, indent=2)

    print(f"Exported {len(blocked)} blocked users to {output_file}")
    return blocked


def import_blocked(
    config_path="config.ini",
    input_file=EXPORT_FILE,
    progress_file=PROGRESS_FILE,
):
    """Block exported users on the target account."""
    reddit = get_target(config_path)
    user = reddit.user.me()
    print(f"Logged in as: {user.name}")

    with open(input_file, "r", encoding="utf-8") as f:
        users = json.load(f)

    done = set()
    if os.path.exists(progress_file):
        with open(progress_file, "r") as f:
            done = set(json.load(f))

    total = len(users)
    blocked = 0
    errors = 0

    print(f"Total users to block: {total} ({len(done)} already done)")

    for i, u in enumerate(users, 1):
        name = u["name"]
        if name in done:
            continue

        try:
            redditor = reddit.redditor(name)
            redditor.block()
            blocked += 1
            done.add(name)
        except Exception as e:
            print(f"  [{i}/{total}] Error blocking u/{name}: {e}")
            errors += 1

        if blocked % 25 == 0 and blocked > 0:
            with open(progress_file, "w") as f:
                json.dump(sorted(done), f)

        time.sleep(0.5)

    with open(progress_file, "w") as f:
        json.dump(sorted(done), f)

    print(f"Done. Blocked: {blocked}, Errors: {errors}, Total: {total}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "import":
        import_blocked()
    else:
        export_blocked()
