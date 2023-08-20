from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

# this is for the request --- what user sends to us


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # this is an optional


class PostCreate(PostBase):
    pass


# this is for the response --- what we send to user
# instead of duplicating the fields again -- we can inherit the class PostBase and the class Post will have all the details that is in the parent class
# class Post(BaseModel):
#     id: int
#     title: str
#     content: str
#     published: bool
#     created_at: datetime

#     class Config:
#         orm_mode = True
class UserOut(BaseModel):
    id: int
    # password: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr  # this is to validate the email
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# shema for the access token and its type
class Token(BaseModel):
    access_token: str
    token_type: str

# shema for the data that is embeded into the token


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    # user_id : int
    dir: conint(le=1)
