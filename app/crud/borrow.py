from datetime import datetime

from sqlalchemy.orm import Session

from app.models.borrow import Borrow


def create_borrow(db: Session, book_id: int, reader_id: int):
    db_borrow = Borrow(book_id=book_id, reader_id=reader_id)
    db.add(db_borrow)
    db.commit()
    db.refresh(db_borrow)
    return db_borrow


def get_borrow(db: Session, borrow_id: int):
    return db.query(Borrow).filter(Borrow.id == borrow_id).first()


def get_active_reader_borrows(db: Session, reader_id: int):
    return (
        db.query(Borrow)
        .filter(Borrow.reader_id == reader_id, Borrow.return_date.is_(None))
        .all()
    )


def get_returned_reader_borrows(db: Session, reader_id: int):
    return (
        db.query(Borrow)
        .filter(Borrow.reader_id == reader_id, Borrow.return_date.is_not(None))
        .all()
    )


def return_borrow(db: Session, borrow_id: int):
    db_borrow = (
        db.query(Borrow)
        .filter(Borrow.id == borrow_id, Borrow.return_date.is_(None))
        .first()
    )

    if db_borrow:
        db_borrow.return_date = datetime.utcnow()
        db.commit()
        db.refresh(db_borrow)

    return db_borrow


def get_borrow_by_book_and_reader(db: Session, book_id: int, reader_id: int):
    return (
        db.query(Borrow)
        .filter(
            Borrow.book_id == book_id,
            Borrow.reader_id == reader_id,
            Borrow.return_date.is_(None),
        )
        .first()
    )
