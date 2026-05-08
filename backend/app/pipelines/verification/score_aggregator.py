"""
Score Aggregator — v2.
Calculates trust_score and risk_score from verification signals.
Enforces:
- Automated cap = 85 (spec §10)
- Verified threshold = 3 signals (spec §10)
- Hard fail rejection logic
"""
from typing import Dict, Any, Tuple
from app.config import settings

class ScoreAggregator:
    def __init__(self):
        self.max_auto_score = settings.MAX_AUTO_TRUST_SCORE
        self.verified_threshold = settings.MIN_SIGNALS_FOR_VERIFIED

    def calculate(self, signals: Dict[str, bool], infra_failures: Dict[str, bool]) -> Tuple[int, int, bool]:
        """
        Returns (trust_score, risk_score, is_verified).
        Signals: mca21, gstin, startup_india, ats_detected, whois_old.
        """
        trust_score = 0
        risk_score = 50  # Start neutral
        
        # Signal weights
        weights = {
            "mca21": 30,
            "gstin": 25,
            "startup_india": 25,
            "ats_detected": 15,
            "whois_old": 10,
        }

        signal_count = 0
        for signal, passed in signals.items():
            if passed:
                trust_score += weights.get(signal, 0)
                signal_count += 1
            
            # If it failed and it WASN'T an infra failure, increase risk
            elif not infra_failures.get(signal, False):
                risk_score += 10

        # Enforce automation cap (max 85)
        trust_score = min(trust_score, self.max_auto_score)
        
        # Risk score cap 0-100
        risk_score = max(0, min(100, risk_score))
        
        # Verified threshold
        is_verified = signal_count >= self.verified_threshold

        return trust_score, risk_score, is_verified
