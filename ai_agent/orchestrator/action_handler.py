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

class ActionHandler:
    def __init__(self):
        self.llm = get_llm_client()
        self.tools = ToolClient()
        self.retriever = RAGRetriever()
        self.system_prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/base_system_prompt.md")

    def _load_base_prompt(self) -> str:
        with open(self.system_prompt_path, "r") as f:
            return f.read()

    def handle(self, patient_id: str, user_query: str) -> str:
        print(f"⚙️ [ActionHandler] Processing: {user_query}")

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
        if tool_calls:
            for tool in tool_calls:
                name = tool["name"]
                args = tool["arguments"]
                print(f"🔨 [Tool Call] {name}({args})")

                if name == "schedule_reminder":
                    req = CreateReminderRequest(
                        patient_id=patient_id,
                        message=args.get("message"),
                        schedule=args.get("schedule", datetime.now().isoformat())
                    )
                    self.tools.create_reminder(req)
                    return f"I've set a reminder for you to {args.get('message')}."
                
                # TODO: Handle other tools

        return agent_content or "I've processed your request."
