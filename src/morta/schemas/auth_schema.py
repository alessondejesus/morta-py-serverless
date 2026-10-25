from pydantic import BaseModel, EmailStr, Field


class RegisterAccount(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str


class RegisteredAccount(BaseModel):
    id: int
    name: str = Field(min_length=3, max_length=100)
    email: EmailStr
