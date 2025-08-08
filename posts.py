from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, Query
from sqlmodel import Session, select
import os
from typing import List
from ..database import get_session
from ..models import Post
from ..schemas import PostCreate, PostRead
from ..auth import get_current_user
from ..config import settings

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=PostRead, status_code=201)
async def create_post(data: PostCreate, file: UploadFile | None = File(None), session: Session = Depends(get_session), current_user = Depends(get_current_user)):
    image_path = None
    if file:
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        filename = f"{int(__import__('time').time()*1000)}_{file.filename}"
        dest = os.path.join(settings.UPLOAD_DIR, filename)
        contents = await file.read()
        with open(dest, "wb") as f:
            f.write(contents)
        image_path = dest
    post = Post(title=data.title, description=data.description, image_path=image_path, author_id=current_user.id)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

@router.get("/", response_model=List[PostRead])
def list_posts(skip: int = 0, limit: int = Query(10, le=100), author: int | None = None, session: Session = Depends(get_session)):
    if author:
        statement = select(Post).where(Post.author_id == author).offset(skip).limit(limit)
    else:
        statement = select(Post).offset(skip).limit(limit)
    posts = session.exec(statement).all()
    return posts

@router.get("/{post_id}", response_model=PostRead)
def get_post(post_id: int, session: Session = Depends(get_session)):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}", response_model=PostRead)
def update_post(post_id: int, data: PostCreate, session: Session = Depends(get_session), current_user = Depends(get_current_user)):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    post.title = data.title
    post.description = data.description
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

@router.delete("/{post_id}", status_code=204)
def delete_post(post_id: int, session: Session = Depends(get_session), current_user = Depends(get_current_user)):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    if post.image_path and os.path.exists(post.image_path):
        try:
            os.remove(post.image_path)
        except Exception:
            pass
    session.delete(post)
    session.commit()
    return None
