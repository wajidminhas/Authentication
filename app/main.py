

from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from contextlib import asynccontextmanager

from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.auth import authenticate_user
from app.router.user import user_router
from app.db import create_db_and_tables, get_session
from app.model import Todo


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

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm ,Depends()],
                session: Annotated[Session, Depends(get_session)]):
    user = authenticate_user(session, form_data.username, form_data.password)
    return user