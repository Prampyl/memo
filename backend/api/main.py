"""
RATIONALE:
FastAPI server to expose the Database Manager as a REST API.
This allows the AI Agent (and Frontend) to interact with the system's "Body".
Includes Pydantic models for validation.
"""

from fastapi import FastAPI, HTTPException, Body, Query, Depends, Security
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

# Add parent directory to path to import models
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from models.db_manager import MemoDB

app = FastAPI(title="Memo Backend", version="1.0.0")
db = MemoDB()

# --- Security ---
API_KEY_NAME = "X-API-KEY"
API_KEY = os.getenv("BACKEND_API_KEY", "memo-secret-key") # Default for dev
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header != API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return api_key_header

# --- Shared Models ---
class ReminderCreate(BaseModel):
    patientId: str
    message: str
    schedule: str # ISO8601
    category: str = "General"

class LogCreate(BaseModel):
    requestId: str
    agentPlan: List[str]
    toolCalls: List[dict]
    response: str

# --- Endpoints ---

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/memory", dependencies=[Depends(get_api_key)])
def get_memory(patient_id: str = Query(..., alias="patientId")):
    """
    Retrieves facts/memory for a patient.
    """
    media = db.get_patient_media(patient_id)
    reminders = db.get_patient_reminders(patient_id)
    
    facts = []
    for m in media:
        facts.append({"id": str(m['id']), "text": m['description'], "category": "media", "updated_at": "2023-01-01"})
    for r in reminders:
        facts.append({"id": str(r['id']), "text": r['spoken_message'], "category": "reminder", "updated_at": "2023-01-01"})
        
    return {"facts": facts}

@app.post("/reminders", dependencies=[Depends(get_api_key)])
def create_reminder(body: ReminderCreate):
    try:
        # Note: db_manager signature differs slightly, adapting here
        db.add_reminder(body.patientId, "Reminder", body.message, body.schedule, body.category)
        return {"id": "mock-uuid", "status": "scheduled"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/logs", dependencies=[Depends(get_api_key)])
def create_log(body: LogCreate):
    # TODO: Implement structured logging to DB
    print(f"📝 [LOG] Request {body.requestId}: {body.response}")
    return {"status": "logged"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
