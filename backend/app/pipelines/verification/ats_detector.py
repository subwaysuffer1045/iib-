"""
ATS Detector — v2.
Identifies if the company uses a premium Applicant Tracking System.
Known ATS = Greenhouse, Lever, Ashby, Workday, SmartRecruiters.
"""
from typing import Tuple

ATS_DOMAINS = [
    "greenhouse.io",
    "lever.co",
    "ashbyhq.com",
    "myworkdayjobs.com",
    "smartrecruiters.com",
    "bamboohr.com",
    "recruitee.com",
]

class AtsDetector:
    def detect(self, apply_link: str) -> Tuple[bool, str]:
        """
        Returns (is_ats, ats_type).
        """
        if not apply_link:
            return False, "none"
            
        link_lower = apply_link.lower()
        
        for ats in ATS_DOMAINS:
            if ats in link_lower:
                # Extract type name from domain (e.g. greenhouse)
                ats_type = ats.split('.')[0]
                return True, ats_type
                
        return False, "none"
