from pydantic import BaseModel
from datetime import date
from typing import Optional, List


class GenreSchema(BaseModel):
    name: str
    parent_genre: Optional[str] = None

    class Config:
        orm_mode: True

class BookSchema(BaseModel):
    id: int
    title: str
    pub_date: date

    class Config:
        orm_mode: True

class AuthorSchema(BaseModel):
    id: int
    name: str
    b_day: date
    books: List[BookSchema]

    class Config:
        orm_mode: True

class AuthorCreateSchema(BaseModel):
    name: str
    b_day: date
    books_ids: List[int] = []

    class Config:
        orm_mode: True

class BookDeepSchema(BaseModel):
    id: int
    title: str
    pub_date: date
    authors: List[AuthorSchema]
    genres: List[GenreSchema]

    class Config:
        orm_mode: True

class BookCreateSchema(BaseModel):
    title: str 
    pub_date: date
    author_ids: List[int] = []
    genre_names: List[str] = []

    class Config:
        orm_mode = True

class BookUpdateSchema(BaseModel):
    title: Optional[str] = None
    pub_date: Optional[date] = None
    author_ids: Optional[List[int]] = None
    genre_names: Optional[List[str]] = None

    class Config:
        orm_mode = True

class GenreBookSchema(BaseModel):
    id: int
    title: str
    pub_date: date
    genres: List[GenreSchema]

    class Config:
        orm_mode = True