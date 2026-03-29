from sqlmodel import SQLModel, create_engine
from pathlib import Path

# File Paths
root_path = Path(__file__).parent.parent.absolute()
data_path = root_path / "data"

print(root_path)

# DB Engine
db_file = root_path / "obsidian-bible-import.db"
db_url = f"sqlite:///{db_file}"
db_engine = create_engine(db_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(db_engine)
