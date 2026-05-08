from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
import uuid

class College(SQLModel, table=True):
    __tablename__ = "colleges"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    city: Optional[str] = Field(default=None, max_length=100)
    state: Optional[str] = Field(default=None, max_length=100)
    website: Optional[str] = Field(default=None, max_length=255)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CollegeEmailDomain(SQLModel, table=True):
    __tablename__ = "college_email_domains"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    college_id: uuid.UUID = Field(foreign_key="colleges.id")
    domain: str = Field(max_length=100, unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
