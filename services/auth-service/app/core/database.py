from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings

# Create a reusable database engine
engine = create_engine(url=settings.DATABASE_URL, pool_pre_ping=True)

# Session factory used for creating database sessions per request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class used by SQLAlchemy models
Base = declarative_base()

def get_db():
    """
    FastAPI dependency for DB session.

    Why yield?
    - Before yield: session opens
    - After request completes: session closes in finally block
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()