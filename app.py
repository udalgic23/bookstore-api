from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
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
def get_genres(db: Session = Depends(get_db)):
    return db.query(Genre).all()


@app.get("/authors/{author_id}/books", response_model=List[BookSchema])
def get_books_of_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author.books

@app.post("/authors", response_model=AuthorSchema)
def create_author(author: AuthorCreateSchema, db: Session = Depends(get_db)):
    new_author = Author(name=author.name, b_day=author.b_day)
    if author.books_ids:
        books = db.query(Book).filter(Book.id.in_(author.books_ids)).all()
        if len(books) != len(author.books_ids):
            raise HTTPException(status_code=404, detail="One or more books not found")
        new_author.books = books
    
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author

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

@app.put("/books/{book_id}", response_model=BookDeepSchema)
def update_book(book_id: int, book: BookUpdateSchema, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book.title is not None:
        db_book.title = book.title

    if book.pub_date is not None:
        db_book.pub_date = book.pub_date

    if book.author_ids is not None:
        authors = db.query(Author).filter(Author.id.in_(book.author_ids)).all()
        if len(authors) != len(book.author_ids):
            raise HTTPException(status_code=404, detail="One or more authors not found")
        db_book.authors = authors

    if book.genre_names is not None:
        genres = db.query(Genre).filter(Genre.name.in_(book.genre_names)).all()
        if len(genres) != len(book.genre_names):
            raise HTTPException(status_code=404, detail="One or more genres not found")
        db_book.genres = genres

    db.commit()
    db.refresh(db_book)
    return db_book

@app.put("/genres/{genre_name}", response_model=List[BookSchema])
def add_book_to_genre(genre_name: str, books_to_add: List[int], db: Session = Depends(get_db)):
    books = db.query(Book).filter(Book.id.in_(books_to_add)).all()
    genre = db.query(Genre).filter(Genre.name == genre_name).first()
    
    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")

    if len(books) != len(books_to_add):
        raise HTTPException(status_code=404, detail="One or more books not found")
    
    genre.books.extend(books)
    db.commit()
    db.refresh(genre)
    return books

@app.put("/books/{book_id}/authors", response_model=BookDeepSchema)
def add_authors_to_book(book_id: int, authors_list: List[int], db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    authors = db.query(Author).filter(Author.id.in_(authors_list)).all()
    if len(authors) != len(authors_list):
        raise HTTPException(status_code=404, detail="One or more authors not found")
    
    book.authors.extend(authors)
    db.commit()
    db.refresh(book)
    return book

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book does not exist")

    db.delete(book)
    db.commit()
    return {"message": f"Book {book_id} has been deleted"}

@app.get("/genre/{genre_name}", response_model=List[GenreBookSchema])
def all_books_of_genre(genre_name: str, db: Session = Depends(get_db)):
    genre = db.query(Genre).filter(Genre.name == genre_name).first()
    if genre is None:
        raise HTTPException(status_code=404, detail="Genre does not exist")
    
    base = select(Genre.name, Genre.parent_genre).where(Genre.name == genre.name)
    genre_cte = base.cte(name="genre_cte", recursive=True)

    genre_alias = Genre.__table__.alias()
    recursive = (
        select(genre_alias.c.name, genre_alias.c.parent_genre)
        .join(genre_cte, genre_alias.c.parent_genre == genre_cte.c.name)
    )

    genre_cte = genre_cte.union_all(recursive)

    stmt = (
        select(Book)
        .join(book_genre, book_genre.c.book_id == Book.id)
        .join(Genre, Genre.name == book_genre.c.genre_name)
        .join(genre_cte, genre_cte.c.name == Genre.name)
        .distinct()
    )

    books = db.scalars(stmt).all()
    return books



@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def catch_all(path_name: str):
    return JSONResponse(
        status_code=404,
        content={"detail": f"Endpoint '/{path_name}' not found"}
    )

