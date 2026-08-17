from sqlmodel import Session
import json

from src.database import DB_ENGINE, Book
from src.common import BIBLES_PATH, read_json

bible_books = BIBLES_PATH / "Bible Books.json"
books_en = BIBLES_PATH / "bibles_json_6" / "Extras" / "books_en.json"


# Prefix tokens that introduce a multi-word book name (e.g. "1 Sm", "First Samuel").
NAME_PREFIXES = frozenset({"1", "2", "3", "I", "II", "III", "1st", "2nd", "3rd", "First", "Second", "Third"})

# Connective tokens that bind a previous and following token into one entry
# (e.g. "Song of Songs", "Canticle of Canticles").
NAME_CONNECTIVES = frozenset({"of"})


def read_bible_books():
    print("Reading bible books file into the database:", bible_books)
    print("Reading bible books file into the database:", books_en)

    # Read the JSON files
    bible_books_data = read_json(bible_books)
    books_en_data = read_json(books_en)
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


def _split_matching_field(value: str | None) -> list[str]:
    """Parse a `matching1`-style space-separated names field into entries.

    Most entries are single tokens (e.g. "Gn", "Ezek"). Numeric/ordinal prefix
    tokens (e.g. "1", "I", "First", "1st") are combined with the following
    token to form a single entry (e.g. "1 Sm", "First Samuel"). The connective
    "of" is merged with its neighbours (e.g. "Song of Songs").
    """
    if not value:
        return []

    tokens = value.split()
    entries: list[str] = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token in NAME_PREFIXES and i + 1 < len(tokens):
            entries.append(f"{token} {tokens[i + 1]}")
            i += 2
        elif token in NAME_CONNECTIVES and entries and i + 1 < len(tokens):
            entries[-1] = f"{entries[-1]} {token} {tokens[i + 1]}"
            i += 2
        else:
            entries.append(token)
            i += 1
    return entries


def build_matching_names(book_en: dict) -> str:
    """Build a JSON array of all matching names for a book."""

    names: list[str] = []

    # `shortname` may itself contain a space (e.g. "1 Sam"); keep it as a single entry.
    shortname = book_en.get("shortname")
    if shortname:
        names.append(shortname)

    # `matching1` is a space-separated list where individual entries may also contain spaces.
    names.extend(_split_matching_field(book_en.get("matching1")))

    # `matching2` is always a single (possibly multi-word) entry; do not split it.
    matching2 = book_en.get("matching2")
    if matching2:
        names.append(matching2)

    return json.dumps(names)
