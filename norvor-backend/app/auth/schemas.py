from pydantic import BaseModel
from typing import Optional

# --- Schema for the data we send back to the user ---
class Token(BaseModel):
    access_token: str
    token_type: str

# --- Schema for the data encoded inside the JWT ---
class TokenData(BaseModel):
    email: Optional[str] = None