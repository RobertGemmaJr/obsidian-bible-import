"""
Project-wide utility functions for obsidian-bible-import.
"""

import html
import json
import re
from pathlib import Path
from typing import Any, Optional


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


def clean_text(text: str) -> str:
    """Strip HTML tags and unescape entities from a verse text string."""
    cleaned = text.replace("<br/>", "\n").replace("<br>", "\n")
    cleaned = re.sub(r"<[^>]+>", "", cleaned)
    cleaned = html.unescape(cleaned)
    return cleaned.strip()


def yaml_quote(value: str) -> str:
    """Quote a string for safe inclusion in a YAML double-quoted scalar."""
    escaped = (
        value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
    )
    return f'"{escaped}"'


def format_field(name: str, value) -> str:
    if value is None:
        return f"{name}:"
    if isinstance(value, bool):
        return f"{name}: {'true' if value else 'false'}"
    if isinstance(value, (int, float)):
        return f"{name}: {value}"
    return f"{name}: {yaml_quote(str(value))}"
