import os
from dotenv import load_dotenv

# Load .env values into runtime environment
load_dotenv()

class settings:
    # Shared secret used for signing and verifying HS256 JWT tokens
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")

    # HS256 is simple for standalone service
    # Later, RS256 can be used for gateway and microservice verification
    JWT_ALGORITHM: str = "HS256"

    # Database connection URL used by SQLAlchemy and Alembic
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # Google OAuth client ID used for audience validation
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")

    # Access token expiry time
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 50

    # Refresh token expiry time
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

settings = settings()