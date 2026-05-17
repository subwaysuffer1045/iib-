from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine
from alembic import context
import asyncio
from app.config import settings
from app.database import engine
from sqlmodel import SQLModel

# Import ALL models so Alembic sees them
from app.models.college import College, CollegeEmailDomain
from app.models.user import User, UserProfile, Consent
from app.models.source import Source, SourcePolicy
from app.models.company import Company, CompanyVerification, VerificationCheck
from app.models.internship import Internship, InternshipSource
from app.models.crawl import CrawlJob, CrawlLog, ParserFailure
from app.models.saved import UserSavedInternship, UserApplicationTracker
from app.models.alert import UserAlertPreference
from app.models.audit import AuditLog, SuspiciousReport
from app.models.import_batch import ImportBatch, ImportRow

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL.replace("%", "%%"))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await engine.dispose()

def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
