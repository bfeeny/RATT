"""Phase 10: Transfer Reddit account preferences from source to target.

Exports preferences (content settings, notification prefs, etc.) to JSON,
then applies them on the target account via the /api/v1/me/prefs endpoint.
"""

import json

from .auth import get_source, get_target


EXPORT_FILE = "preferences.json"

# Preferences that are safe to copy between accounts.
# Excludes account-specific fields like email, username, etc.
TRANSFERABLE_PREFS = [
    "beta",
    "clickgadget",
    "collapse_read_messages",
    "compress",
    "default_comment_sort",
    "domain_details",
    "email_digests",
    "email_messages",
    "enable_default_themes",
    "enable_followers",
    "hide_ads",
    "hide_downs",
    "hide_ups",
    "highlight_controversial",
    "highlight_new_comments",
    "ignore_suggested_sort",
    "label_nsfw",
    "lang",
    "legacy_search",
    "live_orangereds",
    "mark_messages_read",
    "media",
    "media_preview",
    "min_comment_score",
    "min_link_score",
    "monitor_mentions",
    "newwindow",
    "no_profanity",
    "num_comments",
    "numsites",
    "over_18",
    "private_feeds",
    "public_votes",
    "research",
    "search_include_over_18",
    "send_crosspost_messages",
    "send_welcome_messages",
    "show_flair",
    "show_gold_expiration",
    "show_link_flair",
    "show_location_based_recommendations",
    "show_presence",
    "show_stylesheets",
    "show_trending",
    "store_visits",
    "survey_last_seen_time",
    "third_party_data_personalized_ads",
    "third_party_personalized_ads",
    "third_party_site_data_personalized_ads",
    "third_party_site_data_personalized_content",
    "threaded_messages",
    "threaded_modmail",
    "top_karma_subreddits",
    "use_global_defaults",
    "video_autoplay",
]


def export_preferences(config_path="config.ini", output_file=EXPORT_FILE):
    """Export account preferences from the source account."""
    reddit = get_source(config_path)
    user = reddit.user.me()
    print(f"Logged in as: {user.name}")

    prefs = reddit.user.preferences()

    # Filter to only transferable prefs that exist
    filtered = {k: v for k, v in prefs.items() if k in TRANSFERABLE_PREFS}

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(filtered, f, indent=2)

    print(f"Exported {len(filtered)} preferences to {output_file}")
    return filtered


def import_preferences(config_path="config.ini", input_file=EXPORT_FILE):
    """Apply exported preferences on the target account."""
    reddit = get_target(config_path)
    user = reddit.user.me()
    print(f"Logged in as: {user.name}")

    with open(input_file, "r", encoding="utf-8") as f:
        prefs = json.load(f)

    print(f"Applying {len(prefs)} preferences...")

    try:
        reddit.user.preferences.update(**prefs)
        print("Done. Preferences applied successfully.")
    except Exception as e:
        print(f"Error applying preferences: {e}")
        print("Some preferences may require Reddit Premium or may have changed.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "import":
        import_preferences()
    else:
        export_preferences()
