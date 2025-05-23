from sqlalchemy import Column, String

from app.core.db import Base


class User(Base):
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
