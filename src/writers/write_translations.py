from __future__ import annotations

from pathlib import Path

from sqlmodel import Session, select

from src.common import OUTPUT_PATH, SUPPORTED_TRANSLATIONS, format_field
from src.database import DB_ENGINE, Translation


translations_output = OUTPUT_PATH / "Bible Translations"

# Order matches the column definitions in src/database/models.py
_FIELDS: tuple[str, ...] = (
    "name",
    "abbreviation",
    "publisher",
    "year",
    "url",
    "copyright",
    "copyright_statement",
    "citation_limit",
    "module",
    "owner",
    "restrict",
    "italics",
    "strongs",
    "red_letter",
    "paragraph",
    "official",
    "research",
)


def write_translations(output_path: Path = translations_output) -> None:
    """Export one markdown file per Bible translation (frontmatter only)."""
    output_path.mkdir(parents=True, exist_ok=True)

    with Session(DB_ENGINE) as session:
        rows = session.exec(select(Translation)).all()

    order = {abbr: i for i, abbr in enumerate(SUPPORTED_TRANSLATIONS)}
    rows = sorted(rows, key=lambda t: order.get(t.abbreviation, len(order)))

    for translation in rows:
        file_path = output_path / f"{translation.abbreviation}.md"
        file_path.write_text(_render_markdown(translation), encoding="utf-8")

    print(f"Wrote {len(rows)} translation files to: {output_path}")


def _render_markdown(translation: Translation) -> str:
    lines = ["---"]
    for field in _FIELDS:
        lines.append(format_field(field, getattr(translation, field)))
    lines += ["---", "", f"# {translation.name}", ""]
    if translation.description:
        lines += [translation.description, ""]
    return "\n".join(lines).rstrip() + "\n"
