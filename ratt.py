#!/usr/bin/env python3
"""RATT — Reddit Account Transfer Tool.

Transfer saved posts, subscriptions, multireddits, votes, and more
between Reddit accounts.

Usage:
    python ratt.py export              Export all enabled content from source
    python ratt.py import              Import all enabled content to target
    python ratt.py all                 Export then import everything enabled

    python ratt.py <phase>-export      Export a specific phase
    python ratt.py <phase>-import      Import a specific phase

  Phases: saved, subscriptions, multireddits, upvoted, downvoted,
          hidden, blocked, friends, preferences

  Filtering (applies to export, import, and all):
    --only saved,upvoted,blocked       Only run these phases
    --skip downvoted,preferences       Skip these phases

  Config:
    --transfer-config transfer.ini     Use a transfer config file to
                                       enable/disable phases (see
                                       transfer.example.ini)

Examples:
    python ratt.py all
    python ratt.py all --only saved,subscriptions,multireddits
    python ratt.py export --skip preferences
    python ratt.py import --transfer-config transfer.ini
    python ratt.py saved-export
    python ratt.py blocked-import
"""

import argparse
import configparser
import sys

from ratt.phase1_export_saved import export_saved
from ratt.phase2_import_saved import import_saved
from ratt.phase3_subscriptions import export_subscriptions, import_subscriptions
from ratt.phase4_multireddits import export_multireddits, import_multireddits
from ratt.phase5_upvoted import export_upvoted, import_upvoted
from ratt.phase6_downvoted import export_downvoted, import_downvoted
from ratt.phase7_hidden import export_hidden, import_hidden
from ratt.phase8_blocked import export_blocked, import_blocked
from ratt.phase9_friends import export_friends, import_friends
from ratt.phase10_preferences import export_preferences, import_preferences


# Ordered list of all phases. Each entry: (name, export_func, import_func)
PHASES = [
    ("saved", export_saved, import_saved),
    ("subscriptions", export_subscriptions, import_subscriptions),
    ("multireddits", export_multireddits, import_multireddits),
    ("upvoted", export_upvoted, import_upvoted),
    ("downvoted", export_downvoted, import_downvoted),
    ("hidden", export_hidden, import_hidden),
    ("blocked", export_blocked, import_blocked),
    ("friends", export_friends, import_friends),
    ("preferences", export_preferences, import_preferences),
]

PHASE_NAMES = [p[0] for p in PHASES]


def _resolve_phases(args):
    """Determine which phases to run based on --only, --skip, and --transfer-config."""
    enabled = set(PHASE_NAMES)

    # Transfer config file takes precedence as a baseline
    if args.transfer_config:
        config = configparser.ConfigParser()
        files_read = config.read(args.transfer_config)
        if not files_read:
            print(f"Error: transfer config not found: {args.transfer_config}")
            sys.exit(1)
        if config.has_section("transfer"):
            enabled = set()
            for name in PHASE_NAMES:
                if config.getboolean("transfer", name, fallback=False):
                    enabled.add(name)

    # --only narrows further
    if args.only:
        only_set = set(args.only.split(","))
        unknown = only_set - set(PHASE_NAMES)
        if unknown:
            print(f"Error: unknown phases: {', '.join(unknown)}")
            print(f"Available: {', '.join(PHASE_NAMES)}")
            sys.exit(1)
        enabled &= only_set

    # --skip removes
    if args.skip:
        skip_set = set(args.skip.split(","))
        unknown = skip_set - set(PHASE_NAMES)
        if unknown:
            print(f"Error: unknown phases: {', '.join(unknown)}")
            print(f"Available: {', '.join(PHASE_NAMES)}")
            sys.exit(1)
        enabled -= skip_set

    # Return in original order
    return [(name, exp, imp) for name, exp, imp in PHASES if name in enabled]


def _run_phases(phases, mode):
    """Run export, import, or both for the given phases."""
    for name, export_func, import_func in phases:
        if mode in ("export", "all"):
            print(f"\n{'='*60}")
            print(f"  Export: {name}")
            print(f"{'='*60}\n")
            export_func()

    for name, export_func, import_func in phases:
        if mode in ("import", "all"):
            print(f"\n{'='*60}")
            print(f"  Import: {name}")
            print(f"{'='*60}\n")
            import_func()


def main():
    parser = argparse.ArgumentParser(
        description="RATT — Reddit Account Transfer Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"Available phases: {', '.join(PHASE_NAMES)}",
    )
    parser.add_argument(
        "command",
        help="Command to run (export, import, all, or <phase>-export/<phase>-import)",
    )
    parser.add_argument(
        "--only",
        help="Comma-separated list of phases to include (e.g. saved,upvoted)",
    )
    parser.add_argument(
        "--skip",
        help="Comma-separated list of phases to skip (e.g. downvoted,preferences)",
    )
    parser.add_argument(
        "--transfer-config",
        help="Path to transfer config INI file (default: not used)",
    )

    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print(__doc__)
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()
    command = args.command

    # Handle individual phase commands like "saved-export" or "blocked-import"
    for name, export_func, import_func in PHASES:
        if command == f"{name}-export":
            print(f"\n--- Export: {name} ---\n")
            export_func()
            return
        elif command == f"{name}-import":
            print(f"\n--- Import: {name} ---\n")
            import_func()
            return

    # Handle bulk commands
    if command in ("export", "import", "all"):
        phases = _resolve_phases(args)
        if not phases:
            print("No phases enabled. Check your --only/--skip/--transfer-config.")
            sys.exit(1)
        print(f"Phases to run: {', '.join(p[0] for p in phases)}")
        _run_phases(phases, command)
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
