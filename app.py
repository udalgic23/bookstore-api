from db import engine, Base, SessionLocal
from models import Author, Book, Genre, book_genre
from sqlalchemy import select

session = SessionLocal()

fantasy = session.query(Genre).filter_by(name="Historical Romance").first()

session.close()