# Technical Report: Memo - AI Assistant for Alzheimer’s Care

**Date:** January 16, 2026
**Project:** Memo
**Subject:** System Analysis & Technical Overview

---

## 1. Project Motivation & Problem Statement

### Why Alzheimer’s Care?

Alzheimer’s disease progressively destroys memory and cognitive function, leading to loss of independence and severe anxiety. The global burden falls heavily on family caregivers, who face high burnout rates (up to 60%).

### Key Challenges

1.  **Patient Anxiety & Confusion:** Patients often ask repetitive questions ("Where am I?", "When is dinner?") due to short-term memory loss.
2.  **Caregiver Fatigue:** Answering the same question 50 times a day is emotionally exhausting.
3.  **Loss of Identity:** As memory fades, patients lose their connection to their own history and self.

### Motivation

This project, **Memo**, aims to provide a tireless, empathetic, and personalized AI companion that can handle the repetitive "loop" of dementia care, offering reassurance and safety while preserving the patient’s dignity.

---

## 2. User Research & Caregiver Interviews

To ensure the system solves real problems, I conducted interviews with caregivers and professionals (specifically at a Memory Coffee event in Shanghai).

### Key Insights from Research (`Rapport_ITW.md`)

1.  **"Validation" over "Reality":** Correcting a patient (e.g., "Your husband died") often causes fresh grief. Effective care involves "Validation Therapy"—acknowledging the feeling behind the question rather than forcing the brutal truth.
2.  **Procedural Memory:** Patients often retain the ability to perform tasks (like grinding coffee) long after they lose semantic memory. The system should support "doing" rather than just "talking."
3.  **Sensory Anchoring:** Redirecting focus to sensory details (smell of lavender, touch of wood) is more effective than logical argumentation for reducing anxiety.

### Influence on Design

These insights shifted the project from a simple "FAQ Bot" to an **Empathic Agent** that prioritizes emotional safety over strict factual accuracy in certain contexts (e.g., diverting rather than confronting).

---

## 3. Exploration of AI Agents

### What is an AI Agent here?

In Memo, the "Agent" is not just a text generator. It is a system that can:

1.  **Perceive:** Read user input and retrieve relevant context (RAG).
2.  **Reason:** Analyze emotional state and intent (e.g., "Is the patient distressed?").
3.  **Act:** Execute tools (Search Memory, Schedule Reminder, Log Event) before speaking.

### Why not a simple Chatbot?

A standard chatbot (like basic ChatGPT) is stateless and generic. It does not know the patient's specific triggers (e.g., fear of thunderstorms) or history (e.g., "Son lives in London"). A rule-based system is too rigid to handle the infinite variability of natural language. An **Agentic Architecture** allows for dynamic decision-making based on a personalized knowledge base.

---

## 4. System Architecture Overview

The system follows a **3-Layer Architecture** (as defined in `system_design.md`):

### 1. The Interaction Layer (Frontend)

- **Patient UI:** Extremely simple, large text, voice-first.
- **Caregiver UI:** A dashboard to manage the patient's "profile" and memories.

### 2. The Orchestration Layer (The "Brain")

- **ActionHandler:** The core Python class that coordinates the workflow. It receives the user query, orchestrates tool usage, and synthesizes the final response.
- **Router:** Determines if a request is a simple chit-chat or requires complex handling.

### 3. The Knowledge Layer (Memory)

- **RAG (Retrieval-Augmented Generation):** A Vector Database (ChromaDB) stores unstructured biographical data ("Arthur loved the lake house").
- **Structured DB (PostgreSQL):** Stores rigid data like medication schedules and patient IDs.

**Data Flow:**
User Input → Router → ActionHandler → **RAG Retrieval** (Get Context) → **LLM Reasoning** (Decide Tool) → **Tool Execution** (e.g., Log Event) → **LLM Synthesis** (Generate Answer) → Output.

---

---

## 5. Prompt Engineering, Reasoning & Function Calling

The system's behavior is defined by **System Prompts** (e.g., `prompts/base_system_prompt.md`).

### Structure

The prompt injects variables dynamically:

> "You are Memo, a companion for {{ patient_name }}. Your diagnosis is {{ diagnosis_stage }}. NEVER give medical advice."

### 5.1 Reasoning Loop & Function Calling

A key differentiator of this agent is its ability to **act** using "Function Calling" (also known as Tool Use). The workflow is dynamic:

1.  **Intent Classification:** The agent analyzes: "What is the user effective asking?"
2.  **Tool Selection:** If the request requires data or action (e.g., "Remind me to call Mom"), the LLM does _not_ answer immediately. Instead, it outputs a structured **Tool Call**:
    ```json
    {
      "name": "schedule_reminder",
      "arguments": { "time": "2026-01-17T10:00:00", "message": "Call Mom" }
    }
    ```
3.  **Execution (The "ActionHandler"):** The system intercepts this JSON, executes the actual code (saving to PostgreSQL), and captures the result.
4.  **Observation Loop:** The system feeds the tool's output _back_ to the LLM: `Tool Output: "Reminder ID: 123 created successfully."`
5.  **Final Synthesis:** The LLM receives this confirmation and finally generates the user-facing response: _"I've set a reminder for you to call Mom tomorrow at 10 AM."_

### 5.2 Context Injection & Safety

1.  **Context Injection:** Relevant memories are retrieved via RAG and pasted into the prompt before the LLM generates a response.
2.  **Safety Check:** The prompt explicitly forbids hallucinating facts not found in the context.

### 5.3 Automated Clinical Reporting (Mood Tracking)

Beyond simple conversation, the Agent acts as a sentinel for the patient's well-being.

1.  **Sentiment Analysis:** With every input, the Agent evaluates the patient's emotional state (e.g., Calm, Anxious, Confused).
2.  **The `log_event` Tool:** If a significant emotional shift or recurring pattern is detected (e.g., repetitive questioning about a deceased relative), the Agent executes the `log_event` tool.
    - _Example Log:_ `{"event_type": "Agitation", "description": "Patient asked about husband 5 times in 10 minutes.", "severity": "Medium"}`
3.  **Medical Dashboard:** These logs are stored in the PostgreSQL database and visualized on the Caregiver Dashboard. This provides doctors with objective data to monitor disease progression or medication effectiveness (e.g., "Agitation increased after medication change").

### Limitations

Prompt-based control is fragile. If the LLM "hallucinates," it breaks trust. We mitigate this with strict "Grounding" instructions ("If you don't know, say 'Let's ask John'").

---

## 6. Implementation Details

### Tech Stack

- **Language:** Python 3.12 (Backend), Node.js (Frontend stubs).
- **Framework:** FastAPI (for the REST API).
- **AI Model:** Google Gemini 1.5/2.0 Flash (via `google-genai` SDK).
- **Vector Store:** ChromaDB (Local persistence).
- **Database:** PostgreSQL (Structured data).

### Key Modules

- `ai_agent/orchestrator/action_handler.py`: The main loop implementing the "Reasoning -> Tool -> Response" cycle.
- `ai_agent/rag/retriever.py`: Handles embedding generation and vector search.
- `backend/api/main.py`: The API surface connecting the Frontend to the Agent.

---

## 7. Usage & Feasibility

### Intended Usage

A tablet is placed in the patient's living room. The patient can speak naturally ("When is lunch?"). The system responds audibly. The caregiver updates the "Memory Bank" via a separate app (e.g., adding "Granddaughter visited today").

### Feasibility

- **Technical:** Highly feasible. Latency with Gemini Flash is low enough for voice conversation.
- **Practical:** Requires stable internet. Voice recognition for elderly speech patterns (stuttering, pauses) is a known challenge.

---

## 8. Ethical Considerations & Safety

### Risks

- **Hallucination:** The AI inventing false memories (e.g., "Your mom is visiting today" when she is deceased) is dangerous.
- **Attachment:** The patient might form an unhealthy dependency on the machine.

### Safeguards

- **No Medical Advice:** Hard-coded rule to never interpret symptoms.
- **Emergency Trigger:** The classifier detects distress keywords ("Help", "Pain") and alerts the caregiver immediately.
- **Human-in-the-Loop:** The caregiver ultimately controls the knowledge base.

---

## 9. Evaluation & Testing

- **Unit Tests:** Verified individual components (Database connection, API endpoints).
- **End-to-End Test (`e2e_demo.py`):** Simulated a full conversation loop where the agent successfully retrieved a specific memory ("Lake house keys") and scheduled a reminder, verifying the chain of "Intent -> RAG -> Tool -> Response".
- **Mock Verification:** Due to database complexity, we implemented a `MockToolClient` to isolate and verify the agent's reasoning logic independent of backend infrastructure.

---

## 10. Future Work & Next Steps

### Planned Evolution: Multi-Agent System

We are currently designing a **"Clinical Supervisor"** architecture (`docs/multi_agent_design.md`).

- **Supervisor Agent:** A silent "doctor" AI that monitors the conversation. It decides _strategy_ (e.g., "Use Validation Therapy") but does not speak.
- **Companion Agent:** The "voice" that speaks, strictly following the Supervisor's instructions.
  This splits "Safety/Strategy" from "Persona," reducing the risk of the AI breaking character or giving bad advice.

---

## Conclusion & Gap Analysis

**Missing/Underdeveloped Aspect:**
The current implementation is **Single-Agent**. While it uses RAG effectively, it struggles to balance complex clinical protocols (like Validation Therapy) with maintaining a conversational flow. The system sometimes defaults to "Reality Orientation" (telling the truth) even when "Validation" (comforting white lies) would be clinically superior.
