"""
RATIONALE:
Orchestrates the classification of user intent using the `intent_classifier_prompt.md`.
Parses the LLM output into a structured decision.
"""

import json
import os
from typing import Dict, Any

class IntentRouter:
    def __init__(self, llm_client=None):
        # TODO: Pass actual LLM client interface
        self.llm = llm_client
        self.prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/intent_classifier_prompt.md")

    def _load_prompt(self) -> str:
        with open(self.prompt_path, "r") as f:
            return f.read()

    def classify(self, user_query: str) -> Dict[str, Any]:
        """
        Returns { "category": "...", "confidence": ... }
        """
        template = self._load_prompt()
        filled_prompt = template.replace("{{ user_query }}", user_query)
        
        # TODO: Replace with actual LLM Call
        # response = self.llm.generate(filled_prompt)
        
        print(f"[Router] Classifying: {user_query}")
        
        # Mock Logic for Scaffolding
        lower_q = user_query.lower()
        if "remind" in lower_q:
            return {"category": "ACTION_REQUEST", "confidence": 0.9}
        elif "who" in lower_q or "what" in lower_q:
            return {"category": "INFORMATION_QUERY", "confidence": 0.85}
        elif "help" in lower_q or "pain" in lower_q:
            return {"category": "EMERGENCY", "confidence": 1.0}
        else:
            return {"category": "CASUAL_CHAT", "confidence": 0.8}
