from sqlmodel import Session, select
import sqlite3

from src.database import DB_ENGINE, Book, Translation, Verse
from src.common import BIBLES_PATH, to_bool, to_int


coverdale_bible = BIBLES_PATH / "bibles_sqlite_6" / "EN-English" / "coverdale.sqlite"


def read_coverdale_bible():
    print("Reading Coverdale Bible translation:", coverdale_bible)

    # Read the SQLite source
    conn = sqlite3.connect(coverdale_bible)
    try:
        cur = conn.cursor()
        cur.execute("SELECT field, value FROM meta;")
        meta = dict(cur.fetchall())

        cur.execute("SELECT book, chapter, verse, text FROM verses;")
        verse_rows = cur.fetchall()
    finally:
        conn.close()

    # Write to the database
    with Session(DB_ENGINE) as session:
        # Create the translation
        translation = Translation(
            abbreviation="Coverdale",
            name="Coverdale Bible",
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

        # Create the verses
        for book_id, chapter_num, verse_num, text in verse_rows:
            # Look up the related bible book
            book = session.exec(select(Book).where(Book.canonical_order == book_id)).one_or_none()

            if book is None:
                print(f"  Warning: No matching book for verse book={book_id} chapter={chapter_num} verse={verse_num}")
                continue

            # Add the row
            session.add(
                Verse(
                    chapter_num=chapter_num,
                    verse_num=verse_num,
                    text=text,
                    comment=None,
                    book_id=book.id,
                    translation_id=translation.id,
                )
            )
        session.commit()
