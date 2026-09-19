import json
import logging
from typing import Any

from redis.asyncio import Redis

from my_fastapi_project.core.exceptions import (
    BookAlreadyExists,
    NotBorrowed,
    OutOfStock,
)
from my_fastapi_project.core.redis import RedisUnavailable
from my_fastapi_project.repositories.book_repo import BookRepository
from my_fastapi_project.repositories.borrow_repo import BorrowRecordRepository
from my_fastapi_project.schemas.book import BookCreate, BookUpdate

logger = logging.getLogger(__name__)

CACHE_TTL = 60
CACHE_MISS = "__MISS__"


class BookService:
    def __init__(
        self,
        repo: BookRepository,
        record_repo: BorrowRecordRepository,
        cache: Redis,
    ):
        self.repo = repo
        self.record_repo = record_repo
        self.cache = cache

    async def create(self, book: BookCreate) -> dict[str, Any]:
        if await self.repo.exists(book.isbn):
            raise BookAlreadyExists(book.isbn)
        data = book.model_dump()
        created = await self.repo.create(book.isbn, data)
        await self._invalidate(book.isbn)
        return created

    async def list_book(self, offset: int, limit: int) -> list[dict[str, Any]]:
        return await self.repo.list_all(offset, limit)

    async def get_book(self, isbn: str) -> dict[str, Any] | None:
        key = self._cache_key(isbn)

        cached = await self._cache_get(key)
        if cached is not None:
            if cached == CACHE_MISS:
                return None
            return json.loads(cached)

        book = await self.repo.get(isbn)

        if book is None:
            await self._cache_set(key, CACHE_MISS, ex=5)
            return None

        await self._cache_set(key, json.dumps(book), ex=CACHE_TTL)
        return book

    async def update_book(self, isbn: str, data: BookUpdate) -> dict[str, Any] | None:
        payload = data.model_dump(exclude_unset=True)
        updated = await self.repo.update(isbn, payload)
        await self._invalidate(isbn)
        return updated

    async def delete_book(self, isbn: str) -> bool:
        deleted = await self.repo.delete(isbn)
        await self._invalidate(isbn)
        return deleted

    async def borrow(self, username: str, isbn: str) -> dict[str, Any]:
        if not await self.repo.decrement_stock(isbn):
            raise OutOfStock()
        await self.record_repo.create(username, isbn)
        await self._invalidate(isbn)
        return await self.repo.get(isbn)

    async def return_book(self, username: str, isbn: str) -> dict[str, Any]:
        record = await self.record_repo.get_open(username, isbn)
        if record is None:
            raise NotBorrowed()
        await self.record_repo.close(record["id"])
        await self.repo.increment_stock(isbn)
        await self._invalidate(isbn)
        return await self.repo.get(isbn)

    @staticmethod
    def _cache_key(isbn: str) -> str:
        return f"book:{isbn}"

    async def _cache_get(self, key: str) -> str | None:
        try:
            return await self.cache.get(key)
        except RedisUnavailable:
            logger.warning("Redis 不可用，缓存降级（读 %s）", key)
            return None

    async def _cache_set(self, key: str, value: str, ex: int) -> None:
        try:
            await self.cache.set(key, value, ex=ex)
        except RedisUnavailable:
            logger.warning("Redis 不可用，缓存降级（写 %s）", key)

    async def _invalidate(self, isbn: str) -> None:
        try:
            await self.cache.delete(self._cache_key(isbn))
        except RedisUnavailable:
            logger.warning("Redis 不可用，缓存降级（删 %s）", self._cache_key(isbn))
