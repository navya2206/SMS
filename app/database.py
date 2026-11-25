# app/database.py

from sqlmodel import SQLModel, Session, create_engine

from app.config import settings

# Import all models to register their tables
import app.models


# SQLite connection configuration
connect_args = {}

if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {
        "check_same_thread": False
    }


# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    connect_args=connect_args
)


# Create all database tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Database session dependency
def get_session():
    with Session(engine) as session:
        yield session