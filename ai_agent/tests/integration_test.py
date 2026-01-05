"""
RATIONALE:
Tests the entire flow:
1. Agent Router (Action Detection)
2. Agent Orchestrator (LLM Planning - Mocked)
3. Backend API (Tool Execution - Mocked Client)
"""

import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# Adjust path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from orchestrator.router import IntentRouter
from orchestrator.action_handler import ActionHandler

def test_router_classification():
    router = IntentRouter()
    # Test Action detection based on simple keyword logic in our mock router
    res = router.classify("Please remind me to take pills")
    assert res["category"] == "ACTION_REQUEST"
    
    res = router.classify("Hello there")
    assert res["category"] == "CASUAL_CHAT"

@patch("orchestrator.action_handler.get_llm_client")
@patch("orchestrator.action_handler.ToolClient")
def test_action_handler_reminder_flow(MockToolClient, MockLLMProvider):
    # Setup Mocks
    mock_llm = MockLLMProvider.return_value
    mock_tools = MockToolClient.return_value
    
    # Simulate LLM returning a tool call
    mock_llm.send_prompt.return_value = {
        "content": None,
        "tool_calls": [
            {
                "name": "schedule_reminder",
                "arguments": {
                    "message": "Take pills",
                    "schedule": "2023-10-27T08:00:00"
                }
            }
        ]
    }

    handler = ActionHandler()
    response_text = handler.handle("patient-id-123", "Remind me to take pills")

    # Assert Tool was called
    mock_tools.create_reminder.assert_called_once()
    assert "set a reminder" in response_text

if __name__ == "__main__":
    # verification run
    test_router_classification()
    print("✅ Intent Router Tests Passed")
    try:
        # We need to manually invoke the patch for main execution if not using pytest CLI
        # but for simplicity we rely on pytest usually. 
        print("Run `pytest` to execute all tests.")
    except:
        pass
