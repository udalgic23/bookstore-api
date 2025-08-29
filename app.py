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


@app.get("/books/{book_id}", response_model=BookDeepSchema)
def get_book_information(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books", response_model=BookDeepSchema)
def create_book(book: BookCreateSchema, db : Session = Depends(get_db)):
    new_book = Book(title=book.title, pub_date=book.pub_date)

    if book.author_ids:
        authors = db.query(Author).filter(Author.id.in_(book.author_ids)).all()
        if len(authors) != len(book.author_ids):
            raise HTTPException(status_code=404, detail="One or more authors not found")
        new_book.authors = authors

    if book.genre_names:
        genres = db.query(Genre).filter(Genre.name.in_(book.genre_names)).all()
        if len(genres) != len(book.genre_names):
            raise HTTPException(status_code=404, detail="One or more genres not found")
        new_book.genres = genres

    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book