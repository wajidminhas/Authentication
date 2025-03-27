

from datetime import timedelta
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from contextlib import asynccontextmanager

from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.auth import EXPIRY_MINUTES, authenticate_user, create_access_token
from app.router.user import user_router
from app.db import create_db_and_tables, get_session
from app.model import Todo, Token


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("lifespan: starting")
    create_db_and_tables()
    yield
    print("lifespan: shutting down")


app = FastAPI(
    lifespan=lifespan,
    title="FastAPI Todo App",
)

app.include_router(router=user_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


#    ************     ***********     TODO POST API      ***********     ***********     **********

@app.post("/todo/", response_model=Todo)
async def create_todo(todo: Todo, session: Annotated[Session, Depends(get_session)]):
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

#    ************     ***********     TODO  GET SINGLE API      ***********     ***********     **********

@app.get("/todo/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int, session: Annotated[Session, Depends(get_session)]):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


#    ************     ***********     login user      ***********     ***********     **********

# here create a Token model to returen the access token
@app.post("/token/", response_model=Token) 
async def login(form_data: Annotated[OAuth2PasswordRequestForm ,Depends()],
                session: Annotated[Session, Depends(get_session)]):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    expire_time = timedelta(minutes=EXPIRY_MINUTES)
    access_token =create_access_token({"sub": form_data.username}, expire_time)
    return Token(access_token=access_token, token_type="bearer")