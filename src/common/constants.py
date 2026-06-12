from pathlib import Path

# File Paths
ROOT_PATH = Path(__file__).parent.parent.parent.absolute()
DATA_PATH = ROOT_PATH / "data"
BIBLES_PATH = ROOT_PATH / "Bibles"
OUTPUT_PATH = ROOT_PATH / "output"

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
