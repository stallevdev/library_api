from sqlalchemy import Column, String

from app.core.db import Base


class Reader(Base):
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
