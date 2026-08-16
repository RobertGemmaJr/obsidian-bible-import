import sqlite3
import uuid
from pathlib import Path

from sqlmodel import Session, select

from .models import Book, Verse

__all__ = [
    "load_books_by_canonical_order",
    "load_books_in_canonical_order",
    "load_distinct_verse_coords",
    "read_sqlite_translation",
]


# ---------------------------------------------------------------------------
# Project DB queries (SQLModel / our schema)
# ---------------------------------------------------------------------------


def load_books_by_canonical_order(session: Session) -> dict[int, Book]:
    """
    Return a dict mapping every Book's canonical_order (1-66) to its Book instance.

    Used by Bible readers to translate the source-format book id (which uses the
    same 1-66 canonical-order numbering) into a Book row in O(1) without issuing
    a SELECT per verse.
    """
    return {b.canonical_order: b for b in session.exec(select(Book)).all()}


def load_books_in_canonical_order(session: Session) -> list[Book]:
    """Return every Book in canonical reading order (Genesis -> Revelation)."""
    return session.exec(select(Book).order_by(Book.canonical_order)).all()


def load_distinct_verse_coords(session: Session) -> list[tuple[uuid.UUID, int, int]]:
    """Return distinct ``(book_id, chapter_num, verse_num)`` tuples.

    This is the union of verse coverage across every translation, sorted in
    canonical reading order. Used by the book and chapter writers.
    """
    return session.exec(
        select(Verse.book_id, Verse.chapter_num, Verse.verse_num)
        .distinct()
        .order_by(Verse.book_id, Verse.chapter_num, Verse.verse_num)
    ).all()


# ---------------------------------------------------------------------------
# External source DB reads (raw sqlite3, third-party schema)
# ---------------------------------------------------------------------------


def read_sqlite_translation(path: Path) -> tuple[dict, list[tuple]]:
    """Read meta and verses from an external Bible SQLite source file.

    The source files use a fixed third-party schema with:
      - meta(field TEXT, value TEXT)
      - verses(book INTEGER, chapter INTEGER, verse INTEGER, text TEXT, ...)

    Returns:
        (meta, verse_rows) where meta is {field: value} and verse_rows
        is a list of (book, chapter, verse, text) tuples.
    """
    conn = sqlite3.connect(path)
    try:
        cur = conn.cursor()
        cur.execute("SELECT field, value FROM meta;")
        meta = dict(cur.fetchall())

        cur.execute("SELECT book, chapter, verse, text FROM verses;")
        verse_rows = cur.fetchall()
    finally:
        conn.close()
    return meta, verse_rows
