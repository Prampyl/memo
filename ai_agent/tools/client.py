"""
RATIONALE:
Implements the HTTP interface defined in `TOOL_DOCS.md`.
Decouples the Agent from direct Database access.
Uses synchronous `requests` for simplicity, but could be async.
"""

import os
import requests
from typing import Optional, Dict, Any
from .schemas import (
    CreateReminderRequest, CreateReminderResponse,
    LogEventRequest, MemorySearchRequest, MemorySearchResponse
)

class ToolClient:
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = base_url or os.getenv("BACKEND_API_URL", "http://localhost:8000")
        self.api_key = api_key or os.getenv("BACKEND_API_KEY", "memo-secret-key")
        self.headers = {
            "Content-Type": "application/json",
            "X-API-KEY": self.api_key
        }

    def _post(self, endpoint: str, data: BaseModel) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        try:
            resp = requests.post(url, json=data.model_dump(mode='json'), headers=self.headers, timeout=5)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            # TODO: Improve error handling strategy (retry/fallback)
            print(f"ToolClient Error [{endpoint}]: {e}")
            raise e

    def _get(self, endpoint: str, params: dict) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        try:
            resp = requests.get(url, params=params, headers=self.headers, timeout=5)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
             print(f"ToolClient Error [{endpoint}]: {e}")
             raise e

    def create_reminder(self, request: CreateReminderRequest) -> CreateReminderResponse:
        data = self._post("/reminders", request)
        return CreateReminderResponse(**data)

    def log_event(self, request: LogEventRequest) -> bool:
        """Returns True if log successful, non-blocking failure preferred."""
        try:
            self._post("/logs", request)
            return True
        except:
            return False

    def search_memory(self, request: MemorySearchRequest) -> MemorySearchResponse:
        data = self._get("/memory", params=request.model_dump(mode='json'))
        return MemorySearchResponse(**data)
