from pydantic import BaseSettings as __BaseSettings
import os
try:
    ENV = os.environ['ENV']
except:
    ENV = None


class __Settings(__BaseSettings):
    BASE_API_V1: str
    DATABASE_URI: str
    DATABASE_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    BASE_URL: str
    PORT: int

    class Config:
        env_file = ".env"


settings = __Settings()

if ENV == 'prod':
    settings.DATABASE_URI = "mongodb://mongodb:27017"
