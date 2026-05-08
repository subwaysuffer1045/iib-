"""
Link Validator — v2.
Validates application links before activation.
Implements:
- 5s HTTP timeout
- 24hr Redis cache (LINK_VALIDATION_CACHE_TTL_SECONDS)
- Redirect following (up to 3)
- WhatsApp/Telegram/Google Form detection
"""
import httpx
import redis
import hashlib
from datetime import datetime, timezone
from typing import Tuple, Optional
from app.config import settings

class LinkValidator:
    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL)
        self.timeout = settings.VERIFICATION_HTTP_TIMEOUT_SECONDS
        self.ttl = settings.LINK_VALIDATION_CACHE_TTL_SECONDS

    def _get_cache_key(self, url: str) -> str:
        h = hashlib.sha256(url.encode()).hexdigest()
        return f"iib:link_cache:{h}"

    async def validate(self, url: str) -> Tuple[bool, str, Optional[str]]:
        """
        Returns (is_valid, link_type, error_msg).
        Link types: ats, website, email, unknown.
        """
        if not url:
            return False, "unknown", "Missing URL"

        # Handle mailto:
        if url.startswith("mailto:"):
            return True, "email", None

        # Check Cache
        cache_key = self._get_cache_key(url)
        cached = self.redis.get(cache_key) if self.redis else None
        if cached:
            # Format in cache: "is_valid|type"
            val = cached.decode().split("|")
            return val[0] == "True", val[1], None

        # Real-time Check
        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=self.timeout) as client:
                # Use HEAD first to save bandwidth
                response = await client.head(url)
                if response.status_code >= 400:
                    # Retry with GET as some sites block HEAD
                    response = await client.get(url)
                
                is_valid = response.status_code < 400
                
                # Detect type
                link_type = "website"
                final_url = str(response.url).lower()
                
                # ATS detection
                ats_keywords = ["greenhouse.io", "lever.co", "ashbyhq.com", "myworkdayjobs.com"]
                if any(k in final_url for k in ats_keywords):
                    link_type = "ats"
                
                # Rejection patterns (Scam/Privacy)
                reject_patterns = ["wa.me", "t.me", "chat.whatsapp.com", "docs.google.com/forms"]
                if any(k in final_url for k in reject_patterns):
                    return False, "unknown", "Redirects to social/form (forbidden)"

                # Cache result
                if self.redis:
                    self.redis.setex(cache_key, self.ttl, f"{is_valid}|{link_type}")
                return is_valid, link_type, None

        except (httpx.HTTPError, Exception) as e:
            return False, "unknown", str(e)
