from sqlmodel import Session

from src.database import DB_ENGINE, Translation, Verse, load_books_by_canonical_order
from src.common import BIBLES_PATH, read_json

esv_bible = BIBLES_PATH / "ESV Bible.json"


def read_esv_bible():
    print("Reading ESV Bible translation:", esv_bible)

    # Read the JSON file
    esv_bible_data = read_json(esv_bible)

    # Write to the database
    with Session(DB_ENGINE) as session:
        # Create the translation
        translation = Translation(
            abbreviation="ESV",
            name="English Standard Version",
            year="2001",
            publisher="Crossway",
            lang="English",
            lang_short="en",
            copyright=True,
            copyright_statement=(
                "The ESV\u00ae Bible (The Holy Bible, English Standard Version\u00ae) "
                "copyright \u00a9 2001 by Crossway, a publishing ministry of Good News Publishers."
            ),
            url="https://www.esv.org/",
            official=True,
        )
        session.add(translation)
        session.flush()

        # Pre-load Book rows
        books_by_canonical_order = load_books_by_canonical_order(session)

        # Create the verses
        for verse in esv_bible_data:
            # Look up the related bible book
            book = books_by_canonical_order.get(verse["book"])

            if book is None:
                print(f"  Warning: No matching book for verse {verse['pk']}")
                continue

            # Add the row
            session.add(
                Verse(
                    chapter_num=verse.get("chapter"),
                    verse_num=verse.get("verse"),
                    text=verse.get("text"),
                    comment=verse.get("comment"),
                    book_id=book.id,
                    translation_id=translation.id,
                )
            )
        session.commit()
