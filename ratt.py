#!/usr/bin/env python3
"""RATT — Reddit Account Transfer Tool.

Transfer subscriptions, saved posts, and multireddits between Reddit accounts.

Usage:
    python ratt.py phase1              Export saved posts/comments to JSON
    python ratt.py phase2              Re-save items on target account
    python ratt.py phase3-export       Export subscriptions to JSON
    python ratt.py phase3-import       Subscribe on target account
    python ratt.py phase4-export       Export multireddits to JSON
    python ratt.py phase4-import       Create multireddits on target account
    python ratt.py all                 Run all phases in sequence
"""

import sys

from ratt.phase1_export_saved import export_saved
from ratt.phase2_import_saved import import_saved
from ratt.phase3_subscriptions import export_subscriptions, import_subscriptions
from ratt.phase4_multireddits import export_multireddits, import_multireddits


COMMANDS = {
    "phase1": ("Export saved posts/comments", lambda: export_saved()),
    "phase2": ("Import saved posts/comments", lambda: import_saved()),
    "phase3-export": ("Export subscriptions", lambda: export_subscriptions()),
    "phase3-import": ("Import subscriptions", lambda: import_subscriptions()),
    "phase4-export": ("Export multireddits", lambda: export_multireddits()),
    "phase4-import": ("Import multireddits", lambda: import_multireddits()),
}


def run_all():
    """Run all phases in order: export everything, then import everything."""
    phases = [
        ("Phase 1: Export saved items", export_saved),
        ("Phase 3: Export subscriptions", export_subscriptions),
        ("Phase 4: Export multireddits", export_multireddits),
        ("Phase 2: Import saved items", import_saved),
        ("Phase 3: Import subscriptions", import_subscriptions),
        ("Phase 4: Import multireddits", import_multireddits),
    ]
    for label, func in phases:
        print(f"\n{'='*60}")
        print(f"  {label}")
        print(f"{'='*60}\n")
        func()


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print(__doc__)
        sys.exit(0)

    command = sys.argv[1]

    if command == "all":
        run_all()
    elif command in COMMANDS:
        desc, func = COMMANDS[command]
        print(f"\n--- {desc} ---\n")
        func()
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
