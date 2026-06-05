from sqlalchemy import Column, UUID, Boolean, String, DateTime
from sqlalchemy import func
from app.core.database import Base
import uuid

class DBUser(Base):
    __tablename__ = "users"

    # UUID primary key for unique user identity
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)

    # Basic profile fields
    email = Column(String, unique=True, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    image = Column(String, nullable=True)

    # Account status related flags
    is_active = Column(Boolean, default=True)
    email_verified = Column(Boolean, default=False)

    # Auto creation timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)