"""
WHOIS Checker — v2.
Calculates domain age.
Signal passed if domain_age > 365 days (1 year).
"""
import whois
from datetime import datetime, timezone
from typing import Tuple, Optional

class WhoisChecker:
    def check(self, domain: str) -> Tuple[bool, int, bool]:
        """
        Returns (passed, age_days, is_infra_failure).
        Passed = age > 365 days.
        """
        try:
            w = whois.whois(domain)
            creation_date = w.creation_date
            
            # creation_date can be a single date or a list
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            
            if not creation_date:
                return False, 0, False

            # Ensure timezone-aware comparison
            if creation_date.tzinfo is None:
                creation_date = creation_date.replace(tzinfo=timezone.utc)
            
            now = datetime.now(timezone.utc)
            age = (now - creation_date).days
            
            return age > 365, age, False

        except Exception:
            # WHOIS often rate-limits or times out
            return False, 0, True
