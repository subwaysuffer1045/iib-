from dataclasses import dataclass
from typing import Optional
import re
from app.models.internship import WorkMode

@dataclass
class NormalizedLocation:
    city: Optional[str]
    state: Optional[str]
    country: str
    work_mode: WorkMode
    is_remote: bool
    location_text: str

CITY_STATE_MAP = {
    "mumbai": ("Mumbai", "Maharashtra"),
    "navi mumbai": ("Navi Mumbai", "Maharashtra"),
    "pune": ("Pune", "Maharashtra"),
    "nagpur": ("Nagpur", "Maharashtra"),
    "thane": ("Thane", "Maharashtra"),
    "bengaluru": ("Bengaluru", "Karnataka"),
    "bangalore": ("Bengaluru", "Karnataka"),
    "mysuru": ("Mysuru", "Karnataka"),
    "mysore": ("Mysuru", "Karnataka"),
    "hyderabad": ("Hyderabad", "Telangana"),
    "secunderabad": ("Secunderabad", "Telangana"),
    "chennai": ("Chennai", "Tamil Nadu"),
    "coimbatore": ("Coimbatore", "Tamil Nadu"),
    "kochi": ("Kochi", "Kerala"),
    "cochin": ("Kochi", "Kerala"),
    "thiruvananthapuram": ("Thiruvananthapuram", "Kerala"),
    "delhi": ("Delhi", "Delhi"),
    "new delhi": ("Delhi", "Delhi"),
    "gurgaon": ("Gurugram", "Haryana"),
    "gurugram": ("Gurugram", "Haryana"),
    "noida": ("Noida", "Uttar Pradesh"),
    "faridabad": ("Faridabad", "Haryana"),
    "ghaziabad": ("Ghaziabad", "Uttar Pradesh"),
    "kolkata": ("Kolkata", "West Bengal"),
    "calcutta": ("Kolkata", "West Bengal"),
    "ahmedabad": ("Ahmedabad", "Gujarat"),
    "surat": ("Surat", "Gujarat"),
    "jaipur": ("Jaipur", "Rajasthan"),
    "lucknow": ("Lucknow", "Uttar Pradesh"),
    "chandigarh": ("Chandigarh", "Punjab"),
    "indore": ("Indore", "Madhya Pradesh"),
    "bhopal": ("Bhopal", "Madhya Pradesh"),
    "bhubaneswar": ("Bhubaneswar", "Odisha"),
    "patna": ("Patna", "Bihar"),
    "ranchi": ("Ranchi", "Jharkhand"),
    "guwahati": ("Guwahati", "Assam"),
}

REMOTE_KEYWORDS = [
    'work from home', 'wfh', 'remote', 'anywhere', 
    'pan india', 'all india', 'virtual', 'work from anywhere',
    'home based', 'online'
]

HYBRID_KEYWORDS = ['hybrid', '2-3 days', 'flexible working', 'partial remote']

def normalize_location(raw_location: str) -> NormalizedLocation:
    if not raw_location:
        return NormalizedLocation(None, None, "India", WorkMode.onsite, False, "")
    
    lower = raw_location.lower().strip()
    
    # Check remote
    for kw in REMOTE_KEYWORDS:
        if kw in lower:
            return NormalizedLocation(
                city=None, state=None, country="India",
                work_mode=WorkMode.remote, is_remote=True,
                location_text=raw_location
            )
    
    # Check hybrid
    for kw in HYBRID_KEYWORDS:
        if kw in lower:
            for city_key, (city_name, state_name) in CITY_STATE_MAP.items():
                if city_key in lower:
                    return NormalizedLocation(
                        city=city_name, state=state_name, country="India",
                        work_mode=WorkMode.hybrid, is_remote=False,
                        location_text=raw_location
                    )
            return NormalizedLocation(
                city=None, state=None, country="India",
                work_mode=WorkMode.hybrid, is_remote=False,
                location_text=raw_location
            )
    
    # Check city match
    for city_key, (city_name, state_name) in CITY_STATE_MAP.items():
        if city_key in lower:
            return NormalizedLocation(
                city=city_name, state=state_name, country="India",
                work_mode=WorkMode.onsite, is_remote=False,
                location_text=raw_location
            )
    
    # Unknown location
    return NormalizedLocation(
        city=None, state=None, country="India",
        work_mode=WorkMode.onsite, is_remote=False,
        location_text=raw_location
    )
