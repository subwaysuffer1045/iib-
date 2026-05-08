from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
from enum import Enum
import uuid

class ImportRowStatus(str, Enum):
    pending = "pending"
    valid = "valid"
    invalid = "invalid"
    imported = "imported"
    duplicate = "duplicate"

class ImportBatch(SQLModel, table=True):
    __tablename__ = "import_batches"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    imported_by: uuid.UUID = Field(foreign_key="users.id")
    file_name: Optional[str] = Field(default=None, max_length=255)
    file_size_bytes: Optional[int] = Field(default=None)
    row_count: int = Field(default=0)
    valid_count: int = Field(default=0)
    invalid_count: int = Field(default=0)
    imported_count: int = Field(default=0)
    duplicate_count: int = Field(default=0)
    status: str = Field(default="preview", max_length=20)
    confirmed_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ImportRow(SQLModel, table=True):
    __tablename__ = "import_rows"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    batch_id: uuid.UUID = Field(foreign_key="import_batches.id", index=True)
    row_number: int
    raw_data: dict = Field(sa_column=Column(JSON))
    parsed_data: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    validation_errors: Optional[List] = Field(default=None, sa_column=Column(JSON))
    status: ImportRowStatus = Field(default=ImportRowStatus.pending, index=True)
    internship_id: Optional[uuid.UUID] = Field(default=None, foreign_key="internships.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
