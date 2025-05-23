from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_user
from app.crud.reader import create_reader as create_reader_in_db
from app.crud.reader import delete_reader as delete_reader_in_db
from app.crud.reader import get_reader, get_readers
from app.crud.reader import update_reader as update_reader_in_db
from app.schemas.reader import Reader, ReaderCreate, ReaderUpdate

router = APIRouter()


@router.post("/", response_model=Reader)
def create_reader(
    reader: ReaderCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    try:
        return create_reader_in_db(db=db, reader=reader)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[Reader])
def read_readers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    return get_readers(db, skip=skip, limit=limit)


@router.get("/{reader_id}", response_model=Reader)
def read_reader(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    db_reader = get_reader(db, reader_id=reader_id)
    if db_reader is None:
        raise HTTPException(status_code=404, detail="Считыватель не найден")
    return db_reader


@router.put("/{reader_id}", response_model=Reader)
def update_reader(
    reader_id: int,
    reader: ReaderUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    db_reader = get_reader(db, reader_id=reader_id)
    if db_reader is None:
        raise HTTPException(status_code=404, detail="Считыватель не найден")
    return update_reader_in_db(db=db, reader_id=reader_id, reader=reader)


@router.delete("/{reader_id}")
def delete_reader(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    db_reader = get_reader(db, reader_id=reader_id)
    if db_reader is None:
        raise HTTPException(status_code=404, detail="Считыватель не найден")
    delete_reader_in_db(db=db, reader_id=reader_id)
    return {"message": "Программа чтения успешно удалена"}
