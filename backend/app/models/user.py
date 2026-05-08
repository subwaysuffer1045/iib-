from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from enum import Enum
import uuid

class UserRole(str, Enum):
    student = "student"
    admin = "admin"

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    password_hash: str = Field(max_length=255)
    role: UserRole = Field(default=UserRole.student)
    is_active: bool = Field(default=False)
    is_verified: bool = Field(default=False)
    email_verified_at: Optional[datetime] = Field(default=None)
    last_login_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def is_superuser(self) -> bool:
        return self.role == UserRole.admin

class UserProfile(SQLModel, table=True):
    __tablename__ = "user_profiles"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", unique=True)
    full_name: Optional[str] = Field(default=None, max_length=255)
    phone: Optional[str] = Field(default=None, max_length=20)
    college_id: Optional[uuid.UUID] = Field(default=None, foreign_key="colleges.id")
    graduation_year: Optional[int] = Field(default=None)
    degree: Optional[str] = Field(default=None, max_length=100)
    branch: Optional[str] = Field(default=None, max_length=100)
    dpdp_consent_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Consent(SQLModel, table=True):
    __tablename__ = "consents"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    consent_type: str = Field(max_length=50)
    version: str = Field(max_length=20)
    consented: bool
    consented_at: datetime = Field(default_factory=datetime.utcnow)
    ip_address: Optional[str] = Field(default=None, max_length=45)
    user_agent: Optional[str] = Field(default=None)
