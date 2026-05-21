from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.v1.health import router as health_router
from app.api.v1.auth import router as auth_router
from app.api.v1.internships import router as internships_router
from app.api.v1.companies import router as companies_router
from app.api.v1.admin.internships import router as admin_internships_router
from app.api.v1.admin.companies import router as admin_companies_router
from app.api.v1.admin.sheet import router as admin_sheet_router
from app.api.v1.admin.ingest import router as admin_ingest_router

# Import all models so SQLAlchemy can resolve foreign keys
from app.models import college, user, source, company, internship, crawl, saved, alert, audit, import_batch  # noqa: F401
from app.models import dedup_hash, sheet_sync_log  # noqa: F401  # v2 new models

app = FastAPI(
    title="IIB India API",
    description="Internship Intelligence Bot India",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001", 
        "https://iib-web-b949.vercel.app",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api/v1", tags=["health"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(internships_router, prefix="/api/v1/internships", tags=["internships"])
app.include_router(companies_router, prefix="/api/v1/companies", tags=["companies"])
app.include_router(admin_internships_router, prefix="/api/v1/admin/internships", tags=["admin-internships"])
app.include_router(admin_companies_router, prefix="/api/v1/admin/companies", tags=["admin-companies"])
app.include_router(admin_sheet_router, prefix="/api/v1/admin/sheet", tags=["admin-sheet"])
app.include_router(admin_ingest_router, prefix="/api/v1/admin/ingest", tags=["admin-ingest"])

@app.get("/")
async def root():
    return {"message": "IIB India API", "docs": "/docs"}
