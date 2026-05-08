from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from enum import Enum
import uuid

class SourceType(str, Enum):
    api = "api"
    html = "html"
    browser = "browser"
    manual = "manual"

class PolicyStatus(str, Enum):
    approved = "approved"
    pending = "pending"
    blocked = "blocked"

class ActivationState(str, Enum):
    enabled = "enabled"
    conditional = "conditional"
    disabled = "disabled"

class Source(SQLModel, table=True):
    __tablename__ = "sources"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    source_name: str = Field(max_length=100, unique=True)
    base_url: str
    source_type: SourceType
    policy_status: PolicyStatus = Field(default=PolicyStatus.pending)
    activation_state: ActivationState = Field(default=ActivationState.disabled)
    parser_name: Optional[str] = Field(default=None, max_length=100)
    crawl_mode: Optional[str] = Field(default=None, max_length=50)
    crawl_interval_minutes: int = Field(default=720)
    robots_txt_cached: Optional[str] = Field(default=None)
    robots_txt_checked_at: Optional[datetime] = Field(default=None)
    last_crawl_at: Optional[datetime] = Field(default=None)
    last_success_at: Optional[datetime] = Field(default=None)
    last_failure_at: Optional[datetime] = Field(default=None)
    last_failure_reason: Optional[str] = Field(default=None)
    consecutive_failures: int = Field(default=0)
    total_crawls: int = Field(default=0)
    total_parsed: int = Field(default=0)
    total_published: int = Field(default=0)
    notes: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class SourcePolicy(SQLModel, table=True):
    __tablename__ = "source_policies"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    source_id: uuid.UUID = Field(foreign_key="sources.id", unique=True)
    allow_html_scrape: bool = Field(default=False)
    allow_api_call: bool = Field(default=False)
    allow_browser: bool = Field(default=False)
    rate_limit_rph: int = Field(default=60)
    respect_robots: bool = Field(default=True)
    user_agent_str: str = Field(default="IIBIndiaBot/1.0", max_length=255)
    policy_notes: Optional[str] = Field(default=None)
    approved_by: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    approved_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
