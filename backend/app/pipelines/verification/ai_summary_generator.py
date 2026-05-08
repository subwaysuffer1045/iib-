"""
AI Summary Generator — v2.
Uses Anthropic Claude 3.5 Sonnet to generate a trust summary.
Implements spec §5.3 requirements.
"""
import anthropic
import json
from typing import Optional
from app.config import settings

class AISummaryGenerator:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = settings.ANTHROPIC_MODEL

    async def generate(self, company_name: str, signals: dict) -> Optional[str]:
        """
        Generates a 2-sentence trust summary.
        """
        if not settings.ANTHROPIC_API_KEY:
            return "Verification in progress."

        prompt = f"""
        Analyze these verification signals for the company '{company_name}':
        {json.dumps(signals)}
        
        Write a professional 2-sentence summary of their legitimacy for a student platform.
        Focus on confirmed registrations (MCA21, GST) and domain age.
        Return ONLY the 2 sentences. No intro.
        """
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=100,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text.strip()
        except Exception:
            return None

    def validate_ai_summary(self, summary: str) -> bool:
        """Spec requirement: Summary must be < 300 chars and >= 2 sentences."""
        if not summary: return False
        if len(summary) > 300: return False
        if summary.count('.') < 2: return False
        return True
