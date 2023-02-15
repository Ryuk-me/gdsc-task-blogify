from passlib.hash import bcrypt as __bcrypt
from app.database import USER_COL
from app.error_status import USER_NOT_FOUND


def hash_password(password: str):
    return __bcrypt.hash(password)


def verify_hash(password, hash):
    return __bcrypt.verify(password, hash)


def is_user_exist(username: str):
    user = USER_COL.find_one({"username": username})
    if not user:
        raise USER_NOT_FOUND
    return user
