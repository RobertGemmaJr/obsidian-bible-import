"""Query helpers for the obsidian-bible-import database."""

from sqlmodel import Session, select

from .models import Book

__all__ = ["load_books_by_canonical_order"]


def load_books_by_canonical_order(session: Session) -> dict[int, Book]:
    """
    Return a dict mapping every Book's canonical_order (1-66) to its Book instance.

    Used by Bible readers to translate the source-format book id (which uses the
    same 1-66 canonical-order numbering) into a Book row in O(1) without issuing
    a SELECT per verse.
    """
    return {b.canonical_order: b for b in session.exec(select(Book)).all()}
