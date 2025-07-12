from sqlalchemy import Column, String, Boolean, Enum, ForeignKey, LargeBinary, Integer, Identity
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
import uuid
from app.db import Base

class UserRole(enum.Enum):
    ops = "ops"
    client = "client"

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, index=True)
    password_hash = Column(String)
    role = Column(Enum(UserRole))
    is_verified = Column(Boolean, default=False)

class File(Base):
    __tablename__ = "files"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    optionID = Column(Integer, Identity(start=1), unique=True, nullable=False)
    filename = Column(String)
    content = Column(LargeBinary)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    uploader = relationship("User", backref="uploaded_files")