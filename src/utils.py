"""
Project-wide utility functions for obsidian-bible-import.
"""

from typing import Optional


def to_bool(value) -> Optional[bool]:
    """Coerce a SQLite '0'/'1' meta value into a bool (or None if empty/missing)."""
    if value is None or value == "":
        return None
    return value not in ("0", 0, False, "false", "False")


def to_int(value) -> Optional[int]:
    """Coerce a SQLite numeric meta value into an int (or None if empty/missing)."""
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
