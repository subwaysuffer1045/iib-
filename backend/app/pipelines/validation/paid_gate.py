"""
Paid Gate Pipeline — v2.
Simplified version that uses normalized stipend data.
Enforces "Every internship is paid" mandate.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from app.models.internship import StipendConfidence


# ── Fee-scam hard-fail keywords ───────────────────────────────────────────────
_FEE_SCAM_PATTERNS = [
    "registration fee", "training fee", "deposit required",
    "security deposit", "pay to apply", "payment required to join",
    "refundable deposit",
]


@dataclass
class FeeScamResult:
    is_hard_fail: bool
    hard_fail_reason: Optional[str] = None


@dataclass
class PaidStatusResult:
    is_paid: bool
    confidence: Optional[str] = None


def detect_fee_scam(description: str, apply_url: Optional[str] = None) -> FeeScamResult:
    """
    Checks description (and optionally the apply URL) for fee-scam signals.
    Returns a FeeScamResult with is_hard_fail=True if any hard-fail pattern found.
    """
    text = (description or "").lower()
    for pattern in _FEE_SCAM_PATTERNS:
        if pattern in text:
            return FeeScamResult(is_hard_fail=True, hard_fail_reason=f"Fee-scam keyword detected: '{pattern}'")
    return FeeScamResult(is_hard_fail=False)


def evaluate_paid_status(stipend_text: str, description: str = "") -> PaidStatusResult:
    """
    Evaluates whether an internship is paid based on stipend text and description.
    Returns PaidStatusResult with is_paid flag and confidence level string.
    """
    text = (stipend_text or "").lower().strip()
    desc = (description or "").lower()

    # Explicitly unpaid signals
    unpaid_keywords = ["unpaid", "no stipend", "volunteer", "honorarium only", "0 stipend"]
    for kw in unpaid_keywords:
        if kw in text or kw in desc:
            return PaidStatusResult(is_paid=False, confidence="high")

    # Check for a number in stipend text
    import re
    numbers = re.findall(r"\d+", text)
    if numbers:
        amount = int(numbers[0])
        if amount > 0:
            return PaidStatusResult(is_paid=True, confidence="high" if amount > 100 else "medium")
        return PaidStatusResult(is_paid=False, confidence="high")

    # If we find currency symbols with no number, treat as low confidence
    if any(sym in text for sym in ["₹", "rs", "inr"]):
        return PaidStatusResult(is_paid=True, confidence="low")

    return PaidStatusResult(is_paid=False, confidence="low")


class PaidGate:
    def __init__(self, min_stipend: float = 1.0):
        self.min_stipend = min_stipend

    def check(self, internship_data: dict) -> bool:
        """
        Returns True if the internship passes the paid gate.
        Expects keys from Normalizer: stipend_min, stipend_confidence.
        """
        stipend = internship_data.get("stipend_min")
        confidence = internship_data.get("stipend_confidence")

        # Rejects explicitly unpaid or zero stipend
        if stipend is not None and stipend <= 0:
            return False

        # Rejects if stipend is missing entirely
        if stipend is None:
            return False

        # Rejects if confidence is low (needs manual review/fix)
        if confidence == StipendConfidence.low:
            return False

        # Must meet minimum stipend (usually 1 INR)
        return stipend >= self.min_stipend

