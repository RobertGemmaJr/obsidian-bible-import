from __future__ import annotations

from pathlib import Path

from sqlmodel import Session, select

from src.common import (
    OUTPUT_PATH,
    SUPPORTED_TRANSLATIONS,
    clean_text,
    yaml_quote,
)
from src.database import DB_ENGINE, Book, Translation, Verse


verses_path = OUTPUT_PATH / "Bible Verses"


def write_verses(output_path: Path = verses_path) -> None:
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


def _build_aliases(grouped: dict) -> list[str]:
    """Build a deduplicated list of alias references for a verse.

    The first alias uses the full book name (e.g. "Genesis 1:1") and is also
    used as the H1 heading. Additional aliases are derived from the book's
    short name and any matching names (e.g. "Gen 1:1", "Gn 1:1").
    """
    chapter = grouped["chapter"]
    verse_num = grouped["verse"]

    name_candidates: list[str] = [grouped["book_name"], grouped["book_short_name"]]
    name_candidates.extend(grouped.get("book_matching_names") or [])

    aliases: list[str] = []
    seen: set[str] = set()
    for name in name_candidates:
        if not name:
            continue
        ref = f"{name} {chapter}:{verse_num}"
        if ref in seen:
            continue
        seen.add(ref)
        aliases.append(ref)

    return aliases


def _render_markdown(grouped: dict) -> str:
    order = {abbr: i for i, abbr in enumerate(SUPPORTED_TRANSLATIONS)}
    translations = sorted(
        grouped["translations"],
        key=lambda t: order.get(t["abbreviation"], len(order)),
    )

    aliases = _build_aliases(grouped)
    reference = aliases[0]

    lines = [
        "---",
        f"book: {yaml_quote(grouped['book_name'])}",
        f"book_order: {grouped['book_order']}",
        f"chapter: {grouped['chapter']}",
        f"verse: {grouped['verse']}",
        "aliases:",
    ]
    for alias in aliases:
        lines.append(f"  - {yaml_quote(alias)}")
    lines += ["translations:"]
    for item in translations:
        lines.append(f'  - "[[{item["abbreviation"]}]]"')
    lines += [
        "---",
        "",
        f"# {reference}",
        "",
    ]

    for item in translations:
        lines.append(f"## {item['abbreviation']}\n")
        lines.append(item["text"])
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"
