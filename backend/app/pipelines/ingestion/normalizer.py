"""
Normalizer Pipeline — v2.
Transforms raw job data into structured Internship records.
Handles:
- Stipend parsing (min/max/currency)
- Domain classification (6 target domains)
- Work mode detection (remote/hybrid/onsite)
- Location cleanup
- Slug generation
- Expiry calculation
"""
import re
from datetime import datetime, date, timedelta
from typing import Optional, Tuple, List
from slugify import slugify
from app.models.internship import (
    TARGET_DOMAINS,
    InternshipStatus,
    WorkMode,
    StipendConfidence,
)

class Normalizer:
    def __init__(self):
        # Keyword mappings for domain classification
        self.domain_keywords = {
            "Android App Development": ["android", "kotlin", "java android", "mobile app"],
            "iOS App Development": ["ios", "swift", "objective-c", "iphone", "ipad"],
            "Web Development": ["web", "frontend", "backend", "fullstack", "react", "node", "javascript", "html", "css", "django", "flask"],
            "Game Development": ["game", "unity", "unreal", "c#", "c++", "3d", "gaming"],
            "Graphic Design": ["design", "ui", "ux", "photoshop", "illustrator", "figma", "graphic"],
            "Data Science": ["data science", "machine learning", "ai", "python", "pandas", "numpy", "pytorch", "tensorflow", "analytics"],
        }

    def generate_slug(self, title: str, company_name: str) -> str:
        """Generates a unique slug for the internship."""
        base = slugify(f"{title}-{company_name}")
        # Add short random suffix for uniqueness
        import uuid
        return f"{base[:280]}-{str(uuid.uuid4())[:8]}"

    def detect_domain(self, title: str, description: str = "") -> Optional[str]:
        """Maps job to one of 6 TARGET_DOMAINS based on keywords."""
        text = f"{title} {description}".lower()
        
        # Priority check: Mobile apps
        if any(k in text for k in self.domain_keywords["Android App Development"]):
            return "Android App Development"
        if any(k in text for k in self.domain_keywords["iOS App Development"]):
            return "iOS App Development"
        
        # Check others
        for domain, keywords in self.domain_keywords.items():
            if domain in ["Android App Development", "iOS App Development"]:
                continue
            if any(k in text for k in keywords):
                return domain
        
        return None

    def detect_work_mode(self, text: str) -> WorkMode:
        """Detects if remote, hybrid, or onsite."""
        text = text.lower()
        if any(k in text for k in ["remote", "work from home", "wfh", "anywhere"]):
            return WorkMode.remote
        if any(k in text for k in ["hybrid", "flexible", "partial remote"]):
            return WorkMode.hybrid
        return WorkMode.onsite

    def parse_stipend(self, text: str) -> Tuple[Optional[float], Optional[float], StipendConfidence]:
        """
        Parses stipend strings like '₹10k - 20k', '15000', 'Unpaid'.
        Returns (min, max, confidence).
        """
        if not text or any(k in text.lower() for k in ["unpaid", "free", "no stipend", "0"]):
            return 0.0, 0.0, StipendConfidence.high

        # Extract all numbers
        numbers = re.findall(r"(\d+(?:\.\d+)?)", text.replace(",", ""))
        if not numbers:
            return None, None, StipendConfidence.low

        vals = [float(n) for n in numbers]
        
        # Handle 'k' multiplier (e.g. 10k -> 10000)
        is_k = "k" in text.lower() or "thousand" in text.lower()
        if is_k:
            vals = [v * 1000 if v < 1000 else v for v in vals]

        min_val = min(vals)
        max_val = max(vals)
        
        confidence = StipendConfidence.high if len(vals) > 0 else StipendConfidence.low
        return min_val, max_val, confidence

    def calculate_expiry(self, posted_at: datetime, duration_weeks: Optional[int] = None) -> datetime:
        """Computes expiry: posted_date + 30 days default OR duration."""
        base_days = (duration_weeks * 7) if duration_weeks else 30
        return posted_at + timedelta(days=base_days)

    def normalize(self, raw: dict) -> dict:
        """Main entry point for normalizing raw source data."""
        title = raw.get("title", "")
        company_name = raw.get("company_name", "Unknown Company")
        description = raw.get("description", "")
        
        posted_at = raw.get("posted_at") or datetime.now()
        duration_weeks = raw.get("duration_weeks")
        
        stipend_min, stipend_max, confidence = self.parse_stipend(raw.get("stipend_text", ""))
        
        return {
            "title": title,
            "slug": self.generate_slug(title, company_name),
            "domain": self.detect_domain(title, description),
            "work_mode": self.detect_work_mode(f"{title} {description}"),
            "stipend_min": stipend_min,
            "stipend_max": stipend_max,
            "stipend_confidence": confidence,
            "is_paid": (stipend_min or 0) > 0,
            "posted_at": posted_at,
            "expires_at": self.calculate_expiry(posted_at, duration_weeks),
            "status": InternshipStatus.draft,
            "location_text": raw.get("location_text"),
            "apply_link": raw.get("apply_link"),
            "source": raw.get("source"),
            "source_id": raw.get("source_id"),
        }
