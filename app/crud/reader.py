from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.reader import Reader
from app.schemas.reader import ReaderCreate, ReaderUpdate


def get_reader(db: Session, reader_id: int) -> Optional[Reader]:
    return db.query(Reader).filter(Reader.id == reader_id).first()


def get_reader_by_email(db: Session, email: str) -> Optional[Reader]:
    return db.query(Reader).filter(Reader.email == email).first()


def get_readers(db: Session, skip: int = 0, limit: int = 100) -> List[Reader]:
    return db.query(Reader).offset(skip).limit(limit).all()


def create_reader(db: Session, reader: ReaderCreate) -> Reader:
    if get_reader_by_email(db, email=reader.email):
        raise ValueError("Читатель с этим электронным письмом уже существует")

    db_reader = Reader(name=reader.name, email=reader.email)
    db.add(db_reader)
    db.commit()
    db.refresh(db_reader)
    return db_reader


def update_reader(
    db: Session, reader_id: int, reader: ReaderUpdate
) -> Optional[Reader]:
    db_reader = get_reader(db, reader_id=reader_id)
    if db_reader:
        update_data = reader.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_reader, field, value)
        db.commit()
        db.refresh(db_reader)
    return db_reader


def delete_reader(db: Session, reader_id: int) -> Optional[Reader]:
    db_reader = get_reader(db, reader_id=reader_id)
    if db_reader:
        db.delete(db_reader)
        db.commit()
    return db_reader
