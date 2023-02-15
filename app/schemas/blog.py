from pydantic import Field, BaseModel as __BaseModel
from datetime import datetime
from bson import ObjectId
from typing import Optional
from app.helper.pyobjectid import PyObjectId

# https://www.mongodb.com/developer/languages/python/python-quickstart-fastapi/


class Blogout(__BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    content: str
    image_url: Optional[str] = None
    author: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
