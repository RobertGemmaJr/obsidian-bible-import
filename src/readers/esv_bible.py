from sqlmodel import Session, select
import json

from src.database import DB_ENGINE, Book, Translation, Verse
from src.constants import BIBLES_PATH

esv_bible = BIBLES_PATH / "ESV Bible.json"


def read_esv_bible():
    print("Reading ESV Bible translation:", esv_bible)

    # Read the JSON file
    with open(esv_bible, "r") as f:
        esv_bible_data = json.load(f)

    # Write to the database
    with Session(DB_ENGINE) as session:
        # Create the translation
        translation = Translation(abbreviation="ESV", name="English Standard Version")
        session.add(translation)
        session.flush()

        # Create the verses
        for verse in esv_bible_data:
            # Look up the related bible book
            book = session.exec(select(Book).where(Book.canonical_order == verse["book"])).one_or_none()

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
