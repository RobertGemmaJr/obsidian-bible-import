import uuid
import json

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

import enum


class Translation(str, enum.Enum):
    """Supported bible translation"""

    ESV = "ESV"


class Book(SQLModel, table=True):
    """Represents a Bible book record."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    canonical_order: int
    chronological_order: int
    name: str = Field(index=True)
    short_name: str = Field(index=True)
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


class Verse:
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    translation: Translation
    chapter_num: int
    verse_num: int
    text: str = Field(index=True)
    comment: Optional[int]

    # Relations
    book_id: int = Field(default=None, foreign_key="book.id")
    book: Book = Relationship(back_populates="verses")
