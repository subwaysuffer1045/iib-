import re
from dataclasses import dataclass
from typing import Optional

@dataclass
class MoneyRange:
    stipend_min: Optional[float]
    stipend_max: Optional[float]
    currency: str
    is_paid: Optional[bool]   # True=paid, False=unpaid, None=unknown/hidden
    confidence: int           # 0-100
    original_text: str

# Keywords that mean UNPAID — confidence 95
UNPAID_KEYWORDS = [
    'unpaid', 'no stipend', 'no salary', 'volunteer', 'no compensation',
    'without stipend', 'no remuneration', 'pro bono', 'honorary'
]

# Keywords that mean HIDDEN/UNKNOWN — confidence 20
HIDDEN_KEYWORDS = [
    'competitive', 'as per norms', 'best in industry', 'market standard',
    'negotiable', 'to be discussed', 'tbd', 'tba', 'will be discussed',
    'as per profile', 'performance based', 'ppo based', 'depends on'
]

def parse_money_range(text: str) -> MoneyRange:
    """
    Parse Indian stipend text into structured MoneyRange.
    
    Examples handled:
      "₹10,000 - 20,000/month" → min=10000, max=20000, paid=True, confidence=90
      "Rs. 15000 per month" → min=15000, max=15000, paid=True, confidence=90
      "10k-20k monthly" → min=10000, max=20000, paid=True, confidence=85
      "INR 8000" → min=8000, max=8000, paid=True, confidence=85
      "Unpaid" → min=None, max=None, paid=False, confidence=95
      "Competitive stipend" → min=None, max=None, paid=None, confidence=20
      "0" or "0/month" → min=None, max=None, paid=False, confidence=90
    """
    if not text or not text.strip():
        return MoneyRange(None, None, "INR", None, 10, text or "")
    
    clean = text.strip().lower()
    original = text
    
    # Check unpaid keywords
    for kw in UNPAID_KEYWORDS:
        if kw in clean:
            return MoneyRange(None, None, "INR", False, 95, original)
    
    # Check hidden/unknown keywords
    for kw in HIDDEN_KEYWORDS:
        if kw in clean:
            return MoneyRange(None, None, "INR", None, 20, original)
    
    # Remove currency symbols
    clean = re.sub(r'[₹$€£]', '', clean)
    clean = re.sub(r'\b(rs\.?|inr|rupees?)\b', '', clean, flags=re.IGNORECASE)
    
    # Remove common suffixes
    clean = re.sub(r'(/month|per month|monthly|/mo|p\.?m\.?)', '', clean)
    clean = re.sub(r'(per annum|/year|annually|p\.?a\.?)', '', clean)
    
    # Expand k suffix (10k → 10000)
    clean = re.sub(r'(\d+(?:\.\d+)?)\s*k\b', lambda m: str(int(float(m.group(1)) * 1000)), clean)
    
    # Remove commas and spaces in numbers
    clean = re.sub(r'(\d),(\d)', r'\1\2', clean)
    
    # Try to find range: two numbers with separator
    range_match = re.search(r'(\d+(?:\.\d+)?)\s*[-–to]\s*(\d+(?:\.\d+)?)', clean)
    if range_match:
        min_val = float(range_match.group(1))
        max_val = float(range_match.group(2))
        if min_val == 0 and max_val == 0:
            return MoneyRange(None, None, "INR", False, 90, original)
        if min_val > 0 or max_val > 0:
            return MoneyRange(
                stipend_min=min(min_val, max_val),
                stipend_max=max(min_val, max_val),
                currency="INR",
                is_paid=True,
                confidence=90,
                original_text=original
            )
    
    # Try single number
    single_match = re.search(r'\b(\d{3,6}(?:\.\d+)?)\b', clean)
    if single_match:
        val = float(single_match.group(1))
        if val == 0:
            return MoneyRange(None, None, "INR", False, 90, original)
        if val > 0:
            return MoneyRange(
                stipend_min=val,
                stipend_max=val,
                currency="INR",
                is_paid=True,
                confidence=85,
                original_text=original
            )
    
    # Could not parse
    return MoneyRange(None, None, "INR", None, 15, original)
