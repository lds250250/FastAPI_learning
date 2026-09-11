import time
from typing import Annotated

from fastapi import HTTPException, status, Depends, Query, Header, Request


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


API_KEYS = {
    "demo-secret-key": "user",
    "admin-secret-key": "admin",
}

ROLE_USER = "user"
ROLE_ADMIN = "admin"


async def get_caller_role(
        x_api_key: Annotated[str | None, Header()] = None,
) -> str:
    role = API_KEYS.get(x_api_key)
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key 无效或缺失",
        )
    return role

CallerRoleDep = Annotated[str, Depends(get_caller_role)]


def require_role(required: str):
    async def checker(role: CallerRoleDep) -> None:
        if role != required:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"需要 {required} 权限",
            )

    return checker


# ---------- 限流 ----------


RATE_LIMIT_TIMES = 5
RATE_LIMIT_WINDOW = 60

_hits: dict[str, list[float]] = {}


async def rate_limit(request: Request) -> None:
    client = request.client.host if request.client else "unknown"
    now = time.monotonic()

    timestamps = _hits.setdefault(client, [])

    cutoff = now-RATE_LIMIT_WINDOW
    while timestamps and timestamps[0] < cutoff:
        timestamps.pop(0)

    if len(timestamps) >= RATE_LIMIT_TIMES:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="请求过于频繁，请稍后再试",
        )

    timestamps.append(now)


# ---------- 请求耗时日志 ----------


async def log_request(request: Request):
    start = time.monotonic()
    yield
    elapsed = (time.monotonic()-start)*1000
    print(f"[{request.method}]{request.url.path} {elapsed:.0f} ms")
