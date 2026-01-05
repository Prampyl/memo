"""
RATIONALE:
Orchestrates complex actions.
1. Receives intent & query.
2. formulated a PLAN using the LLM.
3. Executes tool calls if prescribed by the LLM.
4. Returns final natural language response.
"""

import sys
import os
import json
from datetime import datetime

# Adjust path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from api_client import get_llm_client
from rag.retriever import RAGRetriever
from tools.client import ToolClient
from tools.schemas import CreateReminderRequest

class ActionHandler:
    def __init__(self, tool_client: ToolClient = None):
        self.llm = get_llm_client()
        self.tools = tool_client or ToolClient()
        self.retriever = RAGRetriever()
        self.system_prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/base_system_prompt.md")

    def _load_base_prompt(self) -> str:
        with open(self.system_prompt_path, "r") as f:
            return f.read()

    def handle(self, patient_id: str, user_query: str) -> str:
        print(f"   [ActionHandler] Processing: {user_query}")

        # 1. RAG Retrieve
        docs = self.retriever.retrieve(patient_id, user_query)
        rag_context = "\n".join([f"- {d.text}" for d in docs]) if docs else "No relevant memory found."

        # 2. Prepare Context
        # In a real app, inject real patient data here
        system_prompt = self._load_base_prompt()\
            .replace("{{ patient_name }}", "Alice")\
            .replace("{{ current_time }}", datetime.now().isoformat())\
            .replace("{{ caregiver_name }}", "John")\
            .replace("{{ patient_diagnosis }}", "Moderate") \
            + f"\n\n# MEMORY CONTEXT\n{rag_context}"

        # 3. Get LLM Response (with Tools)
        defined_tools = json.load(open(os.path.join(os.path.dirname(__file__), "../prompts/tool_call_template.json")))["tools"]
        
        response = self.llm.send_prompt(system_prompt, user_query, tools=defined_tools)

        # 3. Process Response
        agent_content = response.get("content")
        tool_calls = response.get("tool_calls", [])

        # 4. Execute Tools
        # 4. Execute Tools & Re-prompt
        if tool_calls:
            tool_outputs = []
            for tool in tool_calls:
                name = tool["name"]
                args = tool["arguments"]
                print(f"   [Tool Call] {name}({args})")

                output = None
                try:
                    if name == "schedule_reminder":
                        req = CreateReminderRequest(
                            patientId=patient_id,
                            message=args.get("text"),
                            schedule=args.get("time_iso", datetime.now().isoformat())
                        )
                        resp = self.tools.create_reminder(req)
                        output = f"Reminder Scheduled: ID={resp.id}"
                    
                    elif name == "search_memory":
                        # We might need to map args if they differ, but usually it's 'query'
                        # Check schema: MemorySearchRequest(patient_id, query)
                        # The LLM tool def uses 'query'.
                        from tools.schemas import MemorySearchRequest
                        req = MemorySearchRequest(
                            patient_id=patient_id,
                            query=args.get("query")
                        )
                        resp = self.tools.search_memory(req)
                        
                        # Format facts
                        found_facts = [f.text for f in resp.facts]
                        output = f"Memory Search Results: {json.dumps(found_facts)}" if found_facts else "Memory Search: No results found."

                    elif name == "log_event":
                        from tools.schemas import LogEventRequest
                        req = LogEventRequest(
                            patient_id=patient_id,
                            event_type=args.get("event_type", "observation"),
                            description=args.get("description", "No description")
                        )
                        success = self.tools.log_event(req)
                        output = "Event Logged Successfully" if success else "Failed to log event"
                    
                    else:
                        output = f"Error: Unknown tool '{name}'"
                
                except Exception as e:
                    output = f"Error executing {name}: {str(e)}"
                
                tool_outputs.append(f"Tool '{name}' returned: {output}")

            # 5. Final Synthesis
            # We feed the tool outputs back to the LLM to get a natural response
            print(f"   [Observation] {tool_outputs}")
            
            tool_feedback_prompt = (
                f"Context: The user asked '{user_query}'.\n"
                f"You decided to call tools. Here are the results:\n"
                f"{chr(10).join(tool_outputs)}\n\n"
                f"Instruction: Use these results to answer the user naturally. Do not expose internal IDs."
            )
            
            # Call LLM again (without tools this time to force a text answer)
            final_response = self.llm.send_prompt(system_prompt, tool_feedback_prompt, tools=None)
            return final_response.get("content") or "I completed the action."

        return agent_content or "I've processed your request."
