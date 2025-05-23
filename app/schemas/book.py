from typing import Optional

from pydantic import BaseModel, Field


class BookBase(BaseModel):
    title: str
    author: str
    year: Optional[int] = None
    isbn: Optional[str] = None
    quantity: int = Field(default=1, ge=0)
    description: Optional[str] = Field(None, max_length=1000)


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True
