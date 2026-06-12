import uuid
import json

from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint
from typing import Optional


class Translation(SQLModel, table=True):
    """Represents a complete translation of the Bible."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    abbreviation: str = Field(index=True, unique=True)
    name: str = Field(index=True, unique=True)

    # Metadata (sourced from each translation's SQLite `meta` table where available)
    module: Optional[str] = Field(default=None)
    year: Optional[str] = Field(default=None)
    publisher: Optional[str] = Field(default=None)
    owner: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    lang: Optional[str] = Field(default=None)
    lang_short: Optional[str] = Field(default=None)
    copyright: Optional[bool] = Field(default=None)
    copyright_statement: Optional[str] = Field(default=None)
    url: Optional[str] = Field(default=None)
    citation_limit: Optional[int] = Field(default=None)
    restrict: Optional[bool] = Field(default=None)
    italics: Optional[bool] = Field(default=None)
    strongs: Optional[bool] = Field(default=None)
    red_letter: Optional[bool] = Field(default=None)
    paragraph: Optional[bool] = Field(default=None)
    official: Optional[bool] = Field(default=None)
    research: Optional[bool] = Field(default=None)
    module_version: Optional[str] = Field(default=None)

    # Relations
    verses: list["Verse"] = Relationship(back_populates="translation")


class Book(SQLModel, table=True):
    """Represents a single book of the Bible."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    canonical_order: int = Field(index=True, unique=True)
    chronological_order: int = Field(unique=True)
    name: str = Field(index=True, unique=True)
    short_name: str = Field(index=True, unique=True)
    num_chapters: int

    # Relations
    verses: list["Verse"] = Relationship(back_populates="book")

    # JSON
    matching_names: str = Field(default="[]")

    def get_matching_names(self) -> list[str]:
        """Return matching names as a list."""
        return json.loads(self.matching_names)

    def set_matching_names(self, names: list[str]):
        """Set matching names from a list."""
        self.matching_names = json.dumps(names)


class Verse(SQLModel, table=True):
    """Represents a single verse of the Bible."""

    __table_args__ = (
        # Each verse number is unique per translation
        UniqueConstraint("translation_id", "book_id", "chapter_num", "verse_num"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    chapter_num: int
    verse_num: int
    text: str = Field(index=True)
    comment: Optional[int]

    # Relations
    book_id: uuid.UUID = Field(default=None, foreign_key="book.id")
    book: Book = Relationship(back_populates="verses")
    translation_id: uuid.UUID = Field(default=None, foreign_key="translation.id")
    translation: Translation = Relationship(back_populates="verses")
