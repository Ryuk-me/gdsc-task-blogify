from pydantic import validator, constr, BaseModel as __BaseModel
from datetime import datetime
from typing import Optional
from bson import ObjectId


class BlogCreate(__BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None
    author: Optional[constr(
        min_length=6, regex="^[A-Za-z][A-Za-z0-9_]{6,20}$", max_length=20)] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @validator("created_at", pre=True, always=True)
    def generate_created_at(cls, created_at: datetime) -> datetime:
        created_at = datetime.now()
        return created_at

    @validator("updated_at", pre=True, always=True)
    def generate_updated_at(cls, updated_at: datetime) -> datetime:
        updated_at = datetime.now()
        return updated_at

    @validator("content", pre=True)
    def trim_spaces_content(cls, content: str) -> str:
        content = content.strip()
        return content

    @validator("title", pre=True)
    def trim_spaces_title(cls, title: str) -> str:
        title = title.strip()
        return title

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateBlog(__BaseModel):
    title: str
    content: str
    author: Optional[constr(
        min_length=6, regex="^[A-Za-z][A-Za-z0-9_]{6,20}$", max_length=20)] = None
    updated_at: Optional[datetime]

    @validator("updated_at", pre=True, always=True)
    def generate_updated_at(cls, updated_at: datetime) -> datetime:
        updated_at = datetime.now()
        return updated_at

    @validator("content", pre=True)
    def trim_spaces_content(cls, content: str) -> str:
        content = content.strip()
        return content

    @validator("title", pre=True)
    def trim_spaces_title(cls, title: str) -> str:
        title = title.strip()
        return title

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
