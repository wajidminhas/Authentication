from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.auth import get_user_from_db, hash_password
from app.db import get_session
from app.model import Register_User


user_router = APIRouter(
    prefix= "/user",
    tags = ["user"],
    responses= {404: {"description": "User Not found"}},
)

@user_router.get("/")
async def read_user():
    return {"message": "Welcome to Nawfa Mart"}

@user_router.post("/register")
async def register_user(form_data : Annotated[Register_User, Depends()], 
                        session : Annotated[Session, Depends(get_session)], username, email, password):
    db_user = get_user_from_db(session, form_data.username == username,
                                form_data.email == email)
    if db_user:
        return HTTPException(status_code=400, detail="User already exists")
    user = Register_User(username=form_data.username,
                          email=form_data.email,
                         password=hash_password(form_data.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
