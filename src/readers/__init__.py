"""
Package for reading source data into the sqlite database.
"""

from .bible_books import create_bible_books

__all__ = [
    "create_bible_books",
]
