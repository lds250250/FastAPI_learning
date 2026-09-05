from fastapi import FastAPI
from pydantic import BaseModel
from pydantic import Field
from fastapi import status
from fastapi import HTTPException

app = FastAPI()


class UserResponse(BaseModel):
    username: str = Field(description="用户名")
    email: str = Field(description="邮箱")


fake_db_user = {
    "username": "cloudy",
    "email": "cloudy@example.com",
    "password": "super_secret_123",
    "internal_status": "active_admin"
}


class Publisher(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="出版社名称")
    address: str | None = Field(
        default=None, max_length=200, description="出版社地址")

# 1. 定义 Pydantic 数据模型


class BookCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="书籍标题，长度2-100",
        examples=["三体"]
    )
    author: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="作者姓名"
    )
    price: float | None = Field(
        default=None,
        gt=0,
        le=9999.99,
        description="价格必须大于0且不超过9999.99"
    )
    publisher: Publisher | None = Field(default=None, description="出版社信息（可选）")


fake_db = {
    1: {"id": 1, "title": "三体", "author": "刘慈欣"},
    2: {"id": 2, "title": "活着", "author": "余华"}
}


# 2. 将模型作为函数参数（FastAPI 自动识别为请求体）
@app.post(
    "/books/",
    tags=["书籍管理"],
    summary="创建一本新书",
    status_code=status.HTTP_201_CREATED
)
async def create_book(book: BookCreate):
    new_id = max(fake_db.keys())+1 if fake_db else 1
    new_book = {"id": new_id, **book.model_dump()}
    fake_db[new_id] = new_book
    return {
        "message": "书籍创建成功",
        "book_title": book.title,
    }


@app.get(
    "/books/{book_id}",
    tags=["书籍管理"],
    summary="根据ID获取书籍详情"
)
async def get_book(book_id: int):
    if book_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"找不到 ID 为 {book_id} 的书籍"
        )
    return fake_db[book_id]


@app.delete(
        "/books/{book_id}",
        tags=["书籍管理"],
        summary="删除指定书籍", 
        status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    if book_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"无法删除：找不到 ID 为 {book_id} 的书籍"
        )
    del fake_db[book_id]
    return

# 接口1：根路径


@app.get("/")
async def read_root():
    return {"Hello": "World"}


# 接口2：路径参数
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


# 接口3：路径参数 + 查询参数
@app.get("/users/{user_id}/books")
async def get_user_books(
    user_id: int, page: int = 1, limit: int = 10, category: str | None = None
):
    return {"user_id": user_id,
            "page": page,
            "limit": limit,
            "category": category}
