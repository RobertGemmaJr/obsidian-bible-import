from src.database import reset_db
from src.readers import read_bible_books, read_esv_bible, read_niv_bible
from src.writers import write_translations, write_books, write_chapters, write_verses
from src.readers import (
    read_asv_bible,
    read_asvs_bible,
    read_bishops_bible,
    read_coverdale_bible,
    read_geneva_bible,
    read_kjv_bible,
    read_kjv_strongs_bible,
    read_net_bible,
    read_tyndale_bible,
    read_web_bible,
)


def main():
    reset_db()

    print("\n-------------------- READING SOURCE DATA --------------------\n")
    read_bible_books()
    read_esv_bible()
    read_niv_bible()
    read_web_bible()
    read_net_bible()
    read_asv_bible()
    read_asvs_bible()
    read_kjv_bible()
    read_kjv_strongs_bible()
    read_geneva_bible()
    read_bishops_bible()
    read_coverdale_bible()
    read_tyndale_bible()

    print("\n-------------------- WRITING TARGET DATA --------------------\n")
    write_translations()
    write_books()
    write_chapters()
    write_verses()

    print("\nDone")


if __name__ == "__main__":
    main()
