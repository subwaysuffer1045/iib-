"""
MCA21 Scraper — v2.
Public portal lookup for Indian Corporate Identification Number (CIN).
Signals pass if active record found.
"""
import httpx
import re
from bs4 import BeautifulSoup
from typing import Tuple, Optional
from app.config import settings

class MCA21Scraper:
    def __init__(self):
        self.url = settings.MCA21_API_URL
        self.timeout = settings.MCA21_TIMEOUT_SECONDS

    async def check_cin(self, cin: str) -> Tuple[bool, Optional[str], bool]:
        """
        Returns (passed, status_text, is_infra_failure).
        """
        if not cin:
            return False, None, False
            
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Note: Real MCA portal requires handling ASP.NET ViewState/Cookies.
                # This is a simplified scraper logic.
                params = {"cin": cin}
                response = await client.get(self.url, params=params)
                
                if response.status_code != 200:
                    return False, None, True
                    
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Logic to find 'Active' status in the result table
                status_element = soup.find(string=re.compile(r'Active', re.I))
                if status_element:
                    return True, "Active", False
                    
                return False, "Not Found / Inactive", False

        except Exception:
            return False, None, True
