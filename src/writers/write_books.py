from __future__ import annotations

import uuid
from pathlib import Path

from sqlmodel import Session

from src.common import (
    OUTPUT_PATH,
    build_alias_names,
    bullet_links,
    chapter_ref,
    frontmatter,
    heading,
    render_note,
    section,
    verse_ref,
    yaml_link_list,
    yaml_list,
)
from src.database import (
    DB_ENGINE,
    Book,
    load_books_in_canonical_order,
    load_distinct_verse_coords,
)

BOOKS_OUTPUT_PATH = OUTPUT_PATH / "Bible Books"


def write_books(output_path: Path = BOOKS_OUTPUT_PATH) -> None:
    """Export one markdown file per book.

    Each note links to its chapters and to every verse in the book. Verse
    coverage is the union across all translations.
    """
    output_path.mkdir(parents=True, exist_ok=True)

    with Session(DB_ENGINE) as session:
        books = load_books_in_canonical_order(session)
        verse_rows = load_distinct_verse_coords(session)

    verses_by_book: dict[uuid.UUID, list[tuple[int, int]]] = {}
    for book_id, chapter_num, verse_num in verse_rows:
        verses_by_book.setdefault(book_id, []).append((chapter_num, verse_num))

    for book in books:
        verses = verses_by_book.get(book.id, [])
        file_path = output_path / f"{book.name}.md"
        file_path.write_text(_render_markdown(book, verses), encoding="utf-8")

    print(f"Wrote {len(books)} book files to: {output_path}")


def _render_markdown(book: Book, verses: list[tuple[int, int]]) -> str:
    base_names = build_alias_names(book.name, book.short_name, book.get_matching_names())
    chapter_refs = [chapter_ref(book.name, ch) for ch in range(1, book.num_chapters + 1)]
    verse_refs = [verse_ref(book.name, ch, v) for ch, v in verses]

    return render_note([
        *frontmatter([
            *yaml_list("aliases", base_names),
            f"book_order: {book.canonical_order}",
            f"num_chapters: {book.num_chapters}",
            *yaml_link_list("chapters", chapter_refs),
            *yaml_link_list("verses", verse_refs),
        ]),
        "",
        heading(1, book.name),
        *section("Chapters", bullet_links(chapter_refs)),
        *section("Verses", bullet_links(verse_refs)),
    ])
