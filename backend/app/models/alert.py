from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
import uuid

class UserAlertPreference(SQLModel, table=True):
    __tablename__ = "user_alert_preferences"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", unique=True)
    alert_new_matches: bool = Field(default=True)
    alert_expiring_saved: bool = Field(default=True)
    alert_frequency: str = Field(default="daily", max_length=20)
    alert_domains: Optional[List] = Field(default=None, sa_column=Column(JSON))
    alert_regions: Optional[List] = Field(default=None, sa_column=Column(JSON))
    alert_stipend_min: Optional[float] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
