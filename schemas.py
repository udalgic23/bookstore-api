from pydantic import BaseModel
from datetime import date
from typing import Optional

class AuthorSchema(BaseModel):
    id: int
    name: str
    b_day: date

    class Config:
        orm_mode: True


class BookSchema(BaseModel):
    id: int
    title: str
    pub_date: date

    class Config:
        orm_mode: True


class GenreSchema(BaseModel):
    name: str
    parent_genre: Optional[str] = None

    class Config:
        orm_mode: True
