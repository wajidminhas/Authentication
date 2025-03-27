from typing import Annotated, List, Optional
from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlmodel import Relationship, SQLModel, Field





class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str
    todos: List["Todo"] = Relationship(back_populates="user")

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    is_completed: bool = Field(default=False)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="todos")
    

 # ***********     ***********     ***********     ***********     ***********     ********** 

    
class Register_User(BaseModel):
    email: Annotated[
        str,
        Field(
            max_length=20,
        ),
        Form()
    ]

    password: Annotated[
        str,
        Field(
            min_length=8,
        ),
        Form()
    ]
    username: Annotated[
        str,
        Field(
            max_length=20,
        ),
        Form()
    ]


class Token(BaseModel):
    access_token: str
    token_type: str


# class TokenData(BaseModel):
#     username: str | None = None


# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool | None = None


# class UserInDB(User):
#     hashed_password: str