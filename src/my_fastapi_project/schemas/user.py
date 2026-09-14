from pydantic import BaseModel, EmailStr, Field, field_validator


class UserProfile(BaseModel):
    age: int = Field(..., gt=0, description="用户年龄")
    bio: str | None = Field(None, max_length=200, description="个人简历")


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, description="用户名")
    email: EmailStr = Field(..., description="用户邮箱")
    password: str = Field(..., min_length=8, max_length=72, description="用户密码")
    profile: UserProfile | None = Field(None, description="个人简介信息")

    @field_validator("password")
    @classmethod
    def password_within_bcrypt_limit(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError("密码过长")
        return value


class UserResponse(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, description="用户名")
    email: EmailStr = Field(..., description="用户邮箱")
    profile: UserProfile | None = Field(None, description="个人简介信息")


class UserUpdate(BaseModel):
    email: EmailStr | None = Field(None, description="用户邮箱")
    profile: UserProfile | None = Field(None, description="个人简介信息")


class PasswordUpdate(BaseModel):
    old_password: str = Field(..., min_length=8, description="用户密码")
    new_password: str = Field(..., min_length=8, description="用户密码")
