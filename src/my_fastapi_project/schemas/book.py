from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    isbn: str = Field(..., pattern=r"^[0-9]{13}$", min_length=13,
                      max_length=13, description="ISBN:13 位纯数字")
    title: str = Field(..., min_length=1, max_length=100, description="书名")
    author: str = Field(..., min_length=1, max_length=50, description="作者")
    price: float = Field(..., gt=0, description="价格")
    stock: int = Field(..., ge=0, description="库存")
    internal_note: str | None = Field(
        None, max_length=200, description="内部备注")


class BookResponse(BaseModel):
    isbn: str = Field(..., description="ISBN:13 位纯数字")
    title: str = Field(..., description="书名")
    author: str = Field(..., description="作者")
    price: float = Field(..., description="价格")
    stock: int = Field(...,  description="库存")


class BookUpdate(BaseModel):
    title: str | None = Field(
        None, min_length=1, max_length=100, description="书名")
    author: str | None = Field(
        None, min_length=1, max_length=50, description="作者")
    price: float | None = Field(None, gt=0, description="价格")
    stock: int | None = Field(None, ge=0, description="库存")
    internal_note: str | None = Field(
        None, max_length=200, description="内部备注")
