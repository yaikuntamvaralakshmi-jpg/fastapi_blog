from sqlmodel import Session, select
from .models import User, Post

def get_user_by_email(session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

def create_post(session: Session, post: Post) -> Post:
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

def get_post(session: Session, post_id: int) -> Post | None:
    return session.get(Post, post_id)

def delete_post(session: Session, post: Post):
    session.delete(post)
    session.commit()

def update_post(session: Session, db_post: Post, data: dict) -> Post:
    for k, v in data.items():
        setattr(db_post, k, v)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post
