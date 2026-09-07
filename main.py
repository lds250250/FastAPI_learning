from fastapi import FastAPI
from pydantic import BaseModel, Field, ConfigDict

app = FastAPI()


class Student(BaseModel):
    model_config = ConfigDict(extra="forbid",               # 严禁传入未定义的多余字段
                              str_strip_whitespace=True     # 自动去除字符串首尾的空格
                              )

    name:str=Field(
        ...,
        min_length=2,
        max_length=20,
        description="学生姓名"
    )
    age:int = Field(
        ...,
        gt=0,
        le=150,
        description="学生年龄"
    )

@app.post("/student")
async def create_student(student: Student):
    return student.model_dump()