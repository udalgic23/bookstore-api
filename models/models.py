from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.db import Base

author_book = Table(
    "author_book",
    Base.metadata,
    Column("author_id", Integer, ForeignKey("author.id"), primary_key=True),
    Column("book_id", Integer, ForeignKey("book.id"), primary_key=True)
)

book_genre = Table(
    "book_genre",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("book.id"), primary_key=True),
    Column("genre_name", String, ForeignKey("genre.name"), primary_key=True)
)

class Author(Base):

    __tablename__ = "author"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    b_day = Column(Date, nullable=False)

    books = relationship("Book", secondary=author_book, back_populates="authors")


class Book(Base):

    __tablename__ = "book"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    pub_date = Column(Date, nullable=False)

    authors = relationship("Author", secondary=author_book, back_populates="books")
    genres = relationship("Genre", secondary=book_genre, back_populates="books")
    


class Genre(Base):

    __tablename__ = "genre"

    name = Column(String, primary_key=True)
    parent_genre = Column(String, ForeignKey("genre.name"))


    books = relationship("Book", secondary=book_genre, back_populates="genres")
    subgenres = relationship("Genre", back_populates="parent", cascade="all, delete-orphan")
    parent = relationship("Genre", back_populates=subgenres, remote_side=[name])



