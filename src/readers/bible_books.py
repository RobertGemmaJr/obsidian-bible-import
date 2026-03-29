from sqlmodel import Session

from src.database import db_engine


def create_bible_books():
    with Session(db_engine) as session:
        print("Session!", session)
