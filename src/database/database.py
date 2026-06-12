import os

from sqlmodel import SQLModel, create_engine
from ..common import DATA_PATH

# DB Engine
DB_FILE = DATA_PATH / "obsidian-bible-import.db"
DB_ENGINE = create_engine(f"sqlite:///{DB_FILE}")


def create_db_and_tables():
    print("Initialized database")
    SQLModel.metadata.create_all(DB_ENGINE)
    print("Database initialized")


def delete_db():
    """Delete the database file if it exists."""
    if DB_FILE.exists():
        os.remove(DB_FILE)
        print(f"Deleted database: {DB_FILE}")
    else:
        print("No database found to delete.")


def reset_db():
    """Delete and recreate the database."""
    delete_db()
    create_db_and_tables()
    print("Database reset complete.")
