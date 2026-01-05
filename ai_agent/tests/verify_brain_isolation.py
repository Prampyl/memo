"""
Script to verify the 'Brain' components in isolation.
Run this to check if your API Keys and ChromaDB + Google Embeddings are working.

Usage:
    python ai_agent/tests/verify_brain_isolation.py
"""

import sys
import os
import time
from dotenv import load_dotenv

# Add root to path
sys.path.append(os.getcwd())
load_dotenv()

from ai_agent.api_client import get_llm_client
from ai_agent.rag.retriever import RAGRetriever, Document

def test_rag():
    print("\n🔬 TESTING REAL RAG (ChromaDB + Google Embeddings)...")
    try:
        retriever = RAGRetriever()
        
        # 1. Add Data
        docs = [
            Document(id="test_1", text="The secret code is 'BLUEBERRY'.", metadata={"patient_id": "test_user", "category": "secret"})
        ]
        print("   Adding document...")
        retriever.add_documents(docs)
        
        # 2. Retrieve
        print("   Retrieving...")
        results = retriever.retrieve("test_user", "What is the secret code?")
        
        if results and "BLUEBERRY" in results[0].text:
            print("   ✅ RAG SUCCESS: Retrieved the secret code.")
        else:
            print(f"   ❌ RAG FAILURE: Got {results}")
            
    except Exception as e:
        print(f"   ❌ RAG EXCEPTION: {e}")

def test_llm():
    print("\n🔬 TESTING REAL LLM (Gemini)...")
    try:
        client = get_llm_client()
        response = client.send_prompt(
            system_text="You are a test bot. Say 'HELLO WORLD' if you hear me.",
            user_text="Can you hear me?"
        )
        print(f"   Response: {response['content']}")
        
        if "HELLO WORLD" in str(response['content']).upper():
            print("   ✅ LLM SUCCESS: Received expected response.")
        else:
             print("   ⚠️ LLM WARNING: Response was unexpected but strictly speaking 'working'.")
             
    except Exception as e:
        print(f"   ❌ LLM EXCEPTION: {e}")

if __name__ == "__main__":
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ ERROR: GOOGLE_API_KEY is not set in environment.")
        sys.exit(1)
        
    test_rag()
    test_llm()
