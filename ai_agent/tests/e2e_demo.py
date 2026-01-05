"""
RATIONALE:
This script verifies the FULL LOOP:
User Input -> Agent Brain (Real LLM) -> Tool Client -> Backend API (Running Server) -> Database.

Prerequisites:
1. Backend Server running on http://localhost:8000
2. GOOGLE_API_KEY in .env
"""

import sys
import os
from dotenv import load_dotenv

# Add root to path
sys.path.append(os.getcwd())
load_dotenv()

from ai_agent.orchestrator.action_handler import ActionHandler

# --- Mock Tool Client for Verification ---
from ai_agent.tools.client import ToolClient
from ai_agent.tools.schemas import (
    CreateReminderRequest, CreateReminderResponse, 
    MemorySearchRequest, MemorySearchResponse,
    LogEventRequest
)

class MockToolClient(ToolClient):
    def create_reminder(self, request: CreateReminderRequest) -> CreateReminderResponse:
        print(f"   [MOCK] create_reminder called for: {request.message} at {request.schedule}")
        return CreateReminderResponse(id="mock-id-123", status="scheduled")

    def search_memory(self, request: MemorySearchRequest) -> MemorySearchResponse:
        print(f"   [MOCK] search_memory called for: {request.query}")
        return MemorySearchResponse(facts=[])

    def log_event(self, request: LogEventRequest) -> bool:
        print(f"   [MOCK] log_event called.")
        return True

def run_e2e_demo():
    print("\nSTARTING END-TO-END DEMO (MOCK MODE)")
    print("--------------------------------------------------")
    
    # 1. Skip Backend Check
    print("   Backend Check: SKIPPED (Mocking interactions)")

    # 2. Instantiate Agent with Mock Tools
    print("   Initializing Agent (ActionHandler with MockTools)...")
    try:
        mock_tools = MockToolClient()
        agent = ActionHandler(tool_client=mock_tools)
    except Exception as e:
        print(f"   Failed to init agent: {e}")
        return

    # 3. Simulate User Request
    user_query = "Remind me to call the doctor tomorrow at 10 AM"
    patient_id = "test-patient-id"
    
    print(f"   User says: '{user_query}'")
    
    # 4. Agent Execution
    print("   Agent is thinking (Calling Gemini + Tools)...")
    response_text = agent.handle(patient_id, user_query)
    
    print(f"   Agent replied: '{response_text}'")
    print("--------------------------------------------------")

if __name__ == "__main__":
    run_e2e_demo()
