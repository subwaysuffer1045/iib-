from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

class CompanyVerifySchema(BaseModel):
    status: str  # 'verified', 'rejected'
    notes: Optional[str] = None

class CompanyOverrideScoreSchema(BaseModel):
    trust_score: int
    reason: str

class SyncLogSchema(BaseModel):
    id: uuid.UUID
    started_at: datetime
    finished_at: Optional[datetime]
    status: str
    total_processed: int
    new_internships: int
    updated_internships: int
    errors: Optional[List[str]]

    class Config:
        from_attributes = True
