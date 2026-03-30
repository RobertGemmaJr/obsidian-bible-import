from sqlmodel import Session
import json

from src.database import DB_ENGINE, Book
from src.constants import BIBLES_PATH

bible_books = BIBLES_PATH / "Bible Books.json"
books_en = BIBLES_PATH / "bibles_json_6" / "Extras" / "books_en.json"


def read_bible_books():
    print("Reading bible books file into the database:", bible_books)
    print("Reading bible books file into the database:", books_en)

    # Read the JSON file
    with open(bible_books, "r") as f:
        bible_books_data = json.load(f)
    with open(books_en, "r") as f:
        books_en_data = json.load(f)
        books_en_lookup = {book["id"]: book for book in books_en_data}

    # Write to the database
    with Session(DB_ENGINE) as session:
        for book in bible_books_data:
            # Look up the json objects based on the base ID
            book_id = book["bookid"]
            book_en = books_en_lookup.get(book_id)

            if book_en is None:
                print(f"  Warning: ID Mismatch: {book_id}")
                continue

            # Add the row
            session.add(
                Book(
                    canonical_order=book_id,
                    chronological_order=book.get("chronorder"),
                    name=book.get("name"),
                    num_chapters=book.get("chapters"),
                    short_name=book_en.get("shortname"),
                    matching_names=build_matching_names(book_en),
                )
            )
        session.commit()


def build_matching_names(book_en: dict) -> str:
    """Build a JSON array of all matching names for a book."""

    # NOTE @RobertGemmaJr: Some of these fields are separated by space
    # NOTE @RobertGemmaJr: We flatten all possible matches into a single string array
    names = []
    names.extend((book_en.get("shortname") or "").split())
    names.extend((book_en.get("matching1") or "").split())
    names.extend((book_en.get("matching2") or "").split())

    return json.dumps(names)
