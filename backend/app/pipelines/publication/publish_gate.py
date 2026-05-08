from dataclasses import dataclass
from datetime import date
from typing import Optional
import uuid

@dataclass
class PublishDecision:
    should_publish: bool
    reason: str
    action: str  # 'publish', 'review', 'reject'

def decide_publish_eligibility(internship, company=None) -> PublishDecision:
    """
    All conditions must be true to publish.
    Order matters — check cheapest/most certain first.
    """
    # Check 1: Company hard fail (if company provided)
    if company and company.has_payment_demand:
        return PublishDecision(False, "Company has payment demand flag. Permanent.", "reject")
    
    # Check 2: Not expired
    if internship.apply_by and internship.apply_by < date.today():
        return PublishDecision(False, "Internship deadline has passed", "reject")
    
    # Check 3: Paid gate — CRITICAL
    if not internship.is_paid:
        return PublishDecision(False, "is_paid = False. Paid gate failed.", "reject")
    if internship.payment_confidence < 70:
        return PublishDecision(False, f"payment_confidence {internship.payment_confidence} < 70", "review")
    
    # Check 4: Verification status
    if internship.verification_status.value == "rejected":
        return PublishDecision(False, "Verification status: rejected", "reject")
    if internship.verification_status.value == "draft":
        return PublishDecision(False, "Verification not started", "review")
    if internship.verification_status.value == "pending":
        return PublishDecision(False, "Verification running", "review")
    
    # Check 5: needs_review requires admin approval
    if internship.verification_status.value == "needs_review":
        if not internship.admin_approved:
            return PublishDecision(False, "Needs admin review and approval", "review")
        if internship.trust_score < 55:
            return PublishDecision(False, f"Trust score {internship.trust_score} too low", "review")
    
    # Check 6: Trust floor for verified
    if internship.verification_status.value == "verified" and internship.trust_score < 50:
        return PublishDecision(False, f"Trust score {internship.trust_score} below floor", "review")
    
    return PublishDecision(True, "All gates passed", "publish")
