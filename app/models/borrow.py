from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.sql import func

from app.core.db import Base


class Borrow(Base):
    book_id = Column(Integer, ForeignKey('book.id'), nullable=False)
    reader_id = Column(Integer, ForeignKey('reader.id'), nullable=False)
    borrow_date = Column(DateTime, server_default=func.now())
    return_date = Column(DateTime)
