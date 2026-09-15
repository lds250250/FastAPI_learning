import time
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Query, Request, status
from fastapi.security import OAuth2PasswordBearer

from my_fastapi_project.core.exceptions import InvalidCredentials
from my_fastapi_project.core.security import decode_access_token
from my_fastapi_project.repositories.book_repo import BookRepository
from my_fastapi_project.repositories.user_repo import UserRepository
from my_fastapi_project.services.book_service import BookService
from my_fastapi_project.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ---------- USER ----------


def get_user_repo() -> UserRepository:
    return UserRepository()


def get_user_service(
    repo: Annotated[UserRepository, Depends(get_user_repo)],
) -> UserService:
    return UserService(repo)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


# ---------- BOOK ----------


def get_book_repo() -> BookRepository:
    return BookRepository()


def get_book_service(
    repo: Annotated[BookRepository, Depends(get_book_repo)],
) -> BookService:
    return BookService(repo)


BookServiceDep = Annotated[BookService, Depends(get_book_service)]


async def get_current_book(isbn: str, service: BookServiceDep) -> dict:
    book = service.get_book(isbn)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"图书'{isbn}'不存在"
        )
    return book


CurrentBookDep = Annotated[dict, Depends(get_current_book)]


# ---------- 通用 ----------


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
        return (self.page - 1) * self.size

    @property
    def limit(self) -> int:
        return self.size


PaginationDep = Annotated[Pagination, Depends(Pagination)]


def require_role(required: str):
    async def checker(caller: CallerDep) -> None:
        if caller["role"] != required:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"需要 {required} 权限",
            )

    return checker


async def get_path_user(
    username: str,
    service: UserServiceDep,
) -> dict:
    user = service.get_user(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"用户 '{username}' 不存在",
        )
    return user


PathUserDep = Annotated[dict, Depends(get_path_user)]


# ---------- 限流 ----------


_hits: dict[str, list[float]] = {}


def rate_limiter(scope: str, times: int, window: int):

    async def limiter(request: Request) -> None:
        client = request.client.host if request.client else "unknown"
        now = time.monotonic()

        key = f"{scope}:{client}"
        timestamps = _hits.setdefault(key, [])

        cutoff = now - window
        while timestamps and timestamps[0] < cutoff:
            timestamps.pop(0)

        if len(timestamps) >= times:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="请求过于频繁，请稍后再试",
            )

        timestamps.append(now)

    return limiter


login_rate_limit = rate_limiter("auth:token", 5, 60)


books_rate_limit = rate_limiter("books", 5, 60)
users_rate_limit = rate_limiter("users", 10, 60)
register_rate_limit = rate_limiter("users:register", 3, 60)


# ---------- token ----------


async def get_caller(
    token: Annotated[str, Depends(oauth2_scheme)],
    service: UserServiceDep,
) -> dict:
    try:
        payload = decode_access_token(token)
    except jwt.InvalidTokenError:
        raise InvalidCredentials()

    user = service.get_user(payload["sub"])
    if user is None:
        raise InvalidCredentials()

    return user


CallerDep = Annotated[dict, Depends(get_caller)]
