"""Bible reference strings and alias generation."""

from __future__ import annotations

from typing import Optional


def book_ref(name: str) -> str:
    """Return a book reference string, e.g. ``"Genesis"``."""
    return name


def chapter_ref(name: str, chapter: int) -> str:
    """Return a chapter reference string, e.g. ``"Genesis 1"``."""
    return f"{name} {chapter}"


def verse_ref_alias(name: str, chapter: int, verse: int) -> str:
    """Return the human-readable verse reference, e.g. ``"Genesis 1:1"``.

    Suitable for headings, YAML ``aliases:`` entries, and the right-hand
    (display) side of a piped wikilink.
    """
    return f"{name} {chapter}:{verse}"


def verse_ref_file(name: str, chapter: int, verse: int) -> str:
    """Return the file-safe verse reference, e.g. ``"Genesis 1-1"``.

    Matches the on-disk filename written by ``write_verses`` and is suitable
    as the left-hand (target) side of a piped wikilink.
    """
    return f"{name} {chapter}-{verse}"


def verse_ref_link(name: str, chapter: int, verse: int) -> str:
    """Return the piped wikilink-target form, e.g. ``"Genesis 1-1|Genesis 1:1"``.

    When wrapped by ``wikilink()`` (or any helper that calls it) the result
    is ``[[Genesis 1-1|Genesis 1:1]]`` -- an Obsidian link whose target is
    the actual file name and whose display text is the human-readable
    reference.
    """
    return f"{verse_ref_file(name, chapter, verse)}|{verse_ref_alias(name, chapter, verse)}"


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
    return [verse_ref_alias(name, chapter, verse) for name in base_names]
