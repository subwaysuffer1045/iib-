from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from enum import Enum
import uuid

class CrawlStatus(str, Enum):
    queued = "queued"
    running = "running"
    success = "success"
    failed = "failed"
    partial = "partial"

class CrawlJob(SQLModel, table=True):
    __tablename__ = "crawl_jobs"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    source_id: uuid.UUID = Field(foreign_key="sources.id", index=True)
    celery_task_id: Optional[str] = Field(default=None, max_length=100)
    status: CrawlStatus = Field(default=CrawlStatus.queued, index=True)
    triggered_by: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    trigger_mode: str = Field(default="scheduled", max_length=20)
    pages_fetched: int = Field(default=0)
    cards_parsed: int = Field(default=0)
    candidates_created: int = Field(default=0)
    published_count: int = Field(default=0)
    rejected_count: int = Field(default=0)
    review_count: int = Field(default=0)
    started_at: Optional[datetime] = Field(default=None)
    finished_at: Optional[datetime] = Field(default=None)
    error_log: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CrawlLog(SQLModel, table=True):
    __tablename__ = "crawl_logs"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    crawl_job_id: uuid.UUID = Field(foreign_key="crawl_jobs.id", index=True)
    level: str = Field(max_length=10)
    message: str
    logged_at: datetime = Field(default_factory=datetime.utcnow)

class ParserFailure(SQLModel, table=True):
    __tablename__ = "parser_failures"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    source_id: uuid.UUID = Field(foreign_key="sources.id", index=True)
    crawl_job_id: Optional[uuid.UUID] = Field(default=None, foreign_key="crawl_jobs.id")
    failure_type: Optional[str] = Field(default=None, max_length=50)
    raw_url: Optional[str] = Field(default=None)
    error_message: str
    stack_trace: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
