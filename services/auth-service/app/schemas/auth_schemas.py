from pydantic import BaseModel, Field

class GoogleLoginRequest(BaseModel):
    # Google ID token received from frontend
    token: str = Field(..., description="Google id token")

    # Optional Google access token
    access_token: str | None = Field(None, description="Google Access Token (optional)")

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    picture: str | None
    emailVerified: str

    class Config:
        # Allows response models to read values from ORM/data objects
        from_attributes = True

class TokenResponse(BaseModel):
    user: UserResponse
    access: str
    refresh: str

class TokenRefreshRequest(BaseModel):
    refresh: str

class TokenRefreshResponse(BaseModel):
    access: str