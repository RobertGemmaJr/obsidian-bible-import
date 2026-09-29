import uuid
from pathlib import Path

from sqlalchemy import insert
from sqlmodel import Session

from src.database import DB_ENGINE, Translation, Verse, load_books_by_canonical_order, read_sqlite_translation
from src.common import BIBLES_PATH, to_bool, to_int

_SQLITE_DIR = BIBLES_PATH / "bibles_sqlite_6" / "EN-English"


# ---------------------------------------------------------------------------
# SQLite Bible Reader
# ---------------------------------------------------------------------------


def read_sqlite_bible(path: Path, *, abbreviation: str, name: str) -> None:
    """Read a third-party sqlite Bible source file and write it as a Translation + Verses.

    Shared by every reader whose source is one of the `bibles_sqlite_6` files, since
    they all use the same third-party schema (see `read_sqlite_translation`).
    """
    print(f"Reading {abbreviation} Bible translation:", path)

    # Read the SQLite source
    meta, verse_rows = read_sqlite_translation(path)

    # Write to the database
    with Session(DB_ENGINE) as session:
        # Create the translation
        translation = Translation(
            abbreviation=abbreviation,
            name=name,
            module=meta.get("module"),
            year=meta.get("year"),
            publisher=meta.get("publisher"),
            owner=meta.get("owner"),
            description=meta.get("description"),
            lang=meta.get("lang"),
            lang_short=meta.get("lang_short"),
            copyright=to_bool(meta.get("copyright")),
            copyright_statement=meta.get("copyright_statement"),
            url=meta.get("url"),
            citation_limit=to_int(meta.get("citation_limit")),
            restrict=to_bool(meta.get("restrict")),
            italics=to_bool(meta.get("italics")),
            strongs=to_bool(meta.get("strongs")),
            red_letter=to_bool(meta.get("red_letter")),
            paragraph=to_bool(meta.get("paragraph")),
            official=to_bool(meta.get("official")),
            research=to_bool(meta.get("research")),
            module_version=meta.get("module_version"),
        )
        session.add(translation)
        session.flush()

        # Pre-load Book rows
        books_by_canonical_order = load_books_by_canonical_order(session)

        # Build the verse rows
        verse_mappings = []
        for book_id, chapter_num, verse_num, text in verse_rows:
            # Look up the related bible book
            book = books_by_canonical_order.get(book_id)

            if book is None:
                print(f"  Warning: No matching book for verse book={book_id} chapter={chapter_num} verse={verse_num}")
                continue

            verse_mappings.append(
                {
                    "id": uuid.uuid4(),
                    "chapter_num": chapter_num,
                    "verse_num": verse_num,
                    "text": text,
                    "comment": None,
                    "book_id": book.id,
                    "translation_id": translation.id,
                }
            )

        # Bulk insert the verses
        session.exec(insert(Verse), params=verse_mappings)
        session.commit()


# ---------------------------------------------------------------------------
# Methods for reading each Bible translation
# ---------------------------------------------------------------------------


def read_asv_bible():
    read_sqlite_bible(_SQLITE_DIR / "asv.sqlite", abbreviation="ASV", name="American Standard Version")


def read_asvs_bible():
    read_sqlite_bible(_SQLITE_DIR / "asvs.sqlite", abbreviation="ASVs", name="American Standard Version w Strong's")


def read_bishops_bible():
    read_sqlite_bible(_SQLITE_DIR / "bishops.sqlite", abbreviation="Bishops", name="Bishops Bible")


def read_coverdale_bible():
    read_sqlite_bible(_SQLITE_DIR / "coverdale.sqlite", abbreviation="Coverdale", name="Coverdale Bible")


def read_geneva_bible():
    read_sqlite_bible(_SQLITE_DIR / "geneva.sqlite", abbreviation="Geneva", name="Geneva Bible")


def read_kjv_bible():
    read_sqlite_bible(_SQLITE_DIR / "kjv.sqlite", abbreviation="KJV", name="Authorized King James Version")


def read_kjv_strongs_bible():
    read_sqlite_bible(_SQLITE_DIR / "kjv_strongs.sqlite", abbreviation="KJV Strongs", name="KJV with Strongs")


def read_net_bible():
    read_sqlite_bible(_SQLITE_DIR / "net.sqlite", abbreviation="NET", name="NET Bible®")


def read_tyndale_bible():
    read_sqlite_bible(_SQLITE_DIR / "tyndale.sqlite", abbreviation="Tyndale", name="Tyndale Bible")


def read_web_bible():
    read_sqlite_bible(_SQLITE_DIR / "web.sqlite", abbreviation="WEB", name="World English Bible")
