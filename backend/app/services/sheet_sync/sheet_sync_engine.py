"""
Sheet Sync Engine — v2.
Maps Internships to the 9 target tabs in Google Sheets.
Tabs: APP ANDROID, Game development, APP IOS, WEB DEVELOPMENT, 
      Graphic Design, DATA SCIENCE, REJECTED, EXPIRED, NEEDS REVIEW.
"""
import logging
from typing import List
from app.models.internship import Internship, InternshipStatus
from app.services.sheet_sync.google_sheets_client import GoogleSheetsClient

logger = logging.getLogger(__name__)

# Spec Part 6 — Mandatory Tab Mapping
TAB_MAPPING = {
    "Android App Development": "APP ANDROID",
    "Game Development": "Game development",
    "iOS App Development": "APP IOS",
    "Web Development": "WEB DEVELOPMENT",
    "Graphic Design": "Graphic Design",
    "Data Science": "DATA SCIENCE",
}

class SheetSyncEngine:
    def __init__(self, client: GoogleSheetsClient):
        self.client = client

    def _format_row(self, i: Internship) -> List:
        """
        Formats a single internship for Sheet row output.
        Columns: Title, Company, Domain, WorkMode, Stipend, Link, LastDate.
        """
        # Column F (Apply Link) should be a HYPERLINK formula in Sheets
        link_formula = f'=HYPERLINK("{i.apply_link}", "Apply Now")' if i.apply_link else "N/A"
        
        return [
            i.title,
            i.domain or "N/A",
            i.work_mode.value if i.work_mode else "onsite",
            f"₹{i.stipend_min or 0}",
            link_formula,
            str(i.apply_by) if i.apply_by else "Open",
            str(i.posted_at.date()) if i.posted_at else "N/A",
        ]

    async def sync_all(self, internships: List[Internship]):
        """
        Synchronizes all internships into their respective tabs.
        Groups by domain and status.
        """
        if not self.client.service:
            logger.error("Sheets service not available. Sync aborted.")
            return

        tabs_data = {tab: [] for tab in TAB_MAPPING.values()}
        tabs_data["EXPIRED"] = []
        tabs_data["REJECTED"] = []
        tabs_data["NEEDS REVIEW"] = []

        for i in internships:
            row = self._format_row(i)
            
            if i.status == InternshipStatus.expired:
                tabs_data["EXPIRED"].append(row)
            elif i.status == InternshipStatus.rejected:
                tabs_data["REJECTED"].append(row)
            elif i.status == InternshipStatus.draft:
                tabs_data["NEEDS REVIEW"].append(row)
            elif i.status == InternshipStatus.active and i.domain in TAB_MAPPING:
                tab = TAB_MAPPING[i.domain]
                tabs_data[tab].append(row)

        # Batch update each tab
        for tab, rows in tabs_data.items():
            try:
                self.client.update_tab_batch(tab, rows)
                logger.info(f"Synced {len(rows)} rows to tab: {tab}")
            except Exception as e:
                logger.error(f"Failed to sync tab {tab}: {e}")
