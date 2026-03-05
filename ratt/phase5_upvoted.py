"""Phase 5: Transfer upvoted posts/comments from source to target account.

Exports all upvoted items to JSON, then re-upvotes them on the target account.
"""

import json
import os
import time

from .auth import get_source, get_target


EXPORT_FILE = "upvoted_items.json"
PROGRESS_FILE = "upvoted_import_progress.json"


def _serialize_item(item):
    """Convert an upvoted post or comment to a JSON-serializable dict."""
    base = {
        "id": item.id,
        "name": item.name,
        "permalink": item.permalink,
        "created_utc": item.created_utc,
        "subreddit": str(item.subreddit),
    }

    if item.name.startswith("t3_"):
        base["type"] = "submission"
        base["title"] = item.title
        base["author"] = str(item.author) if item.author else "[deleted]"
    elif item.name.startswith("t1_"):
        base["type"] = "comment"
        base["body"] = item.body[:200] if item.body else ""
        base["author"] = str(item.author) if item.author else "[deleted]"
    else:
        base["type"] = "unknown"

    return base


def export_upvoted(config_path="config.ini", output_file=EXPORT_FILE):
    """Export all upvoted items from the source account."""
    reddit = get_source(config_path)
    user = reddit.user.me()
    print(f"Logged in as: {user.name}")
    print("Fetching upvoted items...")

    items = []
    count = 0
    for item in user.upvoted(limit=None):
        items.append(_serialize_item(item))
        count += 1
        if count % 100 == 0:
            print(f"  ...fetched {count} items so far")

    items.reverse()  # oldest first

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

    print(f"Exported {len(items)} upvoted items to {output_file}")
    return items


def import_upvoted(
    config_path="config.ini",
    input_file=EXPORT_FILE,
    progress_file=PROGRESS_FILE,
):
    """Re-upvote exported items on the target account."""
    reddit = get_target(config_path)
    user = reddit.user.me()
    print(f"Logged in as: {user.name}")

    with open(input_file, "r", encoding="utf-8") as f:
        items = json.load(f)

    done = set()
    if os.path.exists(progress_file):
        with open(progress_file, "r") as f:
            done = set(json.load(f))

    total = len(items)
    upvoted = 0
    errors = 0

    print(f"Total items to process: {total} ({len(done)} already done)")

    for i, item in enumerate(items, 1):
        fullname = item["name"]
        if fullname in done:
            continue

        try:
            for obj in reddit.info(fullnames=[fullname]):
                obj.upvote()
                upvoted += 1
                done.add(fullname)
                break
            else:
                done.add(fullname)
                errors += 1
        except Exception as e:
            print(f"  [{i}/{total}] Error upvoting {fullname}: {e}")
            errors += 1

        if upvoted % 25 == 0 and upvoted > 0:
            with open(progress_file, "w") as f:
                json.dump(sorted(done), f)

        time.sleep(0.5)

        if i % 100 == 0:
            print(f"  ...processed {i}/{total}")

    with open(progress_file, "w") as f:
        json.dump(sorted(done), f)

    print(f"Done. Upvoted: {upvoted}, Errors: {errors}, Total: {total}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "import":
        import_upvoted()
    else:
        export_upvoted()
