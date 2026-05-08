from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
import uuid

class UserSavedInternship(SQLModel, table=True):
    __tablename__ = "user_saved_internships"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    internship_id: uuid.UUID = Field(foreign_key="internships.id")
    notes: Optional[str] = Field(default=None)
    saved_at: datetime = Field(default_factory=datetime.utcnow)

class UserApplicationTracker(SQLModel, table=True):
    __tablename__ = "user_application_tracker"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    internship_id: uuid.UUID = Field(foreign_key="internships.id")
    status: str = Field(default="applied", max_length=30)
    applied_at: Optional[datetime] = Field(default=None)
    notes: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
