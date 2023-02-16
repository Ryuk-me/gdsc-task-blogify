from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health, limit
from app.routers.v1 import user, blog, auth
import app.database
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from app.Config import settings

app = FastAPI(
    title="Blogify-API",
    version="1.1",
)

origins = [
    '127.0.0.1',
    '0.0.0.0',
    'localhost',
    "http://localhost:8009",
    'http://127.0.0.1:8009', 'http://127.0.0.1:8009/*',
]

# origins = ["*"]


@app.on_event("startup")
async def startup():
    pool = redis.ConnectionPool(
        host=settings.REDIS_HOST,
        port=6379,
        decode_responses=True,
        encoding="utf-8",
    )

    init_redis = redis.Redis(connection_pool=pool)
    await FastAPILimiter.init(init_redis)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(limit.router)
app.include_router(user.router)
app.include_router(blog.router)
app.include_router(auth.router)
