from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_user
from app.crud.book import create_book as create_book_in_db
from app.crud.book import delete_book as delete_book_in_db
from app.crud.book import get_book
from app.crud.book import get_books as get_books_in_db
from app.crud.book import update_book as update_book_in_db
from app.schemas.book import Book, BookCreate, BookUpdate
from app.schemas.user import User

router = APIRouter()


@router.post("/", response_model=Book)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    return create_book_in_db(db=db, book=book)


@router.get("/", response_model=List[Book])
def get_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = get_books_in_db(db, skip=skip, limit=limit)
    return books


@router.get("/{book_id}", response_model=Book)
def read_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_book = get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена"
        )
    return db_book


@router.put("/{book_id}", response_model=Book)
def update_book(
    book_id: int,
    book: BookUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    db_book = get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена"
        )
    return update_book_in_db(db=db, book_id=book_id, book=book)


@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    db_book = get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена"
        )
    delete_book_in_db(db=db, book_id=book_id)
    return {"message": "Книга успешно удалена"}
