import pymongo as __pymongo
from app.Config import settings as __settings

__client = __pymongo.MongoClient(__settings.DATABASE_URI)

DB = __client["blogify"]

if "user" and "blog" not in DB.list_collection_names():
    USER_COL = DB.create_collection("user")
    BLOG_COL = DB.create_collection("blog")
else:
    USER_COL = DB.get_collection("user")
    BLOG_COL = DB.get_collection("blog")
