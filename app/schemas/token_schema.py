from pydantic import BaseModel
from typing import Optional, Literal


class BaseToken(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
