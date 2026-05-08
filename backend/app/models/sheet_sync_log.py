"""
SheetSyncLog model — v2 new table.
Records every Google Sheet sync run for audit/debugging.
"""
from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from enum import Enum
import uuid


class SyncStatus(str, Enum):
    success = "success"
    partial = "partial"
    failed = "failed"


class SheetSyncLog(SQLModel, table=True):
    __tablename__: str = "sheet_sync_log"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    sheet_tab: str = Field(
        max_length=64,
        index=True,
        description="Google Sheet tab name: 'APP ANDROID', 'Game development', etc.",
    )
    rows_written: int = Field(
        default=0,
        description="Number of active internship rows written to the tab",
    )
    rows_expired: int = Field(
        default=0,
        description="Number of rows moved to EXPIRED tab in this sync",
    )
    rows_rejected: int = Field(
        default=0,
        description="Number of rows in REJECTED tab during this sync",
    )
    sync_status: SyncStatus = Field(
        default=SyncStatus.success,
        description="Overall outcome of this sync run",
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Error detail if sync_status is partial or failed",
    )
    synced_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        index=True,
        description="UTC timestamp when this sync ran",
    )
