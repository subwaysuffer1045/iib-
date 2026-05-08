"""
Adzuna Ingestion Client — v2.
Fetches internships from Adzuna API (India).
Applies 6-domain filtering, normalization, and validation gates.
"""
import httpx
import logging
from typing import List, Dict, Any
from app.config import settings
from app.pipelines.ingestion.normalizer import Normalizer
from app.pipelines.validation.paid_gate import PaidGate
from app.pipelines.validation.fee_scam_detector import FeeScamDetector

logger = logging.getLogger(__name__)

class AdzunaClient:
    def __init__(self):
        self.app_id = settings.ADZUNA_APP_ID
        self.app_key = settings.ADZUNA_APP_KEY or settings.ADZUNA_API_KEY
        self.base_url = settings.ADZUNA_BASE_URL
        self.country = settings.ADZUNA_COUNTRY
        
        self.normalizer = Normalizer()
        self.paid_gate = PaidGate()
        self.scam_detector = FeeScamDetector()

    async def fetch_and_process(self, domain_name: str, pages: int = 1) -> List[Dict[str, Any]]:
        """
        Fetches jobs for a domain (e.g. 'Web Development') and processes them.
        """
        results = []
        
        if not self.app_id or not self.app_key:
            logger.warning("Adzuna credentials missing. Skipping.")
            return []

        async with httpx.AsyncClient() as client:
            for page in range(1, pages + 1):
                params = {
                    "app_id": self.app_id,
                    "app_key": self.app_key,
                    "what": domain_name,
                    "where": "India",
                    "content-type": "application/json",
                    "results_per_page": 20,
                    "page": page,
                    "category": "it-jobs"
                }
                
                try:
                    response = await client.get(f"{self.base_url}/{self.country}/search/{page}", params=params)
                    response.raise_for_status()
                    data = response.json()
                    
                    for job in data.get("results", []):
                        # 1. Normalize
                        raw_data = {
                            "title": job.get("title"),
                            "company_name": job.get("company", {}).get("display_name"),
                            "description": job.get("description"),
                            "location_text": job.get("location", {}).get("display_name"),
                            "stipend_text": job.get("salary_min"), # Adzuna specific
                            "apply_link": job.get("redirect_url"),
                            "source": "adzuna",
                            "source_id": job.get("id"),
                        }
                        
                        normalized = self.normalizer.normalize(raw_data)
                        
                        # Override domain with the one we searched for to ensure 100% accuracy
                        normalized["domain"] = domain_name 

                        # 2. Gate Checks
                        is_scam, _ = self.scam_detector.detect(f"{normalized['title']} {normalized['description']}")
                        if is_scam:
                            continue
                            
                        if not self.paid_gate.check(normalized):
                            continue
                            
                        results.append(normalized)

                except Exception as e:
                    logger.error(f"Adzuna fetch failed for {domain_name} page {page}: {e}")
                    break
                    
        return results
