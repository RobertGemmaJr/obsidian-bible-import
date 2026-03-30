from sqlmodel import Session, select
import json

from src.database import DB_ENGINE, Book, Translation, Verse
from src.constants import BIBLES_PATH


niv_bible = BIBLES_PATH / "NIV Bible.json"


def read_niv_bible():
    print("Reading NIV Bible translation:", niv_bible)

    # Read the JSON file
    with open(niv_bible, "r") as f:
        niv_bible_data = json.load(f)

    # Write to the database
    with Session(DB_ENGINE) as session:
        # Create the translation
        # TODO: Figure out and add the year to the translation?
        translation = Translation(abbreviation="NIV", name="New International Version")
        session.add(translation)
        session.flush()

        # Create the verses
        for verse in niv_bible_data:
            # Look up the related bible book
            book = session.exec(select(Book).where(Book.canonical_order == verse["book"])).one_or_none()

            if book is None:
                print(f"  Warning: No matching book for verse {verse['pk']}")
                continue

            # Add the row
            # TODO: The NIV bible includes the headings
            # TODO: e.g., "The Beginning<br/>In the beginning God created the heavens and the earth."
            # TODO: We should strip those from the data
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
