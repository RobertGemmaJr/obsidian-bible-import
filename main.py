from src.database import reset_db
from src.readers import read_bible_books, read_esv_bible


def main():
    reset_db()

    print("-------------------- READING SOURCE DATA --------------------")
    read_bible_books()
    read_esv_bible()
    print("Done")


if __name__ == "__main__":
    main()
