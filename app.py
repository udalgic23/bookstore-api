from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db import SessionLocal
from models import *
from schemas import *


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()


@app.get("/authors", response_model=List[AuthorSchema])
def get_authors(db: Session = Depends(get_db)):
    return db.query(Author).all()


@app.get("/books", response_model=List[BookSchema])
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()


@app.get("/genres", response_model=List[GenreSchema])
def get_books(db: Session = Depends(get_db)):
    return db.query(Genre).all()


@app.get("/authors/{author_id}/books", response_model=List[BookSchema])
def get_books_of_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author.books


