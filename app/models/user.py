from pydantic import constr, validator, BaseModel as __BaseModel
from datetime import datetime
from typing import Optional
from bson import ObjectId


class UserCreate(__BaseModel):
    username: constr(
        min_length=6, regex="^[A-Za-z][A-Za-z0-9_]{6,20}$", max_length=20)
    password: constr(min_length=8, max_length=20)
    created_at: Optional[datetime]

    @validator("username", pre=True)
    def username_is_valid(cls, username: str) -> str:
        return username.lower()

    @validator("created_at", pre=True, always=True)
    def generate_created_at(cls, created_at: datetime) -> datetime:
        created_at = datetime.now()
        return created_at

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class User(__BaseModel):
    username: constr(
        min_length=6, regex="^[A-Za-z][A-Za-z0-9_]{6,20}$", max_length=20)
