from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlmodel import Session, select

from app.db import get_session
from app.model import User


pwd_context = CryptContext(schemes=("bcrypt"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def hash_password(password):
    return pwd_context.hash(password)

# ***********         ********** REGISTER USER ************          ******************

def get_user_from_db(session : Annotated[Session, Depends(get_session)],
                     username : str, 
                     email : str):
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    if not user:
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        if user:
            return user
    return user
    
    

