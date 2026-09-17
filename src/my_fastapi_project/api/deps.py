from collections.abc import AsyncIterator
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Query, Request, status
from fastapi.security import OAuth2PasswordBearer
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from my_fastapi_project.core.db import SessionFactory
from my_fastapi_project.core.exceptions import InvalidCredentials
from my_fastapi_project.core.redis import RedisUnavailable, redis_client
from my_fastapi_project.core.roles import ROLE_ADMIN
from my_fastapi_project.core.security import decode_access_token
from my_fastapi_project.repositories.book_repo import BookRepository
from my_fastapi_project.repositories.borrow_repo import BorrowRecordRepository
from my_fastapi_project.repositories.user_repo import UserRepository
from my_fastapi_project.services.book_service import BookService
from my_fastapi_project.services.borrow_service import BorrowService
from my_fastapi_project.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ---------- 会话 ----------


async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionFactory() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


# ---------- 缓存 ----------
def get_redis() -> Redis:
    return redis_client


RedisDep = Annotated[Redis, Depends(get_redis)]

# ---------- USER ----------


def get_user_repo(session: SessionDep) -> UserRepository:
    return UserRepository(session)


def get_user_service(
    repo: Annotated[UserRepository, Depends(get_user_repo)],
) -> UserService:
    return UserService(repo)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


# ---------- BOOK ----------


def get_book_repo(session: SessionDep) -> BookRepository:
    return BookRepository(session)


def get_borrow_repo(session: SessionDep) -> BorrowRecordRepository:
    return BorrowRecordRepository(session)


def get_book_service(
    repo: Annotated[BookRepository, Depends(get_book_repo)],
    record_repo: Annotated[BorrowRecordRepository, Depends(get_borrow_repo)],
    cache: RedisDep,
) -> BookService:
    return BookService(repo, record_repo, cache)


BookServiceDep = Annotated[BookService, Depends(get_book_service)]


async def get_current_book(isbn: str, service: BookServiceDep) -> dict:
    book = await service.get_book(isbn)
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
    user = await service.get_user(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"用户 '{username}' 不存在",
        )
    return user


PathUserDep = Annotated[dict, Depends(get_path_user)]


# ---------- 限流 ----------


async def _check_limit(cache: Redis, key: str, times: int, window: int) -> None:
    try:
        await cache.set(key, 0, ex=window, nx=True)
        count = await cache.incr(key)
    except RedisUnavailable:
        return

    if count > times:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="请求过于频繁，请稍后再试",
        )


def rate_limiter(scope: str, times: int, window: int):
    async def limiter(request: Request, cache: RedisDep) -> None:
        client = request.client.host if request.client else "unknown"
        await _check_limit(cache, f"rate:{scope}:ip:{client}", times, window)

    return limiter


def user_rate_limiter(scope: str, times: int, window: int):
    async def limiter(caller: CallerDep, cache: RedisDep) -> None:
        await _check_limit(
            cache, f"rate:{scope}:user:{caller['username']}", times, window
        )

    return limiter


login_rate_limit = rate_limiter("auth:token", 5, 60)
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

    user = await service.get_user(payload["sub"])
    if user is None:
        raise InvalidCredentials()

    return user


CallerDep = Annotated[dict, Depends(get_caller)]
books_rate_limit = user_rate_limiter("books", 5, 60)
users_rate_limit = user_rate_limiter("users", 10, 60)


async def require_self_or_admin(caller: CallerDep, username: str):
    if caller["role"] == ROLE_ADMIN:
        return
    if caller["username"] == username:
        return
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="只能操作自己的资料",
    )


async def require_not_self(caller: CallerDep, username: str) -> None:
    """不允许对自己执行这个操作。"""
    if caller["username"] == username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能对自己执行此操作",
        )


# ---------- borrow ----------
def get_borrow_service(
    repo: Annotated[BorrowRecordRepository, Depends(get_borrow_repo)],
) -> BorrowService:
    return BorrowService(repo)


BorrowServiceDep = Annotated[BorrowService, Depends(get_borrow_service)]
