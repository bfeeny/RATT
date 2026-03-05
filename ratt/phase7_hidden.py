"""Phase 7: Transfer hidden posts from source to target account.

Exports all hidden posts to JSON, then re-hides them on the target account.
"""

import json
import os
import time

from .auth import get_source, get_target


EXPORT_FILE = "hidden_items.json"
PROGRESS_FILE = "hidden_import_progress.json"


def _serialize_item(item):
    """Convert a hidden post to a JSON-serializable dict."""
    return {
        "id": item.id,
        "name": item.name,
        "permalink": item.permalink,
        "created_utc": item.created_utc,
        "subreddit": str(item.subreddit),
        "type": "submission",
        "title": item.title,
        "author": str(item.author) if item.author else "[deleted]",
    }


def export_hidden(config_path="config.ini", output_file=EXPORT_FILE):
    """Export all hidden posts from the source account."""
    reddit = get_source(config_path)
    user = reddit.user.me()
    print(f"Logged in as: {user.name}")
    print("Fetching hidden posts...")

    items = []
    count = 0
    for item in user.hidden(limit=None):
        items.append(_serialize_item(item))
        count += 1
        if count % 100 == 0:
            print(f"  ...fetched {count} items so far")

    items.reverse()  # oldest first

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

    print(f"Exported {len(items)} hidden posts to {output_file}")
    return items


def import_hidden(
    config_path="config.ini",
    input_file=EXPORT_FILE,
    progress_file=PROGRESS_FILE,
):
    """Re-hide exported posts on the target account."""
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
    hidden = 0
    errors = 0

    print(f"Total items to process: {total} ({len(done)} already done)")

    for i, item in enumerate(items, 1):
        fullname = item["name"]
        if fullname in done:
            continue

        try:
            for obj in reddit.info(fullnames=[fullname]):
                obj.hide()
                hidden += 1
                done.add(fullname)
                break
            else:
                done.add(fullname)
                errors += 1
        except Exception as e:
            print(f"  [{i}/{total}] Error hiding {fullname}: {e}")
            errors += 1

        if hidden % 25 == 0 and hidden > 0:
            with open(progress_file, "w") as f:
                json.dump(sorted(done), f)

        time.sleep(0.5)

        if i % 100 == 0:
            print(f"  ...processed {i}/{total}")

    with open(progress_file, "w") as f:
        json.dump(sorted(done), f)

    print(f"Done. Hidden: {hidden}, Errors: {errors}, Total: {total}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "import":
        import_hidden()
    else:
        export_hidden()
