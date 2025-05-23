from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class BorrowBase(BaseModel):
    book_id: int
    reader_id: int


class BorrowCreate(BorrowBase):
    pass


class BorrowReturn(BaseModel):
    borrow_id: int


class BorrowUpdate(BaseModel):
    return_date: Optional[datetime] = Field(None)


class BorrowInDBBase(BorrowBase):
    id: int
    borrow_date: datetime
    return_date: Optional[datetime] = None

    class Config:
        orm_mode = True


class Borrow(BorrowInDBBase):
    pass


class ReaderBorrows(BaseModel):
    active_borrows: List[Borrow]
    returned_borrows: List[Borrow]
