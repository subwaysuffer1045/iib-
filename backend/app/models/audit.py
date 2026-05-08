from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
import uuid

class AuditLog(SQLModel, table=True):
    __tablename__ = "audit_logs"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    action: str = Field(max_length=100, index=True)
    resource_type: Optional[str] = Field(default=None, max_length=50)
    resource_id: Optional[uuid.UUID] = Field(default=None)
    before_data: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    after_data: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    ip_address: Optional[str] = Field(default=None, max_length=45)
    user_agent: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SuspiciousReport(SQLModel, table=True):
    __tablename__ = "suspicious_reports"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    internship_id: uuid.UUID = Field(foreign_key="internships.id", index=True)
    reported_by: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    report_reason: str = Field(max_length=50)
    report_text: Optional[str] = Field(default=None)
    auto_generated: bool = Field(default=False)
    resolved: bool = Field(default=False, index=True)
    resolved_by: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    resolved_at: Optional[datetime] = Field(default=None)
    resolution_note: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
