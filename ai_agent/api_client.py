"""
RATIONALE:
Implements real interaction with Google Gemini via `google-generativeai`.
Handles authentication via `GOOGLE_API_KEY` env var.
Supports text generation and tool calling (Function Calling).
Includes retry logic with exponential backoff.
"""

import os
import time
import json
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
import google.generativeai as genai
from google.api_core import exceptions

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
        
        genai.configure(api_key=self.api_key)
        self.model_name = model

    def _convert_tools_to_gemini_format(self, tools: List[Dict]) -> Any:
        """
        Converts generic JSON schema tools to Gemini's FunctionDeclaration format.
        Note: This is a simplified mapper. Complex types might need recursion.
        """
        gemini_tools = []
        for tool in tools:
            # Gemini expects 'function_declarations'
            # For simplicity using the dict approach which the SDK supports
            gemini_tools.append({
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["parameters"]
            })
        return gemini_tools

    def generate(self, system_prompt: str, user_content: str, tools: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Calls Gemini API.
        """
        try:
            # Configure model
            # Gemini Pro doesn't support 'system_instruction' in all versions, 
            # but we can prepend it to history or use the beta version.
            # Using the chat interface is usually better for agentic flows.
            
            tool_config = None
            if tools:
                # tools argument in genai can be a list of functions
                tool_config = self._convert_tools_to_gemini_format(tools)

            model = genai.GenerativeModel(self.model_name, tools=tool_config)
            
            # Start a chat session to handle the System Prompt conceptually
            # (Or just send as message 1)
            messages = [
                {"role": "user", "parts": [f"System: {system_prompt}\n\nUser: {user_content}"]}
            ]

            response = model.generate_content(messages)
            
            # Parse Response
            result = {"content": None, "tool_calls": []}
            
            # Check for Function Calls
            if response.parts:
                for part in response.parts:
                    if fn := part.function_call:
                        result["tool_calls"].append({
                            "name": fn.name,
                            "arguments": dict(fn.args)
                        })
                    if text := part.text:
                        # Append text if present (CoT thought process often comes before tool call)
                        if result["content"] is None:
                            result["content"] = text
                        else:
                            result["content"] += text
            
            if not result["content"] and not result["tool_calls"]:
                # Fallback
                result["content"] = response.text

            return result

        except exceptions.ResourceExhausted:
            raise Exception("Rate limit exceeded")
        except Exception as e:
            raise Exception(f"Gemini API Error: {str(e)}")

class LLMClient:
    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def send_prompt(self, system_text: str, user_text: str, tools: Optional[List[Dict]] = None) -> Dict[str, Any]:
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Add logging for debug
                print(f"[LLMClient] Sending prompt to provider (Attempt {attempt+1})...")
                return self.provider.generate(system_prompt=system_text, user_content=user_text, tools=tools)
            except Exception as e:
                print(f"[LLMClient] Error on attempt {attempt+1}: {e}")
                if attempt < max_retries - 1:
                    sleep_time = 2 * (attempt + 1)
                    print(f"[LLMClient] Sleeping for {sleep_time}s...")
                    time.sleep(sleep_time)
        
        raise Exception("LLM Generation failed after max retries")

# Factory to get default provider
def get_llm_client() -> LLMClient:
    return LLMClient(provider=GeminiProvider())
