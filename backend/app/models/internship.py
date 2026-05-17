"""
Internship model — v2 schema.
Additive: all original columns kept. New v2 columns appended.
v2 adds: domain, status, paid_gate_passed, fee_scam_detected,
         apply_link, apply_link_type, apply_link_valid, apply_link_checked_at,
         source (enum), source_id, last_date, sheet_synced_at, stipend_confidence,
         expires_at.
"""
from typing import Optional, List
from datetime import datetime, date
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON, Enum as saEnum
from enum import Enum
import uuid
from datetime import timezone

# ──────────────────────────────────────────────────────────────
# Enums — original (kept)
# ──────────────────────────────────────────────────────────────

class WorkMode(str, Enum):
    remote = "remote"
    hybrid = "hybrid"
    onsite = "onsite"


class IngestionMode(str, Enum):
    AUTO_SOURCE = "AUTO_SOURCE"
    MANUAL_FORM = "MANUAL_FORM"
    BULK_IMPORT = "BULK_IMPORT"


class FreshnessBucket(str, Enum):
    today = "today"
    yesterday = "yesterday"
    last_2_days = "last_2_days"
    this_week = "this_week"
    older = "older"


# ──────────────────────────────────────────────────────────────
# Enums — v2 (new)
# ──────────────────────────────────────────────────────────────

TARGET_DOMAINS = [
    "Android App Development",
    "Game Development",
    "iOS App Development",
    "Web Development",
    "Graphic Design",
    "Data Science",
]


class InternshipStatus(str, Enum):
    """v2 unified status enum (replaces is_active/is_public/verification_status)."""
    active = "active"
    expired = "expired"
    rejected = "rejected"
    draft = "draft"


class InternshipSource(str, Enum):  # source enum distinct from InternshipSource table below
    adzuna = "adzuna"
    greenhouse = "greenhouse"
    lever = "lever"
    manual = "manual"
    csv_import = "csv_import"


class ApplyLinkType(str, Enum):
    ats = "ats"
    website = "website"
    email = "email"
    unknown = "unknown"


class StipendConfidence(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


# ──────────────────────────────────────────────────────────────
# Import after enum defs to avoid circular import
# ──────────────────────────────────────────────────────────────
from app.models.company import VerificationStatus  # noqa: E402


# ──────────────────────────────────────────────────────────────
# Internship model
# ──────────────────────────────────────────────────────────────

class Internship(SQLModel, table=True):
    __tablename__: str = "internships"  # type: ignore

    # ── Primary key ──────────────────────────────────────────
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    # ── Original columns (kept as-is) ────────────────────────
    slug: str = Field(max_length=320, unique=True, index=True)
    title: str = Field(max_length=255, index=True)
    company_id: uuid.UUID = Field(foreign_key="companies.id", index=True)

    # Stipend — original
    stipend_min: Optional[float] = Field(default=None)
    stipend_max: Optional[float] = Field(default=None)
    stipend_currency: str = Field(default="INR", max_length=10)
    stipend_text: Optional[str] = Field(default=None)
    is_paid: bool = Field(default=False, index=True)
    payment_confidence: int = Field(default=0, ge=0, le=100)

    # Location — original
    work_mode: WorkMode = Field(default=WorkMode.onsite, index=True)
    country: str = Field(default="India", max_length=100)
    state: Optional[str] = Field(default=None, max_length=100, index=True)
    city: Optional[str] = Field(default=None, max_length=100, index=True)
    district: Optional[str] = Field(default=None, max_length=100)
    location_text: Optional[str] = Field(default=None)

    # Duration / description — original
    duration_text: Optional[str] = Field(default=None, max_length=255)
    duration_weeks: Optional[int] = Field(default=None)
    eligibility_text: Optional[str] = Field(default=None)
    summary: Optional[str] = Field(default=None)
    description_raw: Optional[str] = Field(default=None)

    # Apply link — original (kept; v2 adds apply_link alongside)
    apply_url: Optional[str] = Field(default=None)
    original_source_url: Optional[str] = Field(default=None)

    # Dates — original
    apply_by: Optional[date] = Field(default=None, index=True)
    registration_start: Optional[date] = Field(default=None)
    posted_at: Optional[datetime] = Field(default=None, index=True)

    # Scoring — original
    trust_score: int = Field(default=0, ge=0, le=100, index=True)
    risk_score: int = Field(default=0, ge=0, le=100)
    relevance_score: int = Field(default=0, ge=0, le=100)

    # Status — original
    verification_status: VerificationStatus = Field(
        default=VerificationStatus.draft, index=True
    )
    admin_approved: bool = Field(default=False)
    admin_approved_by: Optional[uuid.UUID] = Field(
        default=None, foreign_key="users.id"
    )
    admin_approved_at: Optional[datetime] = Field(default=None)
    admin_notes: Optional[str] = Field(default=None)

    # Source — original
    source_primary_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="sources.id"
    )
    ingestion_mode: IngestionMode = Field(default=IngestionMode.AUTO_SOURCE)

    # Flags — original
    is_active: bool = Field(default=False, index=True)
    is_public: bool = Field(default=False, index=True)
    freshness_bucket: FreshnessBucket = Field(
        default=FreshnessBucket.older, index=True
    )
    is_expiring_soon: bool = Field(default=False)
    expired_at: Optional[datetime] = Field(default=None)

    # Domain — original (slug form)
    domain_slug: Optional[str] = Field(default=None, max_length=64, index=True)

    # JSON — original
    skills: Optional[List] = Field(default=None, sa_column=Column(JSON))
    raw_payload: Optional[dict] = Field(default=None, sa_column=Column(JSON))

    # Timestamps — original
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # ── v2 NEW columns (additive, all nullable with defaults) ─
    domain: Optional[str] = Field(
        default=None,
        max_length=64,
        index=True,
        description="One of 6 TARGET_DOMAINS exactly",
    )
    status: InternshipStatus = Field(
        default=InternshipStatus.draft,
        index=True,
        description="v2 unified status: active/expired/rejected/draft",
    )
    paid_gate_passed: bool = Field(
        default=False,
        description="True only after paid gate check confirms stipend > 0 and confidence high/medium",
    )
    fee_scam_detected: bool = Field(
        default=False,
        description="True if fee/scam keywords found — permanent rejection trigger",
    )

    # v2 apply link (canonical, replaces apply_url in pipeline logic)
    apply_link: Optional[str] = Field(
        default=None,
        description="Primary apply URL — validated before activation",
    )
    apply_link_type: ApplyLinkType = Field(
        default=ApplyLinkType.unknown,
        description="Detected type: ats/website/email/unknown",
    )
    apply_link_valid: bool = Field(
        default=False,
        description="True only after link_validator.validate() passes",
    )
    apply_link_checked_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp of last link validation run",
    )

    # v2 source tracking
    source: Optional[InternshipSource] = Field(
        sa_column=Column(saEnum(InternshipSource, name="internshipsourceenum"), nullable=True),
        description="Which ingestion channel produced this internship",
    )
    source_id: Optional[str] = Field(
        default=None,
        max_length=255,
        description="External source record ID (Adzuna job ID, etc.)",
    )

    # v2 deadline (mapped from apply_by for sheet output)
    last_date: Optional[date] = Field(
        default=None,
        description="Application deadline date — drives sheet Last Date column",
    )

    # v2 sheet sync tracking
    sheet_synced_at: Optional[datetime] = Field(
        default=None,
        description="Last time this row was written to Google Sheet",
    )

    # v2 stipend confidence (replaces payment_confidence int scale)
    stipend_confidence: StipendConfidence = Field(
        default=StipendConfidence.low,
        description="Confidence level of parsed stipend: high/medium/low",
    )

    # v2 expiry tracking
    expires_at: Optional[datetime] = Field(
        default=None,
        description="Computed expiry: posted_date + duration OR source deadline",
    )


# ──────────────────────────────────────────────────────────────
# InternshipSourceLink — junction (original, kept as-is)
# Note: renamed from InternshipSource to avoid clash with
# the InternshipSource enum above.
# ──────────────────────────────────────────────────────────────

class InternshipSourceLink(SQLModel, table=True):
    __tablename__: str = "internship_sources"  # type: ignore
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    internship_id: uuid.UUID = Field(foreign_key="internships.id")
    source_id: uuid.UUID = Field(foreign_key="sources.id")
    source_url: Optional[str] = Field(default=None)
    first_seen_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
