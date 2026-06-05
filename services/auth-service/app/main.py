from fastapi import FastAPI
from app.core.database import engine, Base
from app.db.user_model import DBUser
from app.api.v1 import routes
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    App lifecycle manager.

    Why yield?
    - Before yield: startup logic runs
    - After yield: shutdown logic can run
    """
    # Create tables on startup
    Base.metadata.create_all(bind=engine)
    yield
    # Future shutdown cleanup can be added here

app = FastAPI(
    title="Auth Microservice",
    version="1.0.0",
    description="Handles user authentication, Google OAuth, and JWT management.",
    # lifespan=lifespan
)

origins = [
    "http://localhost:3000",
    "http://gateway:8000",
]

app.include_router(routes.router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return {"message": "auth service is running"}