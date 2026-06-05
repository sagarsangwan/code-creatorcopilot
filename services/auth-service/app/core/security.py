from datetime import timedelta, timezone, datetime

# jose library is used for JWT operations
# jwt provides encode/decode functions
# JWTError handles token validation errors
from jose import JWTError, jwt

from app.core.config import settings

# Official Google token verification utilities
from google.oauth2 import id_token
from google.auth.transport.requests import (
    Request as GoogleAuthRequest,
)  # Alias used to avoid naming conflict

# Reusable request object for Google certificate validation
google_request = GoogleAuthRequest()

def create_access_token(data: dict):
    """
    Creates a short-lived access token.
    """
    to_encode = data.copy()
    expire = datetime.now((timezone.utc)) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    expire_timestamp = int(expire.timestamp())

    # Current project uses custom `expire` key for access token expiry
    to_encode.update({"expire": expire_timestamp, "type": "access"})

    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt

def create_refresh_token(data: dict):
    """
    Creates a long-lived refresh token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    expire_timestamp = int(expire.timestamp())

    # `exp` is the standard JWT expiry claim
    to_encode.update({"exp": expire_timestamp, "type": "refresh"})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt

def decode_token(token: str):
    """
    Decodes a JWT token and returns None for invalid tokens.
    """
    try:
        payload = jwt.decode(
            token=token, key=settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM
        )
        return payload
    except JWTError:
        return None

def verify_refresh_token(refresh_token: str):
    """
    Verifies whether the refresh token is valid.
    """
    payload = decode_token(refresh_token)
    if payload and payload.get("type") == "refresh":
        return payload
    return None

def decode_google_id_token_secure(id_token_str: str) -> dict:
    """
    Securely verifies Google ID token:
    signature, audience, expiry, and issuer.
    """
    try:
        id_info = id_token.verify_oauth2_token(
            id_token_str,
            google_request,
            settings.GOOGLE_CLIENT_ID,
            clock_skew_in_seconds=30,
        )

        if id_info["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
            raise ValueError("Wrong issuer.")

        return id_info

    except ValueError as e:
        raise ValueError(f"Google ID Token verification failed: {e}")
    except Exception as e:
        raise ValueError(f"Error during Google cert fetch: {e}")