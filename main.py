from fastapi import FastAPI
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

app = FastAPI()


class UserCreate(BaseModel):
    username: str = Field(..., min_length=2,
                          max_length=20, description="用户登录名")
    password: str = Field(..., min_length=6,
                          max_length=20, description="用户登录密码")
    email: str = Field(..., description="用户邮箱")


class UserRead(BaseModel):
    user_id: int = Field(..., description="用户ID")
    username: str = Field(..., description="用户登录名")
    email: str = Field(..., description="用户邮箱")
    password: str = Field(..., exclude=True, description="用户登录密码")


class UserUpdate(BaseModel):
    username: Optional[str] = Field(
        default=None, min_length=2, max_length=20, description="用户登录名")
    email: Optional[str] = Field(default=None, description="用户邮箱")


fake_db = {}


@app.post("/users/", response_model=UserRead, status_code=201)
async def create_user(user: UserCreate):
    if user_id not in fake_db:
        return {"detail": "用户不存在"}
    return fake_db[user_id]


@app.patch("/users/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user_update: UserUpdate):
    if user_id not in fake_db:
        return {"detail": "用户不存在"}

    update_data = user_update.model_dump(exclude_unset=True)
    fake_db[user_id].update(update_data)
    return fake_db[user_id]


class ArticleCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="文章标题")
    content: str = Field(..., min_length=1, description="文章正文")


class ArticleRead(BaseModel):
    article_id: int = Field(..., description="文章唯一ID")
    title: str = Field(..., description="文章标题")
    content: str = Field(..., description="文章正文")
    author: str = Field(..., description="文章作者")


class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(
        default=None, min_length=1, max_length=100, description="新的文章标题")
    content: Optional[str] = Field(
        default=None, min_length=1, description="新的文章正文")

fake_articles_db = {
    1: {"article_id": 1, "title": "初学FastAPI", "content": "这是正文...", "author": "Cloudy"}
}

@app.patch("/articles/{article_id}", response_model=ArticleRead)
async def update_article(article_id: int, article_update: ArticleUpdate):
    if article_id not in fake_articles_db:
        return {"detail": "文章不存在"}
    
    update_data = article_update.model_dump(exclude_unset=True)
    fake_articles_db[article_id].update(update_data)
    
    return fake_articles_db[article_id]