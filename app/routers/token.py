from functools import wraps
from typing import Annotated
from fastapi import APIRouter, Form, HTTPException, status
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.config.settings import Settings

settings = Settings()

# static_admin_credentials = {
#         "username": "admin",
#         "password": "password",
# }


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
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
    return encoded_jwt

router = APIRouter()

@router.post("/login")
async def login_for_access_token(
    username: Annotated[str, Form()], password: Annotated[str, Form()]
) -> Token:
    
    if username != settings.admin_username or password != settings.admin_password:
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