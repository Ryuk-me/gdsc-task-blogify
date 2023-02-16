from fastapi import status as __status, APIRouter as __APIRouter, Depends
from app.Config import settings as __settings
from app.models import user as __user_model
from app.database import BLOG_COL as __BLOG_COL, USER_COL as __USER_COL
from app import error_status as __error_status
from app import services as __services
from app.schemas import blog as __blog_schema, user as __user_schema
from app.auth import get_current_user
from typing import List

router = __APIRouter(
    prefix=__settings.BASE_API_V1 + "/user",
    tags=['User Route'],
    redirect_slashes=False
)


@router.get("/", status_code=__status.HTTP_302_FOUND, response_model=__user_schema.UserOut)
async def __get_user_by_username(username: str, current_user: __user_model.User = Depends(get_current_user)):
    user = __USER_COL.find_one({"username": username})
    if user:
        return user
    else:
        raise __error_status.USER_NOT_FOUND


@router.post('/', status_code=__status.HTTP_201_CREATED,)
async def __create_user(user: __user_model.UserCreate):
    if __USER_COL.find_one({"username": user.username}):
        raise __error_status.USER_ALREADY_EXIST
    user.password = __services.hash_password(user.password)
    inserted_user = __USER_COL.insert_one(user.dict())
    return {"detail": "account created"}


@router.get("/blogs", status_code=__status.HTTP_200_OK, response_model=List[__blog_schema.Blogout], description="This will show only author posts")
async def __get_all_blogs_by_author(current_user: __user_model.User = Depends(get_current_user)):
    if not __USER_COL.find_one({"username": current_user["username"]}):
        raise __error_status.USER_NOT_FOUND
    all_blogs = __BLOG_COL.find({"author": current_user["username"]})
    l = []
    for b in all_blogs:
        b["_id"] = str(b["_id"])
        l.append(b)
    if len(l) > 0:
        return l
    raise __error_status.NO_RESULT_FOUND
