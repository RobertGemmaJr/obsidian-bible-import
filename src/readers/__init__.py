"""
Package for reading source data into the sqlite database.
"""

from .bible_books import read_bible_books
from .esv_bible import read_esv_bible
from .niv_bible import read_niv_bible
from .asv_bible import read_asv_bible
from .asvs_bible import read_asvs_bible
from .bishops_bible import read_bishops_bible
from .coverdale_bible import read_coverdale_bible
from .geneva_bible import read_geneva_bible
from .kjv_bible import read_kjv_bible
from .kjv_strongs_bible import read_kjv_strongs_bible
from .net_bible import read_net_bible
from .tyndale_bible import read_tyndale_bible
from .web_bible import read_web_bible

__all__ = [
    "read_bible_books",
    "read_esv_bible",
    "read_niv_bible",
    "read_asv_bible",
    "read_asvs_bible",
    "read_bishops_bible",
    "read_coverdale_bible",
    "read_geneva_bible",
    "read_kjv_bible",
    "read_kjv_strongs_bible",
    "read_net_bible",
    "read_tyndale_bible",
    "read_web_bible",
]
