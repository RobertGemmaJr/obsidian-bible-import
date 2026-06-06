from sqlmodel import Session
import json

from src.database import DB_ENGINE, Translation, Verse, load_books_by_canonical_order
from src.common import BIBLES_PATH


niv_bible = BIBLES_PATH / "NIV Bible.json"


def read_niv_bible():
    print("Reading NIV Bible translation:", niv_bible)

    # Read the JSON file
    with open(niv_bible, "r") as f:
        niv_bible_data = json.load(f)

    # Write to the database
    with Session(DB_ENGINE) as session:
        # Create the translation
        translation = Translation(
            abbreviation="NIV",
            name="New International Version",
            year="1978",
            publisher="Biblica",
            lang="English",
            lang_short="en",
            copyright=True,
            copyright_statement=(
                "Scripture quotations taken from The Holy Bible, New International Version\u00ae NIV\u00ae "
                "Copyright \u00a9 1973, 1978, 1984, 2011 by Biblica, Inc.\u00ae"
            ),
            url="https://www.biblica.com/",
            official=True,
        )
        session.add(translation)
        session.flush()

        # Pre-load Book rows
        books_by_canonical_order = load_books_by_canonical_order(session)

        # Create the verses
        for verse in niv_bible_data:
            # Look up the related bible book
            book = books_by_canonical_order.get(verse["book"])

            if book is None:
                print(f"  Warning: No matching book for verse {verse['pk']}")
                continue

            # Add the row
            # TODO #9: The NIV bible includes the headings
            # TODO #9: e.g., "The Beginning<br/>In the beginning God created the heavens and the earth."
            # TODO #9: We should strip those from the data
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
