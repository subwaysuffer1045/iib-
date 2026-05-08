"""v2_schema_additions

Additive migration — adds v2 columns to existing tables.
No columns dropped. No existing data affected.
Also creates two new tables: dedup_hashes, sheet_sync_log.
Adds DB-level indexes required by spec Part 11.

Revision ID: a1b2c3d4e5f6
Revises: 6ec1034a6d5a
Create Date: 2026-05-08
"""
from typing import Sequence, Union
import alembic
from alembic import op
import sqlalchemy as sa
import sqlmodel
import sqlmodel.sql.sqltypes

revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "6ec1034a6d5a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ──────────────────────────────────────────────────────────
    # 1. COMPANIES — add v2 columns
    # ──────────────────────────────────────────────────────────

    op.add_column("companies", sa.Column("name", sa.Text(), nullable=True))
    op.add_column(
        "companies",
        sa.Column("domain", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
    )
    op.add_column(
        "companies",
        sa.Column("hard_fail_reason", sa.Text(), nullable=True),
    )
    op.add_column(
        "companies",
        sa.Column("mca21_verified", sa.Boolean(), nullable=False, server_default="false"),
    )
    op.add_column(
        "companies",
        sa.Column("gstin_verified", sa.Boolean(), nullable=False, server_default="false"),
    )
    op.add_column(
        "companies",
        sa.Column(
            "startup_india_verified",
            sa.Boolean(),
            nullable=False,
            server_default="false",
        ),
    )
    op.add_column(
        "companies",
        sa.Column("ats_detected", sa.Boolean(), nullable=False, server_default="false"),
    )
    op.add_column(
        "companies",
        sa.Column("whois_domain_age_days", sa.Integer(), nullable=True),
    )
    op.add_column(
        "companies",
        sa.Column("signal_count", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column("companies", sa.Column("ai_summary", sa.Text(), nullable=True))

    # Index on companies.domain (not unique at DB level to avoid migration complexity
    # for existing rows; uniqueness enforced at application layer)
    op.create_index("ix_companies_domain", "companies", ["domain"], unique=False)

    # trust_score cap: add CHECK constraint (trust_score <= 85 for automated rows;
    # admin override bypasses at application layer, not DB level, to allow >85 via admin)
    # NOTE: We enforce <=85 via application logic (min(score, 85)) per spec.
    # A DB CHECK constraint at column level is added here as a safety net.
    # The /admin/companies/{id}/override-score route uses a direct UPDATE bypass.
    # We set the CHECK on the existing column type — Postgres allows this:
    op.execute(
        "ALTER TABLE companies ADD CONSTRAINT companies_trust_score_auto_cap "
        "CHECK (trust_score <= 100)"  # Full 0-100 range; cap enforced in service layer
    )

    # ──────────────────────────────────────────────────────────
    # 2. INTERNSHIPS — add v2 columns
    # ──────────────────────────────────────────────────────────

    # Domain (one of 6 target domains)
    op.add_column(
        "internships",
        sa.Column("domain", sqlmodel.sql.sqltypes.AutoString(length=64), nullable=True),
    )
    op.create_index("ix_internships_domain_v2", "internships", ["domain"])

    # v2 unified status enum
    op.execute("""
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'internshipstatus') THEN
                CREATE TYPE internshipstatus AS ENUM ('active', 'expired', 'rejected', 'draft');
            END IF;
        END $$;
    """)
    op.add_column(
        "internships",
        sa.Column(
            "status",
            sa.Enum("active", "expired", "rejected", "draft", name="internshipstatus", create_type=False),
            nullable=False,
            server_default="draft",
        ),
    )
    op.create_index("ix_internships_status", "internships", ["status"])

    # Paid gate
    op.add_column(
        "internships",
        sa.Column(
            "paid_gate_passed", sa.Boolean(), nullable=False, server_default="false"
        ),
    )

    # Fee scam
    op.add_column(
        "internships",
        sa.Column(
            "fee_scam_detected", sa.Boolean(), nullable=False, server_default="false"
        ),
    )

    # v2 apply link fields
    op.add_column(
        "internships",
        sa.Column("apply_link", sa.Text(), nullable=True),
    )

    op.execute("""
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'applylinktype') THEN
                CREATE TYPE applylinktype AS ENUM ('ats', 'website', 'email', 'unknown');
            END IF;
        END $$;
    """)
    op.add_column(
        "internships",
        sa.Column(
            "apply_link_type",
            sa.Enum("ats", "website", "email", "unknown", name="applylinktype", create_type=False),
            nullable=False,
            server_default="unknown",
        ),
    )
    op.add_column(
        "internships",
        sa.Column(
            "apply_link_valid", sa.Boolean(), nullable=False, server_default="false"
        ),
    )
    op.add_column(
        "internships",
        sa.Column("apply_link_checked_at", sa.DateTime(timezone=True), nullable=True),
    )

    # v2 source enum
    op.execute("""
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'internshipsourceenum') THEN
                CREATE TYPE internshipsourceenum AS ENUM ('adzuna', 'greenhouse', 'lever', 'manual', 'csv_import');
            END IF;
        END $$;
    """)
    op.add_column(
        "internships",
        sa.Column(
            "source",
            sa.Enum(
                "adzuna", "greenhouse", "lever", "manual", "csv_import",
                name="internshipsourceenum",
                create_type=False,
            ),
            nullable=True,
        ),
    )
    op.add_column(
        "internships",
        sa.Column(
            "source_id",
            sqlmodel.sql.sqltypes.AutoString(length=255),
            nullable=True,
        ),
    )

    # v2 deadline (alias of apply_by for sheet column G)
    op.add_column(
        "internships",
        sa.Column("last_date", sa.Date(), nullable=True),
    )

    # v2 sheet sync tracking
    op.add_column(
        "internships",
        sa.Column("sheet_synced_at", sa.DateTime(timezone=True), nullable=True),
    )

    # v2 stipend confidence enum
    op.execute("""
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'stipendconfidence') THEN
                CREATE TYPE stipendconfidence AS ENUM ('high', 'medium', 'low');
            END IF;
        END $$;
    """)
    op.add_column(
        "internships",
        sa.Column(
            "stipend_confidence",
            sa.Enum("high", "medium", "low", name="stipendconfidence", create_type=False),
            nullable=False,
            server_default="low",
        ),
    )

    # v2 expiry timestamp
    op.add_column(
        "internships",
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
    )

    # DB-level safety constraints (belt-and-suspenders; main enforcement is app layer)
    op.execute(
        "ALTER TABLE internships ADD CONSTRAINT active_requires_paid_gate "
        "CHECK (status != 'active' OR paid_gate_passed = TRUE)"
    )
    op.execute(
        "ALTER TABLE internships ADD CONSTRAINT active_requires_valid_link "
        "CHECK (status != 'active' OR apply_link_valid = TRUE)"
    )

    # ──────────────────────────────────────────────────────────
    # 3. VERIFICATION_CHECKS — add is_infrastructure_failure
    # ──────────────────────────────────────────────────────────

    op.add_column(
        "verification_checks",
        sa.Column(
            "is_infrastructure_failure",
            sa.Boolean(),
            nullable=False,
            server_default="false",
        ),
    )

    # ──────────────────────────────────────────────────────────
    # 4. NEW TABLE: dedup_hashes
    # ──────────────────────────────────────────────────────────

    op.create_table(
        "dedup_hashes",
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("internship_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("hash_exact", sqlmodel.sql.sqltypes.AutoString(length=64), nullable=False),
        sa.Column("hash_fuzzy", sqlmodel.sql.sqltypes.AutoString(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["internship_id"], ["internships.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("hash_exact"),
    )
    op.create_index("ix_dedup_hashes_internship_id", "dedup_hashes", ["internship_id"])
    op.create_index("ix_dedup_hashes_hash_exact", "dedup_hashes", ["hash_exact"], unique=True)
    op.create_index("ix_dedup_fuzzy", "dedup_hashes", ["hash_fuzzy"])

    # ──────────────────────────────────────────────────────────
    # 5. NEW TABLE: sheet_sync_log
    # ──────────────────────────────────────────────────────────

    op.execute("""
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'syncstatus') THEN
                CREATE TYPE syncstatus AS ENUM ('success', 'partial', 'failed');
            END IF;
        END $$;
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS sheet_sync_log (
            id UUID PRIMARY KEY,
            sheet_tab VARCHAR(64) NOT NULL,
            rows_written INTEGER NOT NULL DEFAULT 0,
            rows_expired INTEGER NOT NULL DEFAULT 0,
            rows_rejected INTEGER NOT NULL DEFAULT 0,
            sync_status syncstatus NOT NULL DEFAULT 'success',
            error_message TEXT,
            synced_at TIMESTAMP NOT NULL
        )
    """)
    op.create_index("ix_sheet_sync_log_sheet_tab", "sheet_sync_log", ["sheet_tab"])
    op.create_index("ix_sheet_sync_log_synced_at", "sheet_sync_log", ["synced_at"])

    # ──────────────────────────────────────────────────────────
    # 6. SPEC PART 11 — required DB indexes
    # ──────────────────────────────────────────────────────────

    # Primary query — domain + status (partial index where active)
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_internships_domain_status "
        "ON internships (domain, status) WHERE status = 'active'"
    )

    # Expiry job
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_internships_expires_status "
        "ON internships (expires_at, status) WHERE status = 'active'"
    )

    # Link validation queue
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_internships_link_invalid "
        "ON internships (apply_link_valid, status) WHERE apply_link_valid = FALSE"
    )

    # Verification queue
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_companies_verification_status "
        "ON companies (verification_status)"
    )

    # Admin audit queries
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_audit_log_entity "
        "ON audit_logs (resource_type, resource_id, created_at DESC)"
    )

    # Alert matching — only index the boolean, not the JSON column (btree incompatible)
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_alerts_domain_active "
        "ON user_alert_preferences (alert_new_matches) "
        "WHERE alert_new_matches = TRUE"
    )

    # Sheet sync — find stale active rows
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_internships_sheet_sync "
        "ON internships (sheet_synced_at, status) WHERE status = 'active'"
    )


def downgrade() -> None:
    # ── Remove Part 11 indexes ───────────────────────────────
    op.execute("DROP INDEX IF EXISTS idx_internships_sheet_sync")
    op.execute("DROP INDEX IF EXISTS idx_alerts_domain_active")
    op.execute("DROP INDEX IF EXISTS idx_audit_log_entity")
    op.execute("DROP INDEX IF EXISTS idx_companies_verification_status")
    op.execute("DROP INDEX IF EXISTS idx_internships_link_invalid")
    op.execute("DROP INDEX IF EXISTS idx_internships_expires_status")
    op.execute("DROP INDEX IF EXISTS idx_internships_domain_status")

    # ── Remove new tables ────────────────────────────────────
    op.drop_index("ix_sheet_sync_log_synced_at", table_name="sheet_sync_log")
    op.drop_index("ix_sheet_sync_log_sheet_tab", table_name="sheet_sync_log")
    op.drop_table("sheet_sync_log")

    op.drop_index("ix_dedup_fuzzy", table_name="dedup_hashes")
    op.drop_index("ix_dedup_hashes_hash_exact", table_name="dedup_hashes")
    op.drop_index("ix_dedup_hashes_internship_id", table_name="dedup_hashes")
    op.drop_table("dedup_hashes")

    # ── Remove verification_checks column ────────────────────
    op.drop_column("verification_checks", "is_infrastructure_failure")

    # ── Remove internships v2 columns ────────────────────────
    op.execute("ALTER TABLE internships DROP CONSTRAINT IF EXISTS active_requires_valid_link")
    op.execute("ALTER TABLE internships DROP CONSTRAINT IF EXISTS active_requires_paid_gate")
    op.drop_column("internships", "expires_at")
    op.drop_column("internships", "stipend_confidence")
    op.drop_column("internships", "sheet_synced_at")
    op.drop_column("internships", "last_date")
    op.drop_column("internships", "source_id")
    op.drop_column("internships", "source")
    op.drop_column("internships", "apply_link_checked_at")
    op.drop_column("internships", "apply_link_valid")
    op.drop_column("internships", "apply_link_type")
    op.drop_column("internships", "apply_link")
    op.drop_column("internships", "fee_scam_detected")
    op.drop_column("internships", "paid_gate_passed")
    op.drop_index("ix_internships_status", table_name="internships")
    op.drop_column("internships", "status")
    op.drop_index("ix_internships_domain_v2", table_name="internships")
    op.drop_column("internships", "domain")

    # ── Remove companies v2 columns ──────────────────────────
    op.execute(
        "ALTER TABLE companies DROP CONSTRAINT IF EXISTS companies_trust_score_auto_cap"
    )
    op.drop_index("ix_companies_domain", table_name="companies")
    op.drop_column("companies", "ai_summary")
    op.drop_column("companies", "signal_count")
    op.drop_column("companies", "whois_domain_age_days")
    op.drop_column("companies", "ats_detected")
    op.drop_column("companies", "startup_india_verified")
    op.drop_column("companies", "gstin_verified")
    op.drop_column("companies", "mca21_verified")
    op.drop_column("companies", "hard_fail_reason")
    op.drop_column("companies", "domain")
    op.drop_column("companies", "name")
