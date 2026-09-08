from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()


class UserProfile(BaseModel):
    age: int = Field(..., gt=0, description="用户年龄")
    bio: str | None = Field(None, max_length=200, description="个人简历")


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, description="用户名")
    email: EmailStr = Field(..., description="用户邮箱")
    password: str = Field(..., min_length=8, description="用户密码")
    profile: UserProfile | None = Field(None, description="个人简介信息")


@app.post("/users/register/")
async def register_user(user: UserCreate)
return user
