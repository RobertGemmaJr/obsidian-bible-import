import uuid
import json

from sqlmodel import SQLModel, Field


class Book(SQLModel, table=True):
    """Represents a Bible book record."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    canonical_order: int
    chronological_order: int
    name: str = Field(index=True)
    short_name: str = Field(index=True)
    num_chapters: int
    matching_names: str = Field(default="[]")

    def get_matching_names(self) -> list[str]:
        """Return matching names as a list."""
        return json.loads(self.matching_names)

    def set_matching_names(self, names: list[str]):
        """Set matching names from a list."""
        self.matching_names = json.dumps(names)
