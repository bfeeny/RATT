"""Phase 2: Re-save exported items on the target account.

Reads the JSON file produced by Phase 1 and saves each item on the target
account in oldest-first order. Tracks progress so it can resume if interrupted.
"""

import json
import os
import time

from .auth import get_target


PROGRESS_FILE = "saved_import_progress.json"


def _load_progress(progress_file):
    """Load the set of already-saved item fullnames."""
    if os.path.exists(progress_file):
        with open(progress_file, "r") as f:
            return set(json.load(f))
    return set()


def _save_progress(done_names, progress_file):
    """Persist the set of completed item fullnames."""
    with open(progress_file, "w") as f:
        json.dump(sorted(done_names), f)


def import_saved(
    config_path="config.ini",
    input_file="saved_items.json",
    progress_file=PROGRESS_FILE,
):
    """Save each item from the JSON export on the target account."""
    reddit = get_target(config_path)
    user = reddit.user.me()
    print(f"Logged in as: {user.name}")

    with open(input_file, "r", encoding="utf-8") as f:
        items = json.load(f)

    done = _load_progress(progress_file)
    total = len(items)
    skipped = 0
    saved = 0
    errors = 0

    print(f"Total items to process: {total} ({len(done)} already done)")

    for i, item in enumerate(items, 1):
        fullname = item["name"]

        if fullname in done:
            skipped += 1
            continue

        try:
            # Fetch the actual Reddit object by fullname and save it
            submission_or_comment = reddit.info(fullnames=[fullname])
            for obj in submission_or_comment:
                obj.save()
                saved += 1
                done.add(fullname)
                break
            else:
                print(f"  [{i}/{total}] Not found (deleted?): {fullname}")
                errors += 1
                done.add(fullname)  # mark so we don't retry deleted items
        except Exception as e:
            print(f"  [{i}/{total}] Error saving {fullname}: {e}")
            errors += 1

        # Save progress every 25 items
        if saved % 25 == 0 and saved > 0:
            _save_progress(done, progress_file)

        # Respect rate limits — small delay between API calls
        time.sleep(0.5)

        if i % 100 == 0:
            print(f"  ...processed {i}/{total} (saved={saved}, errors={errors})")

    _save_progress(done, progress_file)
    print(
        f"Done. Saved: {saved}, Skipped (already done): {skipped}, "
        f"Errors: {errors}, Total: {total}"
    )


if __name__ == "__main__":
    import_saved()
