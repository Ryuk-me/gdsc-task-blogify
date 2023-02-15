from pydantic import BaseModel as __BaseModel
from datetime import datetime
from bson import ObjectId


class UserOut(__BaseModel):
    username: str
    created_at: datetime

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
