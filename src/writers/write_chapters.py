from __future__ import annotations

import uuid
from pathlib import Path

from sqlmodel import Session

from src.common import (
    OUTPUT_PATH,
    book_ref,
    build_alias_names,
    bullet_link,
    bullet_links,
    chapter_aliases,
    chapter_ref,
    frontmatter,
    heading,
    render_note,
    section,
    verse_ref_link,
    yaml_link_field,
    yaml_link_list,
    yaml_list,
)
from src.database import (
    DB_ENGINE,
    Book,
    load_books_in_canonical_order,
    load_distinct_verse_coords,
)

CHAPTERS_OUTPUT_PATH = OUTPUT_PATH / "Bible Chapters"


def write_chapters(output_path: Path = CHAPTERS_OUTPUT_PATH) -> None:
    """Export one markdown file per chapter.

    Each note links back to its parent book and to every verse in the chapter.
    Verse coverage is the union across all translations.
    """
    output_path.mkdir(parents=True, exist_ok=True)

    with Session(DB_ENGINE) as session:
        books = load_books_in_canonical_order(session)
        verse_rows = load_distinct_verse_coords(session)

    verses_by_chapter: dict[tuple[uuid.UUID, int], list[int]] = {}
    for book_id, chapter_num, verse_num in verse_rows:
        verses_by_chapter.setdefault((book_id, chapter_num), []).append(verse_num)

    chapter_count = 0
    for book in books:
        book_dir = output_path / book.name
        book_dir.mkdir(parents=True, exist_ok=True)
        for chapter in range(1, book.num_chapters + 1):
            verse_nums = verses_by_chapter.get((book.id, chapter), [])
            file_path = book_dir / f"{book.name} {chapter}.md"
            file_path.write_text(_render_markdown(book, chapter, verse_nums), encoding="utf-8")
            chapter_count += 1

    print(f"Wrote {chapter_count} chapter files to: {output_path}")


def _render_markdown(book: Book, chapter: int, verse_nums: list[int]) -> str:
    base_names = build_alias_names(book.name, book.short_name, book.get_matching_names())
    aliases = chapter_aliases(base_names, chapter)
    verse_refs = [verse_ref_link(book.name, chapter, v) for v in verse_nums]

    return render_note([
        *frontmatter([
            yaml_link_field("book", book_ref(book.name)),
            f"book_order: {book.canonical_order}",
            f"chapter: {chapter}",
            f"num_verses: {len(verse_nums)}",
            *yaml_list("aliases", aliases),
            *yaml_link_list("verses", verse_refs),
        ]),
        "",
        heading(1, chapter_ref(book.name, chapter)),
        *section("Book", [bullet_link(book_ref(book.name))]),
        *section("Verses", bullet_links(verse_refs)),
    ])
