"""Phase 1: Export all saved posts/comments from the source account to JSON.

Items are saved in oldest-first order so that re-saving them preserves
the original chronological stacking in the target account's saved list.
"""

import json
import time

from .auth import get_source


def _serialize_item(item):
    """Convert a saved post or comment to a JSON-serializable dict."""
    base = {
        "id": item.id,
        "name": item.name,  # fullname, e.g. t1_abc or t3_xyz
        "permalink": item.permalink,
        "created_utc": item.created_utc,
        "subreddit": str(item.subreddit),
    }

    if item.name.startswith("t3_"):  # submission (post)
        base["type"] = "submission"
        base["title"] = item.title
        base["url"] = item.url
        base["selftext"] = item.selftext[:500] if item.selftext else ""
        base["author"] = str(item.author) if item.author else "[deleted]"
    elif item.name.startswith("t1_"):  # comment
        base["type"] = "comment"
        base["body"] = item.body[:500] if item.body else ""
        base["author"] = str(item.author) if item.author else "[deleted]"
        base["link_title"] = item.link_title
    else:
        base["type"] = "unknown"

    return base


def export_saved(config_path="config.ini", output_file="saved_items.json"):
    """Fetch all saved items and write them to a JSON file (oldest first).

    Reddit returns saved items newest-first, so we reverse after collecting.
    """
    reddit = get_source(config_path)
    user = reddit.user.me()
    print(f"Logged in as: {user.name}")
    print("Fetching saved items (this may take a while)...")

    saved_items = []
    count = 0
    for item in user.saved(limit=None):
        saved_items.append(_serialize_item(item))
        count += 1
        if count % 100 == 0:
            print(f"  ...fetched {count} items so far")

    # Reverse to oldest-first order
    saved_items.reverse()

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(saved_items, f, indent=2, ensure_ascii=False)

    print(f"Exported {len(saved_items)} saved items to {output_file} (oldest first)")
    return saved_items


if __name__ == "__main__":
    export_saved()
