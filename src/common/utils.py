"""
Project-wide utility functions for obsidian-bible-import.
"""

import html
import json
import re
from pathlib import Path
from typing import Any, Optional

#################### CONVERTERS ####################


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


def read_json(path: Path) -> Any:
    """Read and parse a JSON file."""
    with open(path, "r") as f:
        return json.load(f)


#################### CONVERTERS ####################


def clean_text(text: str) -> str:
    """Strip HTML tags and unescape entities from a verse text string."""
    cleaned = text.replace("<br/>", "\n").replace("<br>", "\n")
    cleaned = re.sub(r"<[^>]+>", "", cleaned)
    cleaned = html.unescape(cleaned)
    return cleaned.strip()
