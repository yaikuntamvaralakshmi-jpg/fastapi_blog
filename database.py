from sqlmodel import create_engine, SQLModel, Session
from .config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
