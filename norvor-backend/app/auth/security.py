from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
import hashlib
from ..core.config import settings

# --- Password Hashing ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _prepare_password(password: str) -> str:
    """
    Prepare password for bcrypt by pre-hashing if it's too long.
    This ensures we never hit the 72-byte limit while maintaining security.
    """
    password_bytes = password.encode('utf-8')
    
    # If password is longer than 72 bytes, pre-hash it with SHA-256
    if len(password_bytes) > 72:
        # Use SHA-256 to reduce long passwords to a fixed length
        return hashlib.sha256(password_bytes).hexdigest()
    
    return password

def verify_password(plain_password: str, hashed_password: str) -> bool:
    prepared_password = _prepare_password(plain_password)
    return pwd_context.verify(prepared_password, hashed_password)

def get_password_hash(password: str) -> str:
    prepared_password = _prepare_password(password)
    return pwd_context.hash(prepared_password)

# --- JWT Creation ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt