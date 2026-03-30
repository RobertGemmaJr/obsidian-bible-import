"""
Project-wide constants for obsidian-bible-import.
"""

from pathlib import Path

# File Paths
ROOT_PATH = Path(__file__).parent.parent.absolute()
DATA_PATH = ROOT_PATH / "data"
BIBLES_PATH = ROOT_PATH / "Bibles"

# Bible metadata
SUPPORTED_TRANSLATIONS = ["ESV"]
