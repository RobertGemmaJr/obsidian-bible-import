from sqlmodel import Session
import json


from src.database import DB_ENGINE, Book
from src.constants import BIBLES_PATH

bible_books = BIBLES_PATH / "Bible Books.json"
books_en = BIBLES_PATH / "bibles_json_6" / "Extras" / "books_en.json"


def create_bible_books():
    # Read the JSON file
    with open(bible_books, "r") as file:
        bible_books_data = json.load(file)
    # with open(books_en, "r") as file:
    #     books_en_data = json.load(file)

    # Write to the database
    with Session(DB_ENGINE) as session:
        print("Reading bible books file into the database:", bible_books)
        for book in bible_books_data:
            print("Adding book:", book["name"])
            session.add(
                Book(
                    canonical_order=book["bookid"],
                    chronological_order=book["chronorder"],
                    name=book["name"],
                    num_chapters=book["chapters"],
                    short_name="",
                )
            )
        session.commit()
