"""
Evidence Collector — v2.
Orchestrates parallel verification checks.
Handles timeouts, retries, and infra-failure marking.
"""
import asyncio
import logging
from typing import Dict, Any, List
from datetime import datetime, timezone
from app.models.company import CheckStatus
from app.pipelines.verification.score_aggregator import ScoreAggregator

logger = logging.getLogger(__name__)

class EvidenceCollector:
    def __init__(self, session):
        self.session = session
        self.aggregator = ScoreAggregator()

    async def collect_all(self, company_id: str, domain: str) -> Dict[str, Any]:
        """
        Runs all scrapers in parallel.
        Returns aggregated results for the company record.
        """
        # Placeholder for real scraper calls
        # We'll build whois, mca21, gstin next
        tasks = [
            self._run_check("whois", domain),
            self._run_check("mca21", domain),
            self._run_check("gstin", domain),
            self._run_check("ats", domain),
        ]
        
        results = await asyncio.gather(*tasks)
        
        signals = {}
        infra_failures = {}
        
        for check_type, passed, is_infra in results:
            signals[check_type] = passed
            infra_failures[check_type] = is_infra

        trust, risk, verified = self.aggregator.calculate(signals, infra_failures)
        
        return {
            "trust_score": trust,
            "risk_score": risk,
            "company_verified": verified,
            "signal_count": sum(1 for v in signals.values() if v),
            "last_verified_at": datetime.now(timezone.utc),
        }

    async def _run_check(self, check_type: str, domain: str):
        """Wrapper for individual scrapers with infra-failure logic."""
        try:
            # Logic will call real scrapers here
            # For now, return inconclusive/fail
            return check_type, False, False
        except Exception as e:
            logger.error(f"Check {check_type} failed: {e}")
            return check_type, False, True  # Mark as infra failure
