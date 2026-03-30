from src.database import reset_db
from src.readers import create_bible_books


def main():
    reset_db()

    print("-------------------- READING SOURCE DATA --------------------")
    create_bible_books()
    print("Done")


if __name__ == "__main__":
    main()
