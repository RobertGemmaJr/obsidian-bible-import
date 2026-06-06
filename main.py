from src.database import reset_db
from src.readers import (
    read_bible_books,
    read_esv_bible,
    read_niv_bible,
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

    print("-------------------- READING SOURCE DATA --------------------")
    read_bible_books()
    read_esv_bible()
    read_niv_bible()
    read_asv_bible()
    read_asvs_bible()
    read_bishops_bible()
    read_coverdale_bible()
    read_geneva_bible()
    read_kjv_bible()
    read_kjv_strongs_bible()
    read_net_bible()
    read_tyndale_bible()
    read_web_bible()
    print("Done")


if __name__ == "__main__":
    main()
