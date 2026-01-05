"""
RATIONALE:
Defines Pydantic models for all tool interactions.
Ensures strict validation of inputs before sending to the Backend API.
Matches structure in `tool_call_template.json` and `TOOL_DOCS.md`.
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime

# --- Shared Models ---
class ToolResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None

# --- Reminder Tool ---
class CreateReminderRequest(BaseModel):
    patientId: str = Field(..., description="UUID of the patient")
    message: str = Field(..., description="The spoken message content")
    schedule: str = Field(..., description="ISO8601 formatted datetime string")
    category: str = "General"

class CreateReminderResponse(BaseModel):
    id: str
    status: str

# --- Memory/RAG Tool ---
class MemorySearchRequest(BaseModel):
    patient_id: str
    query: str
    limit: int = 5

class MemoryFact(BaseModel):
    id: str
    text: str
    category: str
    updated_at: datetime

class MemorySearchResponse(BaseModel):
    facts: List[MemoryFact]

# --- Logging Tool ---
class LogEventRequest(BaseModel):
    request_id: str
    agent_plan: List[str]
    tool_calls: List[dict]
    response: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# TODO: Add validation regex for UUIDs if strictly required
