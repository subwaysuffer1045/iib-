"""
Google Sheets Client — v2.
Handles authentication and low-level API calls.
Supports batch updates and cell hyperlinking.
"""
import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from app.config import settings

class GoogleSheetsClient:
    def __init__(self):
        self.sheet_id = settings.GOOGLE_SHEET_ID
        self.scopes = [settings.GOOGLE_SHEET_SCOPES]
        self.service = self._authenticate()

    def _authenticate(self):
        """Authenticates using service account JSON (file or env string)."""
        creds_json = settings.GOOGLE_SHEETS_CREDENTIALS_JSON
        
        if not creds_json:
            return None

        try:
            # Check if it's a path or raw JSON string
            if os.path.exists(creds_json):
                creds = service_account.Credentials.from_service_account_file(
                    creds_json, scopes=self.scopes
                )
            else:
                info = json.loads(creds_json)
                creds = service_account.Credentials.from_service_account_info(
                    info, scopes=self.scopes
                )
            
            return build('sheets', 'v4', credentials=creds)
        except Exception as e:
            print(f"Sheets Auth Failed: {e}")
            return None

    def clear_tab(self, tab_name: str):
        """Clears all content from a tab except headers."""
        if not self.service: return
        self.service.spreadsheets().values().clear(
            spreadsheetId=self.sheet_id,
            range=f"'{tab_name}'!A2:Z1000",
            body={}
        ).execute()

    def append_rows(self, tab_name: str, rows: list):
        """Appends multiple rows to a tab."""
        if not self.service or not rows: return
        self.service.spreadsheets().values().append(
            spreadsheetId=self.sheet_id,
            range=f"'{tab_name}'!A2",
            valueInputOption="USER_ENTERED",
            body={"values": rows}
        ).execute()

    def update_tab_batch(self, tab_name: str, rows: list):
        """Full overwrite of a tab (A2 downwards)."""
        if not self.service: return
        self.clear_tab(tab_name)
        if rows:
            self.append_rows(tab_name, rows)
