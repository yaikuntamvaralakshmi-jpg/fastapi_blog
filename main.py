from fastapi import FastAPI # type: ignore
from fastapi.staticfiles import StaticFiles # type: ignore
from .database import init_db
from .routers import auth as auth_router, posts as posts_router
from .config import settings
import os

app = FastAPI(title="FastAPI Blog Internship Task")

@app.on_event("startup")
def on_startup():
    init_db()
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

app.include_router(auth_router.router)
app.include_router(posts_router.router)

@app.get("/")
def read_root():
    return {"message": "FastAPI Blog API - see /docs for Swagger UI"}
