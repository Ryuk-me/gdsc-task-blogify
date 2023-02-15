from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.schemas import token_schema
from app.Config import settings
from app import error_status as __error_status
from app.database import USER_COL

oauth2_scheme_user = OAuth2PasswordBearer(
    tokenUrl=settings.BASE_API_V1 + '/auth/user', scheme_name="USER LOGIN")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        username = payload.get("username")
        if username is None:
            raise __error_status.TOKEN_CREDENTIALS_ERROR
        token_data = token_schema.TokenData(**payload)
    except JWTError:
        raise __error_status.TOKEN_CREDENTIALS_ERROR
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme_user)):
    token = verify_token(token)
    user = USER_COL.find_one({"username": token.username})
    if not user:
        raise __error_status.TOKEN_CREDENTIALS_ERROR
    return user
