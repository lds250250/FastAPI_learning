from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# 1. 定义 Pydantic 数据模型
class BookCreate(BaseModel):
    title: str
    author: str
    price: float
    description: str | None = None


# 2. 将模型作为函数参数（FastAPI 自动识别为请求体）
@app.post("/books/")
async def create_book(book: BookCreate):
    return {
        "message": "书籍创建成功",
        "book_title": book.title,
        "book_price": book.price,
    }


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
