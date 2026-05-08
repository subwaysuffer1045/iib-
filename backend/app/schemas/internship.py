from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
import uuid

class InternshipCardSchema(BaseModel):
    id: uuid.UUID
    slug: str
    title: str
    company_name: str
    company_trust_score: int
    city: Optional[str]
    state: Optional[str]
    location_text: Optional[str]
    work_mode: str
    domain_slug: Optional[str]
    stipend_min: Optional[float]
    stipend_max: Optional[float]
    stipend_text: Optional[str]
    apply_by: Optional[date]
    is_expiring_soon: bool
    trust_score: int
    verification_status: str
    duration_text: Optional[str]
    freshness_bucket: Optional[str]
    skills: Optional[List]
    posted_at: Optional[datetime]

    class Config:
        from_attributes = True

class InternshipDetailSchema(BaseModel):
    id: uuid.UUID
    slug: str
    title: str
    description_raw: Optional[str]
    company_id: uuid.UUID
    company_name: str
    company_trust_score: int
    city: Optional[str]
    state: Optional[str]
    work_mode: str
    stipend_min: Optional[float]
    stipend_max: Optional[float]
    stipend_text: Optional[str]
    apply_url: str
    apply_by: Optional[date]
    trust_score: int
    verification_status: str
    domain_slug: Optional[str]
    duration_text: Optional[str]
    skills: Optional[List]
    posted_at: Optional[datetime]

    class Config:
        from_attributes = True
