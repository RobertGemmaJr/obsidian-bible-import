import uuid
import json

from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint
from typing import Optional


class Translation(SQLModel, table=True):
    """Represents a complete translation of the Bible."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    abbreviation: str = Field(index=True, unique=True)
    name: str = Field(index=True, unique=True)

    # Relations
    verses: list["Verse"] = Relationship(back_populates="translation")


class Book(SQLModel, table=True):
    """Represents a Bible book record."""

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
