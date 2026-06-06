from src.database import reset_db
from src.readers import read_bible_books, read_esv_bible, read_niv_bible
from src.writer import write_obsidian_markdown


def main():
    reset_db()

    print("-------------------- READING SOURCE DATA --------------------")
    read_bible_books()
    read_esv_bible()
    read_niv_bible()
    write_obsidian_markdown()
    print("Done")


if __name__ == "__main__":
    main()
