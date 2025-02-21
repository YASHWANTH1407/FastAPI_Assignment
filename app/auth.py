from datatime import datatime,timedelta
from jose import jwt,JWTError
from passlib.context import CryptContext
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.token import TokenData
import os

#secreat key and algorithm
SECRET_KEY=os.getenv("JWT_SECRET","supersecretkey")
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

#password hashing
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

#OAuth2 scheme for token extraction
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="auth/login")

#Hash a password
def hash_password(password:str):
    return pwd_context.hash(password)

#verify a password
def verify_password(plain_password:str,hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)

#Generate a Jwt token
def create_access_token(data:dict,expires_delta:timedelta|None =None):
    to_encode=data.copy()
    expire=datatime.utcnow()+(expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

#decode a Jwt token and validate it
def get_current_user(token:str=Depends(oauth2_scheme), db : Session==Depends(get_db)): # type: ignore
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"},

    )
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data=TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user=db.query(User).filter(User.username==token_data.username).first()
    if user is None:
        raise credentials_exception
    return user