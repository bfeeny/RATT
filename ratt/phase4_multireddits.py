"""Phase 4: Copy multireddits (custom feeds) from source to target account.

Exports all multireddits with their subreddit lists, then recreates them
on the target account.
"""

import json
import os
import time

from .auth import get_source, get_target


EXPORT_FILE = "multireddits.json"
PROGRESS_FILE = "multireddits_progress.json"


def export_multireddits(config_path="config.ini", output_file=EXPORT_FILE):
    """Export all multireddits from the source account."""
    reddit = get_source(config_path)
    user = reddit.user.me()
    print(f"Logged in as: {user.name}")
    print("Fetching multireddits...")

    multis = []
    for multi in reddit.user.multireddits():
        multis.append({
            "name": multi.name,
            "display_name": multi.display_name,
            "description_md": multi.description_md,
            "visibility": multi.visibility,
            "subreddits": [sub.display_name for sub in multi.subreddits],
        })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(multis, f, indent=2)

    print(f"Exported {len(multis)} multireddits to {output_file}")
    for m in multis:
        print(f"  - {m['display_name']} ({len(m['subreddits'])} subreddits)")
    return multis


def import_multireddits(
    config_path="config.ini",
    input_file=EXPORT_FILE,
    progress_file=PROGRESS_FILE,
):
    """Recreate exported multireddits on the target account."""
    reddit = get_target(config_path)
    user = reddit.user.me()
    print(f"Logged in as: {user.name}")

    with open(input_file, "r", encoding="utf-8") as f:
        multis = json.load(f)

    # Load progress
    done = set()
    if os.path.exists(progress_file):
        with open(progress_file, "r") as f:
            done = set(json.load(f))

    total = len(multis)
    created = 0
    errors = 0

    print(f"Total multireddits to create: {total} ({len(done)} already done)")

    for i, multi in enumerate(multis, 1):
        name = multi["name"]
        if name in done:
            continue

        try:
            # Build subreddit dicts for the PRAW multireddit.create call
            sub_dicts = [{"name": s} for s in multi["subreddits"]]

            reddit.multireddit.create(
                display_name=multi["display_name"],
                subreddits=sub_dicts,
                description_md=multi.get("description_md", ""),
                visibility=multi.get("visibility", "private"),
            )
            created += 1
            done.add(name)
            print(
                f"  [{i}/{total}] Created m/{multi['display_name']} "
                f"({len(multi['subreddits'])} subs)"
            )
        except Exception as e:
            print(f"  [{i}/{total}] Error creating m/{multi['display_name']}: {e}")
            errors += 1

        with open(progress_file, "w") as f:
            json.dump(sorted(done), f)

        time.sleep(1)

    print(f"Done. Created: {created}, Errors: {errors}, Total: {total}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "import":
        import_multireddits()
    else:
        export_multireddits()
