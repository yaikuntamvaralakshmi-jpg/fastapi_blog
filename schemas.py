from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class PostCreate(BaseModel):
    title: str
    description: str

class PostRead(BaseModel):
    id: int
    title: str
    description: str
    image_path: Optional[str]
    author_id: int
    created_at: datetime

    class Config:
        orm_mode = True
