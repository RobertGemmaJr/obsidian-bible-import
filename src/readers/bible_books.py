from sqlmodel import Session
import json

from src.database import DB_ENGINE, Book
from src.constants import BIBLES_PATH

bible_books = BIBLES_PATH / "Bible Books.json"
books_en = BIBLES_PATH / "bibles_json_6" / "Extras" / "books_en.json"


def create_bible_books():
    # Read the JSON file
    with open(bible_books, "r") as f:
        bible_books_data = json.load(f)
    with open(books_en, "r") as f:
        books_en_data = json.load(f)
        books_en_lookup = {book["id"]: book for book in books_en_data}
        print(books_en_lookup)

    # Write to the database
    with Session(DB_ENGINE) as session:
        print("Reading bible books file into the database:", bible_books)
        for book in bible_books_data:
            # Look up the json objects based on the base ID
            book_id = book["bookid"]
            book_en = books_en_lookup.get(book_id)

            if book_en is None:
                print(f"  Warning: ID Mismatch: {book_id}")
                continue
            print("Adding book:", book["name"])

            session.add(
                Book(
                    canonical_order=book_id,
                    chronological_order=book["chronorder"],
                    name=book["name"],
                    num_chapters=book["chapters"],
                    short_name=book_en["shortname"],
                    matching_names=build_matching_names(book_en),
                )
            )
        session.commit()


def build_matching_names(book_en: dict) -> str:
    """Build a JSON array of all matching names for a book."""

    # NOTE @RobertGemmaJr: Some of these fields are separated by space
    # NOTE @RobertGemmaJr: We flatten all possible matches into a single string array
    names = []
    if book_en["shortname"]:
        names.extend(book_en["shortname"].split(" "))
    if book_en["matching1"]:
        names.extend(book_en["matching1"].split(" "))
    if book_en["matching2"]:
        names.extend(book_en["matching2"].split(" "))

    return json.dumps(names)
