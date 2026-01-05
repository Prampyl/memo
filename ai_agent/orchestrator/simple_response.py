"""
RATIONALE:
Handles the 'CASUAL_CHAT' intent.
Uses `simple_response_template` to generate a grounded, empathetic response.
"""

import os
from ..rag.retriever import RAGRetriever

class SimpleResponseHandler:
    def __init__(self, retriever: RAGRetriever):
        self.retriever = retriever
        self.prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/simple_response_template.md")

    def handle(self, patient_id: str, user_query: str, history: list) -> str:
        # 1. Retrieve Context
        docs = self.retriever.retrieve(patient_id, user_query)
        context_str = "\n".join([f"- {d.text}" for d in docs])

        # 2. Load Prompt
        with open(self.prompt_path, "r") as f:
            template = f.read()

        # 3. Fill Prompt
        # TODO: Inject real patient data
        final_prompt = template\
            .replace("{{ patient_name }}", "Alice")\
            .replace("{{ conversation_history }}", str(history))\
            .replace("{{ semantic_memory_snippets }}", context_str)

        # 4. Generate (Mock)
        print(f"[SimpleResponse] Generated prompt:\n{final_prompt[:100]}...")
        return "I understand, Alice. That sounds lovely."
