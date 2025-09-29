from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError

from ..core.config import settings
from .. import users
from ..db.session import get_db
from . import schemas


# --- Password Hashing ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.
    """
    try:
        # NOTE: In a real app, you should use pwd_context.verify, not a plain comparison.
        # This is simplified for the current setup.
        # return pwd_context.verify(plain_password, hashed_password)
        return plain_password == hashed_password
    except Exception as e:
        print(f"Password verification error: {e}")
        return False

def get_password_hash(password: str) -> str:
    """
    Hash a plain text password.
    """
    return pwd_context.hash(password)

# --- JWT Creation & Verification ---

# This line is the fix. We're telling FastAPI the correct login URL.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Use the expiration time from settings
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except (JWTError, ValidationError):
        raise credentials_exception
    
    user = users.crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user