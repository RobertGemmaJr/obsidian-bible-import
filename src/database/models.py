import uuid

from sqlmodel import SQLModel, Field


class Book(SQLModel, table=True):
    """Represents a Bible book record."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    canonical_order: int
    chronological_order: int
    name: str = Field(index=True)
    chapters: int
