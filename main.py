from pydantic import BaseModel, field_validator, model_validator


class User(BaseModel):
    username: str

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if not v.islower():
            raise ValueError('用户名必须全小写')
        return v


class Course(BaseModel):
    start_date: int
    end_date: int

    @model_validator(mode='after')
    def check_dates(self):
        if self.end_date < self.start_date:
            raise ValueError('结束日期不能早于开始日期')
        return self
