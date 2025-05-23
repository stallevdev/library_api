from fastapi import status
from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.borrow import Borrow
from app.models.reader import Reader


def test_borrow_book_success(db: Session, client, librarian_token):
    book = Book(title="Test Book", author="Author", quantity=2)
    reader = Reader(name="Test Reader", email="reader@test.com")
    db.add_all([book, reader])
    db.commit()

    response = client.post(
        "/borrows/borrow",
        json={"book_id": book.id, "reader_id": reader.id},
        headers={"Authorization": f"Bearer {librarian_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert db.query(Borrow).count() == 1
    assert db.query(Book).filter(Book.id == book.id).first().quantity == 1


def test_borrow_book_no_copies(db: Session, client, librarian_token):
    book = Book(title="Test Book", author="Author", quantity=0)
    reader = Reader(name="Test Reader", email="reader1@test.com")
    db.add_all([book, reader])
    db.commit()

    response = client.post(
        "/borrows/borrow",
        json={"book_id": book.id, "reader_id": reader.id},
        headers={"Authorization": f"Bearer {librarian_token}"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Доступных экземпляров" in response.json()["detail"]


def test_borrow_book_max_limit(db: Session, client, librarian_token):
    reader = Reader(name="Test Reader", email="reader2@test.com")
    books = [
        Book(title=f"Book {i}", author="Author", quantity=1) for i in range(4)]
    db.add_all([reader] + books)
    db.commit()

    for i in range(3):
        client.post(
            "/borrows/borrow",
            json={"book_id": books[i].id, "reader_id": reader.id},
            headers={"Authorization": f"Bearer {librarian_token}"},
        )

    response = client.post(
        "/borrows/borrow",
        json={"book_id": books[3].id, "reader_id": reader.id},
        headers={"Authorization": f"Bearer {librarian_token}"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "максимальное количество" in response.json()["detail"]
    assert (
        db.query(Borrow)
        .filter(Borrow.return_date.is_(None), Borrow.reader_id == reader.id)
        .count()
        == 3
    )


def test_return_book_success(db: Session, client, librarian_token):
    book = Book(title="Test Book", author="Author", quantity=2)
    reader = Reader(name="Test Reader", email="reader3@test.com")
    db.add_all([book, reader])
    db.commit()

    borrow_id = client.post(
        "/borrows/borrow",
        json={"book_id": book.id, "reader_id": reader.id},
        headers={"Authorization": f"Bearer {librarian_token}"},
    ).json()["borrow_id"]

    response = client.post(
        "/borrows/return",
        json={"borrow_id": borrow_id},
        headers={"Authorization": f"Bearer {librarian_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert db.query(Book).filter(Book.id == book.id).first().quantity == 2
    assert (
        db.query(Borrow).filter(
            Borrow.id == borrow_id).first().return_date is not None
    )


def test_return_already_returned(db: Session, client, librarian_token):
    book = Book(title="Test Book", author="Author", quantity=1)
    reader = Reader(name="Test Reader", email="reader4@test.com")
    db.add_all([book, reader])
    db.commit()

    borrow_id = client.post(
        "/borrows/borrow",
        json={"book_id": book.id, "reader_id": reader.id},
        headers={"Authorization": f"Bearer {librarian_token}"},
    ).json()["borrow_id"]

    client.post(
        "/borrows/return",
        json={"borrow_id": borrow_id},
        headers={"Authorization": f"Bearer {librarian_token}"},
    )

    response = client.post(
        "/borrows/return",
        json={"borrow_id": borrow_id},
        headers={"Authorization": f"Bearer {librarian_token}"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "уже была возвращена" in response.json()["detail"]


def test_return_nonexistent_borrowing(client, librarian_token):
    response = client.post(
        "/borrows/return",
        json={"borrow_id": 999},
        headers={"Authorization": f"Bearer {librarian_token}"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
