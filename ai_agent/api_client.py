"""
RATIONALE:
Implements real interaction with Google Gemini via the new `google-genai` SDK (v1.0+).
Handles authentication via `GOOGLE_API_KEY` env var.
Supports text generation and tool calling.
"""

import os
import time
import json
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from google import genai
from google.genai import types

class LLMProvider(ABC):
    @abstractmethod
    def generate(self, system_prompt: str, user_content: str, tools: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Generates a response from the LLM.
        Returns a dictionary containing 'content' (str) and optionally 'tool_calls' (list).
        """
        pass

class GeminiProvider(LLMProvider):
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.5-flash"):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = model

    def generate(self, system_prompt: str, user_content: str, tools: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Calls Gemini API using the new SDK.
        """
        try:
            # 1. Config & Tools
            config = types.GenerateContentConfig(
                temperature=0.7,
                system_instruction=system_prompt
            )
            
            if tools:
                # Map JSON schema tools to the expected format
                # The SDK usually accepts a list of tool definitions.
                # We can pass raw dicts if formatted correctly as openapi function declarations
                # OR build types.Tool objects.
                # For simplicity, we construct the Tool object manually or pass dicts if supported.
                
                # Constructing FunctionDeclarations
                funcs = []
                for tool in tools:
                    funcs.append(types.FunctionDeclaration(
                        name=tool["name"],
                        description=tool["description"],
                        parameters=tool["parameters"]
                    ))
                
                tool_obj = types.Tool(function_declarations=funcs)
                config.tools = [tool_obj]

            # 2. Call API
            # Note: client.models.generate_content
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=user_content,
                config=config
            )

            # 3. Parse Response
            result = {"content": None, "tool_calls": []}
            
            # The response object has candidates -> content -> parts
            if response.candidates and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if part.function_call:
                        # It's a tool call
                        fc = part.function_call
                        result["tool_calls"].append({
                            "name": fc.name,
                            "arguments": fc.args # expected to be a dict/map
                        })
                    if part.text:
                        # It's text
                        if result["content"] is None:
                            result["content"] = part.text
                        else:
                            result["content"] += part.text

            if not result["content"] and not result["tool_calls"]:
                result["content"] = "No content generated."

            return result

        except Exception as e:
            print(f"DEBUG: Gemini SDK Error: {e}")
            raise e

class LLMClient:
    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def send_prompt(self, system_text: str, user_text: str, tools: Optional[List[Dict]] = None) -> Dict[str, Any]:
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # print(f"[LLMClient] Attempt {attempt+1}...")
                return self.provider.generate(system_prompt=system_text, user_content=user_text, tools=tools)
            except Exception as e:
                print(f"[LLMClient] Error on attempt {attempt+1}: {e}")
                time.sleep(2 * (attempt + 1))
        
        raise Exception("LLM Generation failed after max retries")

# Factory
def get_llm_client() -> LLMClient:
    return LLMClient(provider=GeminiProvider())
