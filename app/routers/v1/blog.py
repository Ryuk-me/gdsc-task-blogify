from fastapi import UploadFile, File
from fastapi import status as __status, APIRouter as __APIRouter, Depends
from app.Config import settings as __settings
from app.models import blog as __blog_model, user as user_model
from app.database import USER_COL as __USER_COL, BLOG_COL as __BLOG_COL
from app import error_status as __error_status
from app.schemas import blog as __blog_schema
from bson import ObjectId, errors
from typing import List, Optional
from app.auth import get_current_user


router = __APIRouter(
    prefix=__settings.BASE_API_V1 + "/blog",
    tags=['Blog Route'],
    redirect_slashes=False
)


@router.put("/", status_code=__status.HTTP_202_ACCEPTED, response_model=__blog_schema.Blogout)
async def __update_blog(id: str, blog: __blog_model.UpdateBlog, current_user: user_model.User = Depends(get_current_user)):
    try:
        # filter = {
        #     "$and": [{"_id": ObjectId(id)}, {"author": current_user["username"]}]}
        filter = {"_id": ObjectId(id), "author": current_user["username"]}
    except errors.InvalidId:
        raise __error_status.INVALID_ID
    found_row = __BLOG_COL.find_one(filter)
    if not found_row:
        raise __error_status.BLOG_NOT_FOUND
    if not __USER_COL.find_one({"username": current_user["username"]}):
        raise __error_status.USER_NOT_FOUND

    new_vals = {"$set": {"author": current_user["username"], "title": blog.title,
                         "content": blog.content, "updated_at": blog.updated_at}}
    updated_blog = __BLOG_COL.update_one(filter, new_vals)
    rt_blog = __BLOG_COL.find_one({"_id": ObjectId(id)})
    return rt_blog


@router.delete("/", status_code=__status.HTTP_202_ACCEPTED)
async def __delete_blog(id: str, current_user: user_model.User = Depends(get_current_user)):
    try:
        filter = {"_id": ObjectId(id), "author": current_user["username"]}
    except errors.InvalidId:
        raise __error_status.INVALID_ID

    found_row = __BLOG_COL.find_one(filter)
    if not found_row:
        raise __error_status.BLOG_NOT_FOUND

    deleted_blog = __BLOG_COL.delete_one(filter)
    return {"detail": "blog deleted"}


@router.post("/", status_code=__status.HTTP_201_CREATED, response_model=__blog_schema.Blogout)
async def __create_blog(blog: __blog_model.BlogCreate, current_user: user_model.User = Depends(get_current_user)):
    if __USER_COL.find_one({"username": current_user["username"]}):
        blog.author = current_user["username"]
        inserted_blog = __BLOG_COL.insert_one(blog.dict())
        rt_blog = __BLOG_COL.find_one(inserted_blog.inserted_id)
        return rt_blog

    raise __error_status.USER_NOT_FOUND


@router.get("/all", status_code=__status.HTTP_200_OK, response_model=List[__blog_schema.Blogout], description="This will show all blogs by limit")
async def __get_all_blogs(limit: Optional[int] = None, current_user: user_model.User = Depends(get_current_user)):
    if limit:
        all_blogs = __BLOG_COL.find({}).limit(limit)
    else:
        all_blogs = __BLOG_COL.find({})
    l = []
    for b in all_blogs:
        b["_id"] = str(b["_id"])
        l.append(b)
    if len(l) > 0:
        return l
    raise __error_status.NO_RESULT_FOUND


@router.get("/search", status_code=__status.HTTP_200_OK, response_model=List[__blog_schema.Blogout], description="This will search for blog by title")
async def __get_blogs_by_title(title: str, limit: Optional[int] = None, current_user: user_model.User = Depends(get_current_user)):
    title = title.strip()
    if title == '':
        raise __error_status.INVALID_TITLE
    else:
        __BLOG_COL.create_index([('title', 'text'), ('content', 'text')])
        if limit:
            search_result = __BLOG_COL.find(
                {"$text": {"$search": title}}).limit(limit)
        else:
            search_result = __BLOG_COL.find({"$text": {"$search": title}})
        l = []
        for b in search_result:
            b["_id"] = str(b["_id"])
            l.append(b)
        if len(l) > 0:
            return l
        raise __error_status.NO_RESULT_FOUND


@router.post("/image", status_code=__status.HTTP_202_ACCEPTED, response_model=__blog_schema.Blogout)
async def __image_upload(id: str, in_file: UploadFile = File(...), current_user: user_model.User = Depends(get_current_user)):

    try:
        filter = {"_id": ObjectId(id), "author": current_user["username"]}
    except errors.InvalidId:
        raise __error_status.INVALID_ID
    found_row = __BLOG_COL.find_one(filter)
    if not found_row:
        raise __error_status.BLOG_NOT_FOUND
    if not __USER_COL.find_one({"username": current_user["username"]}):
        raise __error_status.USER_NOT_FOUND

    import base64
    from datetime import datetime

    encoded_string = base64.b64encode(in_file.file.read())
    print(encoded_string)
    __BLOG_COL.update_one(filter, {"$set": {
                          "author": current_user["username"], "image_url": encoded_string, "updated_at": datetime.now()}})
    rt = __BLOG_COL.find_one({"_id": ObjectId(id)})
    return rt
