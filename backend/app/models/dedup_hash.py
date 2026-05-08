"""
DedupHash model — v2 new table.
Stores exact SHA256 and fuzzy hashes for internship deduplication.
"""
from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
import uuid


class DedupHash(SQLModel, table=True):
    __tablename__: str = "dedup_hashes"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    internship_id: uuid.UUID = Field(
        foreign_key="internships.id",
        index=True,
        description="FK to the internship this hash belongs to",
    )
    hash_exact: str = Field(
        max_length=64,
        unique=True,
        index=True,
        description="SHA256(company_domain|title.lower()|domain|source_id)",
    )
    hash_fuzzy: Optional[str] = Field(
        default=None,
        max_length=64,
        index=True,
        description="SHA256(sorted filtered title words) — for Jaccard similarity check",
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
