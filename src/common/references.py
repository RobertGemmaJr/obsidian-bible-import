"""Bible reference strings and alias generation."""

from __future__ import annotations

from typing import Optional


def book_ref(name: str) -> str:
    """Return a book reference string, e.g. ``"Genesis"``."""
    return name


def chapter_ref(name: str, chapter: int) -> str:
    """Return a chapter reference string, e.g. ``"Genesis 1"``."""
    return f"{name} {chapter}"


def verse_ref(name: str, chapter: int, verse: int) -> str:
    """Return a verse reference string, e.g. ``"Genesis 1:1"``."""
    return f"{name} {chapter}:{verse}"


def build_alias_names(
    name: str,
    short_name: Optional[str] = None,
    matching_names: Optional[list[str]] = None,
) -> list[str]:
    """Return a deduplicated, order-preserving list of book-name variants.

    The full ``name`` is always first, followed by ``short_name`` and then any
    ``matching_names`` (e.g. from ``Book.get_matching_names()``). Used as the
    base for book/chapter/verse alias generation.
    """
    candidates: list[str] = [name]
    if short_name:
        candidates.append(short_name)
    if matching_names:
        candidates.extend(matching_names)

    result: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        if not candidate or candidate in seen:
            continue
        seen.add(candidate)
        result.append(candidate)
    return result


def chapter_aliases(base_names: list[str], chapter: int) -> list[str]:
    """Return chapter alias references for each base name (e.g. ``"Gen 1"``)."""
    return [chapter_ref(name, chapter) for name in base_names]


def verse_aliases(base_names: list[str], chapter: int, verse: int) -> list[str]:
    """Return verse alias references for each base name (e.g. ``"Gen 1:1"``)."""
    return [verse_ref(name, chapter, verse) for name in base_names]
