from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlmodel import Session, select
from jose import jwt, JWTError
from app.db import get_session
from app.model import User


pwd_context = CryptContext(schemes=("bcrypt"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "8d10cb8c6ffb5e5ff4ae476c3395803a5fc221ce7bdbb7337b148ec982c01100"
ALGORITHM = "HS256"
EXPIRY_MINUTES = 30


def hash_password(password):
    return pwd_context.hash(password)

# ***********         ********** VERIFY PASSWORD ************          ******************

def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

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
    
    
# ***********         ********** Authenticate User ************          ******************

def authenticate_user(session : Annotated[Session, Depends(get_session)],
                      username,
                      password,
                      ):
       db_user = get_user_from_db(username=username, session=session, email=username)
       if not db_user:
           return False
       if not verify_password(password=password, hashed_password=db_user.password):
           return False
       return db_user


# ***********         ********** CREATE ACCESS TOKEN ************          ******************

def create_access_token(data: dict, expiry_time : timedelta | None = None):
    encode_data = data.copy()
    if expiry_time:
        expire = datetime.now(timezone.utc) + expiry_time
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    encode_data.update({"exp":expire})
    encoded_jwt = jwt.encode(encode_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt