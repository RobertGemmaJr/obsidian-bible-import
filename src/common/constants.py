from pathlib import Path

# File Paths
ROOT_PATH = Path(__file__).parent.parent.parent.absolute()
DATA_PATH = ROOT_PATH / "data"
BIBLES_PATH = ROOT_PATH / "Bibles"


# OUTPUT_PATH = ROOT_PATH / "output"
OUTPUT_PATH = Path("/mnt/c/users/gemr1/Synology/SynologyDrive/Documents/Obsidian Vault")

# Bible metadata
SUPPORTED_TRANSLATIONS = [
    "ESV",
    "NIV",
    "WEB",
    "NET",
    "ASV",
    "ASVs",
    "KJV",
    "KJV Strongs",
    "Geneva",
    "Bishops",
    "Coverdale",
    "Tyndale",
]

# Lookup of canonical sort position for each supported translation
TRANSLATION_ORDER: dict[str, int] = {abbr: i for i, abbr in enumerate(SUPPORTED_TRANSLATIONS)}
