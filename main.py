from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional

app = FastAPI()

BookName = Annotated[str,
                     Field(..., min_length=2, max_length=50, description="书名")]
PositiveInt = Annotated[int, Field(..., gt=0, description="正整数")]


class BookCreate(BaseModel):
    title: BookName
    author: str = Field(..., min_length=2, max_length=30, description="作者")
    price: float = Field(..., gt=0, description="价格")
    tags: list[str] | None = Field([], description="标签")


class BookRead(BaseModel):
    book_id: PositiveInt
    title: BookName
    author: str = Field(..., description="作者")
    price: float = Field(..., description="价格")
    tags: list[str] | None = Field([], description="标签")
    internal_note: str = Field(..., description="内部备注", exclude=True)


class BookUpdate(BaseModel):
    title: str | None = Field(
        None, min_length=2, max_length=50, description="书名")
    author: str | None = Field(
        None, min_length=2, max_length=30, description="作者")
    price: float | None = Field(None, gt=0, description="价格")
    tags: list[str] | None = Field(None, description="标签")


fake_books_db = {}


@app.post("/books/", response_model=BookRead, status_code=201)
async def create_book(book: BookCreate):
    new_id = len(fake_books_db)+1
    fake_books_db[new_id] = {
        **book.model_dump(), "book_id": new_id, "internal_note": "系统自动创建"}
    return fake_books_db[new_id]


@app.get("/books/{book_id}", response_model=BookRead)
async def read_book(book_id: int):
    if book_id not in fake_books_db:
        raise HTTPException(status_code=404, detail="书籍不存在")

    return fake_books_db[book_id]


@app.get("/books/", response_model=list[BookRead])
async def read_books():
    return list(fake_books_db.values())


@app.patch("/books/{book_id}", response_model=BookRead)
async def update_book(book_id: int, book_update: BookUpdate):
    if book_id not in fake_books_db:
        raise HTTPException(status_code=404, detail="书籍不存在")

    update_data = book_update.model_dump(exclude_unset=True)
    fake_books_db[book_id].update(update_data)

    return fake_books_db[book_id]
