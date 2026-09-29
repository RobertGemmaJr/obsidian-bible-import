import uuid
from pathlib import Path

from sqlalchemy import insert
from sqlmodel import Session

from src.database import DB_ENGINE, Translation, Verse, load_books_by_canonical_order
from src.common import BIBLES_PATH, read_json


# ---------------------------------------------------------------------------
# JSON Bible Reader
# ---------------------------------------------------------------------------


def read_json_bible(path: Path, **translation_kwargs) -> None:
    """Read a `Bibles/*.json` source file and write it as a Translation + Verses.

    Shared by every reader whose source is one of the standalone `*.json` bible files,
    since they all use the same shape: a list of {book, chapter, verse, text, comment,
    pk} dicts.
    """
    print(f"Reading {translation_kwargs.get('abbreviation')} Bible translation:", path)

    # Read the JSON file
    bible_data = read_json(path)

    # Write to the database
    with Session(DB_ENGINE) as session:
        # Create the translation
        translation = Translation(**translation_kwargs)
        session.add(translation)
        session.flush()

        # Pre-load Book rows
        books_by_canonical_order = load_books_by_canonical_order(session)

        # Build the verse rows
        verse_mappings = []
        for verse in bible_data:
            # Look up the related bible book
            book = books_by_canonical_order.get(verse["book"])

            if book is None:
                print(f"  Warning: No matching book for verse {verse['pk']}")
                continue

            verse_mappings.append(
                {
                    "id": uuid.uuid4(),
                    "chapter_num": verse.get("chapter"),
                    "verse_num": verse.get("verse"),
                    "text": verse.get("text"),
                    "comment": verse.get("comment"),
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


def read_esv_bible():
    read_json_bible(
        BIBLES_PATH / "ESV Bible.json",
        abbreviation="ESV",
        name="English Standard Version",
        year="2001",
        publisher="Crossway",
        lang="English",
        lang_short="en",
        copyright=True,
        copyright_statement=(
            "The ESV® Bible (The Holy Bible, English Standard Version®) "
            "copyright © 2001 by Crossway, a publishing ministry of Good News Publishers."
        ),
        url="https://www.esv.org/",
        official=True,
    )


def read_niv_bible():
    # TODO #9: The NIV bible includes the headings
    # TODO #9: e.g., "The Beginning<br/>In the beginning God created the heavens and the earth."
    # TODO #9: We should strip those from the data
    read_json_bible(
        BIBLES_PATH / "NIV Bible.json",
        abbreviation="NIV",
        name="New International Version",
        year="1978",
        publisher="Biblica",
        lang="English",
        lang_short="en",
        copyright=True,
        copyright_statement=(
            "Scripture quotations taken from The Holy Bible, New International Version® NIV® "
            "Copyright © 1973, 1978, 1984, 2011 by Biblica, Inc.®"
        ),
        url="https://www.biblica.com/",
        official=True,
    )
