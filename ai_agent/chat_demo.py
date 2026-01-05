
import sys
import os
from dotenv import load_dotenv

# Add root to path
sys.path.append(os.getcwd())
load_dotenv()

from ai_agent.orchestrator.action_handler import ActionHandler
# We can import MockToolClient if we want to default to mock, 
# but effectively the ActionHandler defaults to real tools unless overridden.
# Given the user wants "Real Use", let's try Real Tools, but fallback gracefully?
# For now, let's use the DB if it works. If not, the user can switch to Mock.

def chat_loop():
    print("\n💬 Memo AI Agent - Interactive Chat")
    print("--------------------------------------------------")
    print("Type 'exit' or 'quit' to stop.")
    print("Type 'clear' to clear history.")
    print("--------------------------------------------------")

    try:
        # Initialize Agent
        # Note: If database is broken, this might fail on tool execution purely, 
        # but initialization is safe.
        agent = ActionHandler()
        print("✅ Agent Initialized (Connected to Real Backend)")
    except Exception as e:
        print(f"❌ Initialization Failed: {e}")
        return

    patient_id = "7a5c5780-8e97-4e90-be2f-11c2545a4640" # Use a valid ID from our seed/test
    if not patient_id: 
        patient_id = "demo-user"

    history_buffer = [] # List of (User, Agent) tuples
    MAX_HISTORY = 3

    while True:
        try:
            user_input = input("\n👤 You: ").strip()
        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            break

        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break
        
        if user_input.lower() == "clear":
            history_buffer.clear()
            print("🧹 History cleared.")
            continue

        if not user_input:
            continue

        # Construct Prompt with History (Simple concatenation hack for context)
        # In a production app, we'd pass structured messages to the LLM.
        context_str = ""
        if history_buffer:
            context_str = "PREVIOUS CONVERSATION:\n"
            for u, a in history_buffer:
                context_str += f"User: {u}\nAgent: {a}\n"
            context_str += "\nCURRENT REQUEST:\n"
        
        full_prompt = context_str + user_input

        print("⏳ Agent: (Thinking...)")
        try:
            # We pass the full prompt to handle, so RAG sees it too (which is okay)
            response = agent.handle(patient_id, full_prompt)
            print(f"🤖 Memo: {response}")

            # Update History
            history_buffer.append((user_input, response))
            if len(history_buffer) > MAX_HISTORY:
                history_buffer.pop(0)

        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    chat_loop()
