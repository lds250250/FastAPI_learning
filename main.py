from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr
from fastapi import HTTPException, Depends, status
from typing import Annotated

app = FastAPI()


class UserProfile(BaseModel):
    age: int = Field(..., gt=0, description="用户年龄")
    bio: str | None = Field(None, max_length=200, description="个人简历")


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, description="用户名")
    email: EmailStr = Field(..., description="用户邮箱")
    password: str = Field(..., min_length=8, description="用户密码")
    profile: UserProfile | None = Field(None, description="个人简介信息")


class UserRead(BaseModel):
    username: str = Field(..., description="用户名")
    email: EmailStr = Field(..., description="用户邮箱")
    password: str = Field(..., exclude=True, description="用户密码")
    profile: UserProfile | None = Field(None, description="个人简介")


fake_users_db = {}


async def get_user_by_username(username: str):
    if username not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"用户'{username}'不存在"
        )
    return fake_users_db[username]


@app.post("/users/register/", response_model=UserRead, status_code=201)
async def register_user(user: UserCreate):
    hashed_password = f'hashed_{user.password}'

    fake_users_db[user.username] = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "profile": user.profile.model_dump() if user.profile else None
    }

    return fake_users_db[user.username]


@app.get("/users/{username}", response_model=UserRead)
async def get_user(user_data: dict = Depends(get_user_by_username)):

    return user_data
