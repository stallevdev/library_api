from sqlalchemy import Column, Integer, String

from app.core.db import Base


class Book(Base):
    title = Column(String, index=True, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer)
    isbn = Column(String, unique=True)
    quantity = Column(Integer, nullable=False, default=1)
    description = Column(String)
