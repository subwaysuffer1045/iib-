"""
Company model — v2 schema.
Additive: all original columns kept. New v2 columns appended.
v2 adds: name (display alias), domain (unique), hard_fail_reason,
         mca21_verified, gstin_verified, startup_india_verified,
         ats_detected, whois_domain_age_days, signal_count, ai_summary.
trust_score CHECK (<=85) enforced at application layer (DB constraint via migration).
"""
from typing import Optional
from datetime import datetime, date
from sqlmodel import SQLModel, Field
from enum import Enum
import uuid
from datetime import timezone


# ──────────────────────────────────────────────────────────────
# Enums — original (kept)
# ──────────────────────────────────────────────────────────────

class VerificationStatus(str, Enum):
    draft = "draft"
    pending = "pending"
    needs_review = "needs_review"
    verified = "verified"
    rejected = "rejected"


class AtsType(str, Enum):
    greenhouse = "greenhouse"
    lever = "lever"
    ashby = "ashby"
    workday = "workday"
    none = "none"
    unknown = "unknown"


class CheckStatus(str, Enum):
    passed = "passed"
    failed = "failed"
    not_run = "not_run"
    infra_error = "infra_error"


# ──────────────────────────────────────────────────────────────
# Company model
# ──────────────────────────────────────────────────────────────

class Company(SQLModel, table=True):
    __tablename__: str = "companies"  # type: ignore

    # ── Primary key ──────────────────────────────────────────
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    # ── Original columns (kept as-is) ────────────────────────
    canonical_name: str = Field(max_length=255)
    slug: str = Field(max_length=255, unique=True, index=True)
    website: Optional[str] = Field(default=None)
    careers_url: Optional[str] = Field(default=None)
    email_domain: Optional[str] = Field(default=None, max_length=100)
    ats_type: AtsType = Field(default=AtsType.unknown)
    ats_domain: Optional[str] = Field(default=None, max_length=255)

    # MCA/GSTIN — original (raw data fields)
    mca_cin: Optional[str] = Field(default=None, max_length=21)
    mca_cin_source: Optional[str] = Field(default=None, max_length=30)
    mca_cin_verified_at: Optional[datetime] = Field(default=None)
    gstin: Optional[str] = Field(default=None, max_length=15)
    gstin_source: Optional[str] = Field(default=None, max_length=30)
    gstin_verified_at: Optional[datetime] = Field(default=None)
    gstin_trade_name: Optional[str] = Field(default=None, max_length=255)
    startup_india_id: Optional[str] = Field(default=None, max_length=100)

    # WHOIS — original
    domain_age_days: Optional[int] = Field(default=None)
    whois_creation_date: Optional[date] = Field(default=None)
    whois_provider_used: Optional[str] = Field(default=None, max_length=30)
    whois_checked_at: Optional[datetime] = Field(default=None)

    # Status / scoring — original
    company_verified: bool = Field(default=False)
    verification_status: VerificationStatus = Field(
        default=VerificationStatus.draft
    )
    trust_score: int = Field(
        default=0,
        ge=0,
        le=100,
        description="Automated max = 85. Only admin override-score can push above 85.",
    )
    risk_score: int = Field(default=50, ge=0, le=100)
    verification_confidence: str = Field(default="low", max_length=10)
    evidence_count: int = Field(default=0)
    confirmed_signals: int = Field(default=0)
    reputation_summary: Optional[str] = Field(default=None)
    last_verified_at: Optional[datetime] = Field(default=None)

    # Scam flags — original
    has_payment_demand: bool = Field(default=False)
    payment_demand_reason: Optional[str] = Field(default=None)

    # Timestamps — original
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # ── v2 NEW columns (additive, all nullable / with defaults) ──

    # v2 display name (canonical_name is the slug-safe name; name is the display label)
    name: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Human-readable display name for company (sheet Column B, UI display)",
    )

    # v2 primary domain (unique website domain, e.g. 'example.com')
    domain: Optional[str] = Field(
        default=None,
        max_length=255,
        index=True,
        description="Unique company domain used for verification checks and dedup hash",
    )

    # v2 hard-fail permanent rejection reason
    hard_fail_reason: Optional[str] = Field(
        default=None,
        description="Set on permanent rejection (fee scam / blacklist). Cannot be cleared.",
    )

    # v2 verification signal booleans
    mca21_verified: bool = Field(
        default=False,
        description="True when MCA21 lookup confirms active CIN",
    )
    gstin_verified: bool = Field(
        default=False,
        description="True when GST portal confirms active GSTIN",
    )
    startup_india_verified: bool = Field(
        default=False,
        description="True when DPIIT/Startup India registry confirms registration",
    )
    ats_detected: bool = Field(
        default=False,
        description="True when apply link hostname matches known ATS domain list",
    )

    # v2 WHOIS signal (replaces domain_age_days for v2 logic)
    whois_domain_age_days: Optional[int] = Field(
        default=None,
        description="Domain age in days from WHOIS creation date (v2 naming)",
    )

    # v2 signal aggregation
    signal_count: int = Field(
        default=0,
        description="Net positive verification signals. Infra failures excluded.",
    )

    # v2 AI-generated verification summary
    ai_summary: Optional[str] = Field(
        default=None,
        description="AI summary from ai_summary_generator. Only stored after validate_ai_summary() passes.",
    )


# ──────────────────────────────────────────────────────────────
# CompanyVerification — original (kept as-is)
# ──────────────────────────────────────────────────────────────

class CompanyVerification(SQLModel, table=True):
    __tablename__: str = "company_verifications"  # type: ignore
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    company_id: uuid.UUID = Field(foreign_key="companies.id")
    triggered_by: Optional[uuid.UUID] = Field(
        default=None, foreign_key="users.id"
    )
    trust_score_before: Optional[int] = Field(default=None)
    trust_score_after: Optional[int] = Field(default=None)
    risk_score_before: Optional[int] = Field(default=None)
    risk_score_after: Optional[int] = Field(default=None)
    ai_summary: Optional[str] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ──────────────────────────────────────────────────────────────
# VerificationCheck — original (kept as-is)
# ──────────────────────────────────────────────────────────────

class VerificationCheck(SQLModel, table=True):
    __tablename__: str = "verification_checks"  # type: ignore
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    company_id: uuid.UUID = Field(foreign_key="companies.id")
    verification_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="company_verifications.id"
    )
    check_type: str = Field(max_length=50)
    status: CheckStatus = Field(default=CheckStatus.not_run)
    passed: Optional[bool] = Field(default=None)
    score_delta: int = Field(default=0)
    primary_source: Optional[str] = Field(default=None, max_length=50)
    fallback_used: bool = Field(default=False)
    evidence_text: Optional[str] = Field(default=None)
    error_message: Optional[str] = Field(default=None)
    is_infrastructure_failure: bool = Field(
        default=False,
        description="v2: True when check failed due to infra (timeout, portal down). Does NOT reduce signal_count.",
    )
    retry_count: int = Field(default=0)
    duration_ms: Optional[int] = Field(default=None)
    checked_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
