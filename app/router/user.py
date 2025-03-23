from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.auth import oauth2_scheme
from app.auth import get_user_from_db, hash_password
from app.db import get_session
from app.model import Register_User, User


user_router = APIRouter(
    prefix= "/user",
    tags = ["user"],
    responses= {404: {"description": "User Not found"}},
)

@user_router.get("/")
async def read_user():
    return {"message": "Welcome to Nawfa Mart"}

@user_router.post("/register")
async def register_user(new_data : Annotated[Register_User, Depends()], 
                        session : Annotated[Session, Depends(get_session)],
                        ):
    db_user = get_user_from_db(session, new_data.username,
                                new_data.email 
                                )
    if db_user:
        return HTTPException(status_code=400, detail="User already exists")
    user = User(username=new_data.username, email=new_data.email, password=hash_password(new_data.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": f""" User {user.username} has been registered"""}

@user_router.get("/login")
async def user_profile(current_user : Annotated[User, Depends(oauth2_scheme)]):
    return ("hello world")
    
