from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health
from app.routers.v1 import user, blog, auth
import app.database

app = FastAPI(
    title="Blogify-API",
    version="1.1",
)

origins = [
    '127.0.0.1',
    '0.0.0.0',
    'localhost',
    "http://localhost:3000",
    'http://127.0.0.1:8009', 'http://127.0.0.1:8009/*',
]

# origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(user.router)
app.include_router(blog.router)
app.include_router(auth.router)
