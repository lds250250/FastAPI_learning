from fastapi import HTTPException, status, Depends, Query, Header
from typing import Annotated

from my_fastapi_project.repositories.user_repo import UserRepository
from my_fastapi_project.services.user_service import UserService

from my_fastapi_project.repositories.book_repo import BookRepository
from my_fastapi_project.services.book_service import BookService


def get_user_repo() -> UserRepository:
    return UserRepository()


def get_user_service(
        repo: Annotated[UserRepository, Depends(get_user_repo)],
) -> UserService:
    return UserService(repo)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


async def get_current_user(
        username: str,
        service: UserServiceDep,
) -> dict:
    user = service.get_user(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"用户'{username}'不存在"
        )
    return user

CurrentUserDep = Annotated[dict, Depends(get_current_user)]


def get_book_repo() -> BookRepository:
    return BookRepository()


def get_book_service(repo: Annotated[BookRepository, Depends(get_book_repo)]) -> BookService:
    return BookService(repo)


BookServiceDep = Annotated[BookService, Depends(get_book_service)]


async def get_current_book(isbn: str, service: BookServiceDep) -> dict:
    book = service.get_book(isbn)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"图书'{isbn}'不存在"
        )
    return book

CurrentBookDep = Annotated[dict, Depends(get_current_book)]


class Pagination:

    def __init__(
            self,
            page: int = Query(1, ge=1, description="页码，从 1 开始"),
            size: int = Query(10, ge=1, le=100, description="每页条数"),
    ):
        self.page = page
        self.size = size

    @property
    def offset(self) -> int:
        return (self.page-1)*self.size

    @property
    def limit(self) -> int:
        return self.size


PaginationDep = Annotated[Pagination, Depends(Pagination)]


DEMO_API_KEY = "demo-secret-key"


async def verify_api_key(
        x_api_key: Annotated[str | None, Header()] = None,
) -> None:
    if x_api_key != DEMO_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key 无效或缺失",
        )
