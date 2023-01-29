import re
from typing import Optional
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, conint, validator
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class PostOut(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    email: EmailStr
    password: str

    @validator("password", pre=True)
    def check_password(cls, password):
        if not re.match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d]{8,}$", password):
            raise HTTPException(
                status_code=400,
                detail="Password must have a minimum of 8 characters, 1 Uppercase, 1 lowercase and 1 number"
            )
        return password


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Schema for token and tokenData
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
    email: Optional[str] = None

# schema for Likes


class Like(BaseModel):
    post_id: int
    dir: conint(le=1)
