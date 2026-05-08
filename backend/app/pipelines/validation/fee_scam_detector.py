"""
Fee Scam Detector — v2.
Scans for payment demands, training fees, and scam keywords.
Triggers PERMANENT REJECTION (hard fail).
"""
import re
from typing import Optional, Tuple

# Patterns that trigger an immediate Hard Fail (Scam)
HARD_FAIL_PATTERNS = [
    (r'\btraining fee\b', 'Demands training fee'),
    (r'\bregistration fee\b', 'Demands registration fee'),
    (r'\bsecurity deposit\b', 'Demands security deposit'),
    (r'\bjoining\s*fee\b', 'Demands joining fee'),
    (r'\bcertificate fee\b', 'Demands certificate fee'),
    (r'\bpay\s+to\s+(?:join|apply|work|start)\b', 'Demands payment to work'),
    (r'\brefundable\s+deposit\b', 'Demands refundable deposit (fraud pattern)'),
    (r'pay\s*[₹$]\s*\d+', 'Direct payment solicitation'),
    (r'\bwhatsapp\s+group\b', 'Redirects to unofficial WhatsApp group'),
    (r'\btreasure\s+hunt\b', 'Gamified scam pattern'),
    (r'\bmulti-level\b', 'MLM pattern detected'),
]

class FeeScamDetector:
    def detect(self, text: str) -> Tuple[bool, Optional[str]]:
        """
        Returns (is_scam, reason).
        Scans title, description, and raw stipend text.
        """
        if not text:
            return False, None
            
        text_lower = text.lower()
        
        for pattern, reason in HARD_FAIL_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return True, reason
                
        return False, None
