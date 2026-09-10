from fastapi import HTTPException, status, APIRouter

from my_fastapi_project.schemas.book import BookUpdate, BookCreate, BookResponse
from my_fastapi_project.api.deps import BookServiceDep, CurrentBookDep, PaginationDep

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/", response_model=BookResponse, status_code=201)
async def register_book(book: BookCreate, service: BookServiceDep):
    create = service.create(book)
    if create is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="ISBN 已存在"
        )
    return create


@router.get("/", response_model=list[BookResponse])
async def get_books(pagination: PaginationDep, service: BookServiceDep):
    return service.list_book(pagination.offset, pagination.limit)


@router.get("/{isbn}", response_model=BookResponse)
async def get_book(book_data: CurrentBookDep):
    return book_data


@router.patch("/{isbn}", response_model=BookResponse)
async def book_update(
    payload: BookUpdate,
    service: BookServiceDep,
    book_data: CurrentBookDep
):
    return service.update_book(book_data["isbn"], payload)


@router.delete("/{isbn}", status_code=204)
async def book_delete(service: BookServiceDep, book_data: CurrentBookDep):
    service.delete_book(book_data["isbn"])


@router.post("/{isbn}/borrow", response_model=BookResponse)
async def book_borrow(service: BookServiceDep, book_data: CurrentBookDep):
    borrowed = service.borrow(book_data["isbn"])
    if borrowed is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="库存不足"
        )
    return borrowed
