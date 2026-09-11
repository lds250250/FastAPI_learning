from fastapi import APIRouter, Depends

from my_fastapi_project.api.deps import (
    ROLE_ADMIN,
    BookServiceDep,
    CurrentBookDep,
    PaginationDep,
    books_rate_limit,
    get_caller_role,
    require_role,
)
from my_fastapi_project.schemas.book import BookCreate, BookResponse, BookUpdate

router = APIRouter(
    prefix="/books",
    tags=["books"],
    dependencies=[
        Depends(books_rate_limit),
        Depends(get_caller_role),
    ],
)


@router.post(
    "/",
    response_model=BookResponse,
    status_code=201,
)
async def register_book(book: BookCreate, service: BookServiceDep):
    return service.create(book)


@router.get("/", response_model=list[BookResponse])
async def get_books(pagination: PaginationDep, service: BookServiceDep):
    return service.list_book(pagination.offset, pagination.limit)


@router.get("/{isbn}", response_model=BookResponse)
async def get_book(book_data: CurrentBookDep):
    return book_data


@router.patch("/{isbn}", response_model=BookResponse)
async def book_update(
    payload: BookUpdate, service: BookServiceDep, book_data: CurrentBookDep
):
    return service.update_book(book_data["isbn"], payload)


@router.delete(
    "/{isbn}",
    status_code=204,
    dependencies=[Depends(require_role(ROLE_ADMIN))],
)
async def book_delete(service: BookServiceDep, book_data: CurrentBookDep):
    service.delete_book(book_data["isbn"])


@router.post("/{isbn}/borrow", response_model=BookResponse)
async def book_borrow(service: BookServiceDep, book_data: CurrentBookDep):
    return service.borrow(book_data["isbn"])
