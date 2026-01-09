import sys
import os
import json
from dotenv import load_dotenv

# Add root to path so imports work
sys.path.append(os.getcwd())
load_dotenv()

# FORCE MOCK MODE for demo purposes (bypassing region block and latency)
os.environ["USE_MOCK_LLM"] = "true"

from ai_agent.orchestrator.action_handler import ActionHandler

def main():
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Usage: python run_agent.py <patient_id> <prompt>"}), file=sys.stderr)
        sys.exit(1)

    patient_id = sys.argv[1]
    user_prompt = sys.argv[2]
    
    try:
        # Initialize the agent
        # Assuming ActionHandler takes care of everything as seen in chat_demo.py
        agent = ActionHandler()
        
        # Get response
        response = agent.handle(patient_id, user_prompt)
        
        # Output JSON result
        result = {
            "success": True,
            "response": response
        }
        print(json.dumps(result))
        
    except Exception as e:
        error_result = {
            "success": False,
            "error": str(e)
        }
        print(json.dumps(error_result), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
