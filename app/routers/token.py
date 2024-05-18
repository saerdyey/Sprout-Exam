from functools import wraps
from typing import Annotated
from fastapi import APIRouter, Form, HTTPException, status
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from jose import jwt

static_admin_credentials = {
        "username": "admin",
        "password": "password",
}


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

router = APIRouter()

@router.post("/token")
async def login_for_access_token(
    username: Annotated[str, Form()], password: Annotated[str, Form()]
) -> Token:
    
    print(username, password)
    print(static_admin_credentials)

    if username != static_admin_credentials['username'] or password != static_admin_credentials['password']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
        

    return Token(access_token=access_token, token_type="bearer")