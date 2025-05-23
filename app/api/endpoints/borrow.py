from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_user
from app.crud.book import (decrease_book_quantity, get_book,
                           increase_book_quantity)
from app.crud.borrow import (create_borrow, get_active_reader_borrows,
                             get_borrow, get_borrow_by_book_and_reader,
                             get_returned_reader_borrows, return_borrow)
from app.crud.reader import get_reader
from app.schemas.borrow import BorrowCreate, BorrowReturn, ReaderBorrows

router = APIRouter()


@router.post("/borrow")
def borrow_book(
    borrow: BorrowCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    db_book = get_book(db, book_id=borrow.book_id)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена"
        )

    db_reader = get_reader(db, reader_id=borrow.reader_id)
    if not db_reader:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Считыватель не найден"
        )

    if db_book.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Доступных экземпляров этой книги нет",
        )

    active_borrows = get_active_reader_borrows(db, reader_id=borrow.reader_id)
    if len(active_borrows) >= 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Читатель набрал максимальное количество заимствованных "
                   "книг (3)",
        )

    existing_borrow = get_borrow_by_book_and_reader(
        db, book_id=borrow.book_id, reader_id=borrow.reader_id
    )
    if existing_borrow:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="У читателя уже есть эта книга",
        )

    decrease_book_quantity(db, book_id=borrow.book_id)
    db_borrow = create_borrow(db, book_id=borrow.book_id,
                              reader_id=borrow.reader_id)

    db.commit()
    return {"message": "Книга, успешно позаимствованная",
            "borrow_id": db_borrow.id}


@router.post("/return")
def return_book(
    borrow: BorrowReturn,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    db_borrow = get_borrow(db, borrow_id=borrow.borrow_id)
    if not db_borrow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запись о заимствовании не найдена",
        )

    if db_borrow.return_date is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Эта книга уже была возвращена",
        )

    db_book = get_book(db, book_id=db_borrow.book_id)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена"
        )

    increase_book_quantity(db, book_id=db_book.id)
    return_borrow(db, borrow_id=borrow.borrow_id)

    db.commit()
    return {"message": "Книга успешно возвращена"}


@router.get("/reader/{reader_id}", response_model=ReaderBorrows)
def get_reader_borrowings(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    return {
        "active_borrows": get_active_reader_borrows(db, reader_id=reader_id),
        "returned_borrows": get_returned_reader_borrows(
            db, reader_id=reader_id),
    }
