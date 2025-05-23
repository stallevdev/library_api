from fastapi import APIRouter

from app.api.endpoints import (auth_router, book_router, borrow_router,
                               reader_router)

main_router = APIRouter()
main_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["auth"],
)
main_router.include_router(
    book_router,
    prefix="/books",
    tags=["books"],
)
main_router.include_router(
    reader_router,
    prefix="/readers",
    tags=["readers"],
)
main_router.include_router(borrow_router, prefix="/borrows", tags=["borrows"])
