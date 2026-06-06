from __future__ import annotations

import html
import re
from pathlib import Path

from sqlmodel import Session, select

from src.database import DB_ENGINE, Book, Translation, Verse
from src.constants import ROOT_PATH


OUTPUT_PATH = ROOT_PATH / "output"


def write_obsidian_markdown(output_path: Path = OUTPUT_PATH) -> None:
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
                "book_order": book.canonical_order,
                "chapter": verse.chapter_num,
                "verse": verse.verse_num,
                "translations": [],
            }

        grouped_verses[key]["translations"].append(
            {
                "abbreviation": translation.abbreviation,
                "text": _clean_text(verse.text),
            }
        )

    for grouped in grouped_verses.values():
        book_name = grouped["book_name"]
        chapter = grouped["chapter"]
        verse_num = grouped["verse"]
        reference = f"{book_name} {chapter}:{verse_num}"

        chapter_dir = output_path / book_name / str(chapter)
        chapter_dir.mkdir(parents=True, exist_ok=True)

        file_path = chapter_dir / f"{book_name} {chapter}-{verse_num}.md"
        file_path.write_text(_render_markdown(grouped, reference), encoding="utf-8")

    print(f"Wrote {len(grouped_verses)} verse files to: {output_path}")


def _clean_text(text: str) -> str:
    cleaned = text.replace("<br/>", "\n").replace("<br>", "\n")
    cleaned = re.sub(r"<[^>]+>", "", cleaned)
    cleaned = html.unescape(cleaned)
    return cleaned.strip()


def _yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _render_markdown(grouped: dict, reference: str) -> str:
    translations = grouped["translations"]
    translation_list = ", ".join(item["abbreviation"] for item in translations)

    lines = [
        "---",
        f"reference: {_yaml_quote(reference)}",
        f"book: {_yaml_quote(grouped['book_name'])}",
        f"book_order: {grouped['book_order']}",
        f"chapter: {grouped['chapter']}",
        f"verse: {grouped['verse']}",
        f"translations: [{translation_list}]",
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
