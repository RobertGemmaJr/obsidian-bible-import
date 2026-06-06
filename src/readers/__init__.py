"""
Package for reading source data into the sqlite database.
"""

from .bible_books import read_bible_books
from .esv_bible import read_esv_bible
from .niv_bible import read_niv_bible

__all__ = ["read_bible_books", "read_esv_bible", "read_niv_bible"]
