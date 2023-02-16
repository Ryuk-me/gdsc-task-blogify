from fastapi import Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.Config import settings
from app import services as __services
from app import error_status as __error_status
from app.auth import create_access_token
from app.schemas import token_schema
from app.models import user as user_model
from datetime import timedelta
import re
from fastapi_limiter.depends import RateLimiter

router = APIRouter(
    prefix=settings.BASE_API_V1 + '/auth',
    tags=['Authentication'],
    redirect_slashes=False
)


@router.post('/user', response_model=token_schema.BaseToken, dependencies=[Depends(RateLimiter(times=1, seconds=5))])
async def user_login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    user_credentials.username = user_credentials.username.lower()
    isNone = re.match(
        r'^[A-Za-z][A-Za-z0-9_]{6,20}$', user_credentials.username)
    if isNone:
        user_exist = __services.is_user_exist(user_credentials.username)
        if __services.verify_hash(user_credentials.password, user_exist["password"]):
            expire_time = timedelta(minutes=int(
                settings.ACCESS_TOKEN_EXPIRE_MINUTES))
            token = create_access_token(
                data={"username": user_exist["username"]}, expires_delta=expire_time)
            return {"access_token": token, "token_type": "bearer"}
    else:
        raise __error_status.INVALID_USERNAME
    raise __error_status.TOKEN_CREDENTIALS_ERROR
