from __future__ import annotations

from pathlib import Path

from sqlmodel import Session, select

from src.common import (
    OUTPUT_PATH,
    TRANSLATION_ORDER,
    build_alias_names,
    clean_text,
    format_field,
    frontmatter,
    heading,
    render_note,
    verse_aliases,
    yaml_link_list,
    yaml_list,
)
from src.database import DB_ENGINE, Book, Translation, Verse


VERSES_OUTPUT_PATH = OUTPUT_PATH / "Bible Verses"


def write_verses(output_path: Path = VERSES_OUTPUT_PATH) -> None:
    """Export one markdown file per verse with all translations included."""
    output_path.mkdir(parents=True, exist_ok=True)

    with Session(DB_ENGINE) as session:
        statement = (
            select(Verse, Book, Translation)
            .join(Book, Verse.book_id == Book.id)
            .join(Translation, Verse.translation_id == Translation.id)
            .order_by(Book.canonical_order, Verse.chapter_num, Verse.verse_num, Translation.abbreviation)
        )
        rows = session.exec(statement).all()

    grouped_verses: dict[tuple[int, int, int], dict] = {}

    for verse, book, translation in rows:
        key = (book.canonical_order, verse.chapter_num, verse.verse_num)
        if key not in grouped_verses:
            grouped_verses[key] = {
                "book_name": book.name,
                "book_short_name": book.short_name,
                "book_matching_names": book.get_matching_names(),
                "book_order": book.canonical_order,
                "chapter": verse.chapter_num,
                "verse": verse.verse_num,
                "translations": [],
            }

        grouped_verses[key]["translations"].append(
            {
                "abbreviation": translation.abbreviation,
                "text": clean_text(verse.text),
            }
        )

    for grouped in grouped_verses.values():
        book_name = grouped["book_name"]
        chapter = grouped["chapter"]
        verse_num = grouped["verse"]

        chapter_dir = output_path / book_name / str(chapter)
        chapter_dir.mkdir(parents=True, exist_ok=True)

        file_path = chapter_dir / f"{book_name} {chapter}-{verse_num}.md"
        file_path.write_text(_render_markdown(grouped), encoding="utf-8")

    print(f"Wrote {len(grouped_verses)} verse files to: {output_path}")


def _render_markdown(grouped: dict) -> str:
    translations = sorted(
        grouped["translations"],
        key=lambda t: TRANSLATION_ORDER.get(t["abbreviation"], len(TRANSLATION_ORDER)),
    )
    base_names = build_alias_names(
        grouped["book_name"],
        grouped["book_short_name"],
        grouped["book_matching_names"],
    )
    aliases = verse_aliases(base_names, grouped["chapter"], grouped["verse"])

    return render_note(
        [
            *frontmatter(
                [
                    *yaml_list("aliases", aliases),
                    format_field("book", grouped["book_name"]),
                    f"book_order: {grouped['book_order']}",
                    f"chapter: {grouped['chapter']}",
                    f"verse: {grouped['verse']}",
                    *yaml_link_list("translations", [t["abbreviation"] for t in translations]),
                ]
            ),
            "",
            heading(1, aliases[0]),
            "",
            *_render_translation_sections(translations),
        ]
    )


def _render_translation_sections(translations: list[dict]) -> list[str]:
    """Render each translation as an H2 followed by its verse text."""
    lines: list[str] = []
    for item in translations:
        lines.append(heading(2, item["abbreviation"]))
        lines.append("")
        lines.append(item["text"])
        lines.append("")
    return lines
