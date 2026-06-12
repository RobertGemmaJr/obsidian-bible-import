from pathlib import Path

# File Paths
ROOT_PATH = Path(__file__).parent.parent.parent.absolute()
DATA_PATH = ROOT_PATH / "data"
BIBLES_PATH = ROOT_PATH / "Bibles"

# Bible metadata
SUPPORTED_TRANSLATIONS = [
    "ESV",
    "NIV",
    "ASV",
    "ASVs",
    "Bishops",
    "Coverdale",
    "Geneva",
    "KJV",
    "KJV Strongs",
    "NET",
    "Tyndale",
    "WEB",
]
