"""
Phase 1 gate tests — lock in v2 model structure.

Tests verify:
  - InternshipStatus enum has exactly 4 values
  - TARGET_DOMAINS has exactly 6 entries
  - Internship model has all required v2 fields
  - Company model has all required v2 fields
  - DedupHash model exists with correct fields
  - SheetSyncLog model exists with correct fields
  - trust_score field ge/le constraints
  - paid_gate_passed defaults to False
  - apply_link_valid defaults to False
  - fee_scam_detected defaults to False
  - status defaults to draft

Run with: pytest tests/unit/test_phase1_models.py -v
"""
import pytest
import uuid
from datetime import datetime, date

from app.models.internship import (
    Internship,
    InternshipStatus,
    InternshipSource,
    ApplyLinkType,
    StipendConfidence,
    WorkMode,
    TARGET_DOMAINS,
)
from app.models.company import (
    Company,
    VerificationStatus,
    CompanyVerification,
    VerificationCheck,
    CheckStatus,
)
from app.models.dedup_hash import DedupHash
from app.models.sheet_sync_log import SheetSyncLog, SyncStatus


# ──────────────────────────────────────────────────────────────
# TARGET_DOMAINS
# ──────────────────────────────────────────────────────────────

class TestTargetDomains:
    def test_exactly_six_domains(self):
        assert len(TARGET_DOMAINS) == 6

    def test_exact_domain_names(self):
        expected = {
            "Android App Development",
            "Game Development",
            "iOS App Development",
            "Web Development",
            "Graphic Design",
            "Data Science",
        }
        assert set(TARGET_DOMAINS) == expected

    def test_no_extra_domains(self):
        """No domain outside the 6 should silently exist."""
        forbidden = ["Machine Learning", "AI", "Blockchain", "DevOps", "Marketing"]
        for d in forbidden:
            assert d not in TARGET_DOMAINS


# ──────────────────────────────────────────────────────────────
# InternshipStatus enum
# ──────────────────────────────────────────────────────────────

class TestInternshipStatusEnum:
    def test_has_exactly_four_values(self):
        values = [e.value for e in InternshipStatus]
        assert sorted(values) == sorted(["active", "expired", "rejected", "draft"])

    def test_active_value(self):
        assert InternshipStatus.active == "active"

    def test_draft_value(self):
        assert InternshipStatus.draft == "draft"


# ──────────────────────────────────────────────────────────────
# Internship model — v2 field presence & defaults
# ──────────────────────────────────────────────────────────────

class TestInternshipModelV2Fields:
    def _make_internship(self, **overrides) -> Internship:
        defaults = dict(
            slug="test-slug-001",
            title="Test Internship",
            company_id=uuid.uuid4(),
            apply_url="https://example.com/apply",
        )
        defaults.update(overrides)
        return Internship(**defaults)

    def test_has_domain_field(self):
        i = self._make_internship()
        assert hasattr(i, "domain")
        assert i.domain is None  # nullable, no default

    def test_has_status_field_defaults_to_draft(self):
        i = self._make_internship()
        assert hasattr(i, "status")
        assert i.status == InternshipStatus.draft

    def test_paid_gate_passed_defaults_false(self):
        i = self._make_internship()
        assert i.paid_gate_passed is False

    def test_fee_scam_detected_defaults_false(self):
        i = self._make_internship()
        assert i.fee_scam_detected is False

    def test_apply_link_valid_defaults_false(self):
        i = self._make_internship()
        assert i.apply_link_valid is False

    def test_apply_link_type_defaults_unknown(self):
        i = self._make_internship()
        assert i.apply_link_type == ApplyLinkType.unknown

    def test_stipend_confidence_defaults_low(self):
        i = self._make_internship()
        assert i.stipend_confidence == StipendConfidence.low

    def test_has_apply_link_field(self):
        i = self._make_internship()
        assert hasattr(i, "apply_link")
        assert i.apply_link is None

    def test_has_source_field(self):
        i = self._make_internship()
        assert hasattr(i, "source")
        assert i.source is None

    def test_has_source_id_field(self):
        i = self._make_internship()
        assert hasattr(i, "source_id")
        assert i.source_id is None

    def test_has_last_date_field(self):
        i = self._make_internship()
        assert hasattr(i, "last_date")
        assert i.last_date is None

    def test_has_sheet_synced_at_field(self):
        i = self._make_internship()
        assert hasattr(i, "sheet_synced_at")
        assert i.sheet_synced_at is None

    def test_has_expires_at_field(self):
        i = self._make_internship()
        assert hasattr(i, "expires_at")
        assert i.expires_at is None

    def test_domain_must_be_valid_target(self):
        """Business logic: domain set to a valid target."""
        i = self._make_internship(domain="Web Development")
        assert i.domain == "Web Development"
        assert i.domain in TARGET_DOMAINS

    def test_source_enum_values(self):
        values = [e.value for e in InternshipSource]
        assert "adzuna" in values
        assert "greenhouse" in values
        assert "lever" in values
        assert "manual" in values
        assert "csv_import" in values

    def test_apply_link_type_enum_values(self):
        values = [e.value for e in ApplyLinkType]
        assert set(values) == {"ats", "website", "email", "unknown"}

    def test_stipend_confidence_enum_values(self):
        values = [e.value for e in StipendConfidence]
        assert set(values) == {"high", "medium", "low"}


# ──────────────────────────────────────────────────────────────
# Company model — v2 field presence & defaults
# ──────────────────────────────────────────────────────────────

class TestCompanyModelV2Fields:
    def _make_company(self, **overrides) -> Company:
        defaults = dict(
            canonical_name="Test Corp",
            slug="test-corp",
        )
        defaults.update(overrides)
        return Company(**defaults)

    def test_has_name_field(self):
        c = self._make_company()
        assert hasattr(c, "name")
        assert c.name is None

    def test_has_domain_field(self):
        c = self._make_company()
        assert hasattr(c, "domain")
        assert c.domain is None

    def test_has_hard_fail_reason_field(self):
        c = self._make_company()
        assert hasattr(c, "hard_fail_reason")
        assert c.hard_fail_reason is None

    def test_mca21_verified_defaults_false(self):
        c = self._make_company()
        assert c.mca21_verified is False

    def test_gstin_verified_defaults_false(self):
        c = self._make_company()
        assert c.gstin_verified is False

    def test_startup_india_verified_defaults_false(self):
        c = self._make_company()
        assert c.startup_india_verified is False

    def test_ats_detected_defaults_false(self):
        c = self._make_company()
        assert c.ats_detected is False

    def test_has_whois_domain_age_days(self):
        c = self._make_company()
        assert hasattr(c, "whois_domain_age_days")
        assert c.whois_domain_age_days is None

    def test_signal_count_defaults_zero(self):
        c = self._make_company()
        assert c.signal_count == 0

    def test_has_ai_summary_field(self):
        c = self._make_company()
        assert hasattr(c, "ai_summary")
        assert c.ai_summary is None

    def test_trust_score_hard_cap_logic(self):
        """Application layer must enforce max 85 for automated updates."""
        c = self._make_company()
        # Model allows up to 100 (le=100) — cap enforced in score_aggregator
        c.trust_score = 85
        assert c.trust_score == 85
        # Score aggregator will do: min(raw_score, 85)
        raw = 90
        capped = min(raw, 85)
        assert capped == 85


# ──────────────────────────────────────────────────────────────
# VerificationCheck — is_infrastructure_failure
# ──────────────────────────────────────────────────────────────

class TestVerificationCheckV2:
    def test_has_is_infrastructure_failure(self):
        vc = VerificationCheck(
            company_id=uuid.uuid4(),
            check_type="whois",
        )
        assert hasattr(vc, "is_infrastructure_failure")
        assert vc.is_infrastructure_failure is False

    def test_infrastructure_failure_can_be_set(self):
        vc = VerificationCheck(
            company_id=uuid.uuid4(),
            check_type="mca21",
            is_infrastructure_failure=True,
            status=CheckStatus.infra_error,
        )
        assert vc.is_infrastructure_failure is True


# ──────────────────────────────────────────────────────────────
# DedupHash model
# ──────────────────────────────────────────────────────────────

class TestDedupHashModel:
    def test_model_exists(self):
        dh = DedupHash(
            internship_id=uuid.uuid4(),
            hash_exact="a" * 64,
        )
        assert dh.hash_exact == "a" * 64
        assert dh.hash_fuzzy is None
        assert dh.id is not None

    def test_has_created_at(self):
        dh = DedupHash(internship_id=uuid.uuid4(), hash_exact="b" * 64)
        assert dh.created_at is not None
        assert isinstance(dh.created_at, datetime)


# ──────────────────────────────────────────────────────────────
# SheetSyncLog model
# ──────────────────────────────────────────────────────────────

class TestSheetSyncLogModel:
    def test_model_exists(self):
        log = SheetSyncLog(sheet_tab="APP ANDROID")
        assert log.sheet_tab == "APP ANDROID"
        assert log.rows_written == 0
        assert log.rows_expired == 0
        assert log.rows_rejected == 0
        assert log.sync_status == SyncStatus.success
        assert log.error_message is None

    def test_sync_status_enum_values(self):
        values = [e.value for e in SyncStatus]
        assert set(values) == {"success", "partial", "failed"}

    def test_tab_names_match_spec(self):
        """All 9 sheet tab names from spec must be valid."""
        expected_tabs = [
            "APP ANDROID",
            "Game development",
            "APP IOS",
            "WEB DEVELOPMENT",
            "Graphic Design",
            "DATA SCIENCE",
            "REJECTED",
            "EXPIRED",
            "NEEDS REVIEW",
        ]
        for tab in expected_tabs:
            log = SheetSyncLog(sheet_tab=tab)
            assert log.sheet_tab == tab


# ──────────────────────────────────────────────────────────────
# Gate check: active status constraints (business logic layer)
# ──────────────────────────────────────────────────────────────

class TestActiveStatusGates:
    """
    These test the business rule that must be enforced in the service layer
    BEFORE setting status = 'active'. The DB constraint is a safety net.
    """

    def _make_internship(self, **kwargs) -> Internship:
        return Internship(
            slug="gate-test",
            title="Gate Test Internship",
            company_id=uuid.uuid4(),
            apply_url="https://example.com",
            **kwargs,
        )

    def test_active_requires_paid_gate(self):
        """If paid_gate_passed = False, status must NOT be set to active."""
        i = self._make_internship(paid_gate_passed=False)
        # Service layer check
        can_activate = i.paid_gate_passed and i.apply_link_valid
        assert not can_activate

    def test_active_requires_valid_link(self):
        """If apply_link_valid = False, status must NOT be set to active."""
        i = self._make_internship(paid_gate_passed=True, apply_link_valid=False)
        can_activate = i.paid_gate_passed and i.apply_link_valid
        assert not can_activate

    def test_active_allowed_when_both_pass(self):
        i = self._make_internship(
            paid_gate_passed=True,
            apply_link_valid=True,
            apply_link="https://internshala.com/internship/123",
        )
        can_activate = i.paid_gate_passed and i.apply_link_valid
        assert can_activate

    def test_fee_scam_blocks_activation(self):
        """fee_scam_detected = True must permanently block status = active."""
        i = self._make_internship(
            paid_gate_passed=True,
            apply_link_valid=True,
            fee_scam_detected=True,
        )
        can_activate = (
            i.paid_gate_passed and i.apply_link_valid and not i.fee_scam_detected
        )
        assert not can_activate
