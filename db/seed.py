from db.db import engine, Base, SessionLocal
from models.models import Author, Book, Genre

Base.metadata.create_all(bind=engine)

session = SessionLocal()



session.close()