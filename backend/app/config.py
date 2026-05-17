"""
App configuration — v2.
All values loaded from environment variables or .env file.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # ── Database ───────────────────────────────────────────────────
    DATABASE_URL: str

    # ── Redis / Celery (Upstash free tier in MVP) ─────────────────
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # ── JWT Auth ──────────────────────────────────────────────────
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # ── Email (Resend free tier: 100/day) ─────────────────────────
    RESEND_API_KEY: str = ""
    FROM_EMAIL: str = "noreply@localhost"
    RESEND_FROM_NAME: str = "IIB India Alerts"

    # ── AI (Anthropic + OpenAI) ───────────────────────────────────
    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-3-5-sonnet-20241022"
    OPENAI_API_KEY: str = ""

    # ── Adzuna (free 1000 req/day) ────────────────────────────────
    ADZUNA_APP_ID: str = ""
    ADZUNA_APP_KEY: str = ""  # original key name kept for backward compat
    ADZUNA_API_KEY: str = ""  # v2 alias (maps to ADZUNA_APP_KEY)
    ADZUNA_COUNTRY: str = "in"
    ADZUNA_BASE_URL: str = "https://api.adzuna.com/v1/api/jobs"

    # ── Greenhouse / Lever (optional) ─────────────────────────────
    GREENHOUSE_API_KEY: str = ""
    LEVER_API_KEY: str = ""

    # ── MCA21 (free public portal scrape) ─────────────────────────
    MCA21_API_URL: str = "https://www.mca.gov.in/mcafoportal/"
    MCA21_TIMEOUT_SECONDS: int = 5

    # ── GST / Startup India (free public) ─────────────────────────
    GST_PORTAL_API_URL: str = "https://services.gst.gov.in/"
    STARTUP_INDIA_API_URL: str = "https://api.startupindia.gov.in/"

    # ── SerpAPI (optional — free 100/month) ───────────────────────
    SERPAPI_API_KEY: str = ""

    # ── Google Sheets (free — service account) ───────────────────
    GOOGLE_SHEETS_CREDENTIALS_JSON: str = ""  # path to service account JSON
    GOOGLE_SHEET_ID: str = ""
    GOOGLE_SHEET_SCOPES: str = "https://www.googleapis.com/auth/spreadsheets"

    # ── Sentry (optional free tier) ───────────────────────────────
    SENTRY_DSN: str = ""
    SENTRY_ENVIRONMENT: str = "production"

    # ── App ───────────────────────────────────────────────────────
    APP_ENV: str = "development"
    DEBUG: bool = False
    CORS_ORIGINS: str = "http://localhost:3000"
    API_V1_PREFIX: str = "/api/v1"
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 60
    IIB_INGEST_API_KEY: str = "supersecret_ingest_key"

    # ── Verification engine constants ─────────────────────────────
    VERIFICATION_HTTP_TIMEOUT_SECONDS: int = 5
    VERIFICATION_MAX_RETRIES: int = 2
    BAD_DOMAIN_BLACKLIST_KEY: str = "iib:blacklist:domains"

    # ── Business logic constants ──────────────────────────────────
    MIN_SIGNALS_FOR_VERIFIED: int = 3
    MAX_AUTO_TRUST_SCORE: int = 85          # automation cap — only admin can exceed
    MIN_TRUST_FOR_PUBLISH: int = 40         # spec: trust_score > 40
    MIN_TRUST_FOR_NEEDS_REVIEW_PUBLISH: int = 55  # kept for backward compat
    MAX_RISK_FOR_AUTO_PUBLISH: int = 50     # spec: risk_score < 50
    LINK_VALIDATION_CACHE_TTL_SECONDS: int = 86400  # 24 hours

    # ── Pipeline ───────────────────────────────────────────────────
    HTTP_TIMEOUT: int = 8
    MAX_RESULTS_PER_SOURCE: int = 50

    class Config:
        env_file = ".env"


settings = Settings()
