# System Design Memo

## 1. Problem Framing (What Memo Is)

**Memo** is an AI assistant that:

- Supports a **patient** (likely with memory or cognitive difficulties)
- Uses **personalized knowledge** (medical, routines, preferences)
- Is **continuously updated by caregivers**
- Can **reason conversationally** using that knowledge
- Can **remind, answer, reassure, and guide**

Key constraints:

- High personalization
- Strong data separation per patient
- Trustworthy answers (no hallucinations → RAG is critical)
- Simple caregiver interaction

---

## 2. High-Level System Architecture

At a high level, Memo has **three layers**:

```
┌──────────────────────────┐
│   User Interfaces        │
│                          │
│  Patient UI  Caregiver UI│
└─────────────┬────────────┘
              │
┌─────────────▼────────────┐
│   Memo AI Agent          │
│  (LLM + Orchestration)   │
└─────────────┬────────────┘
              │
┌─────────────▼────────────┐
│  Knowledge & Memory Layer│
│  (RAG + Databases)       │
└──────────────────────────┘
```

---

## 3. Core Components

### 3.1 Memo AI Agent (The Brain)

This is **not just a chatbot**.

**Responsibilities:**

- Understand patient intent
- Retrieve relevant patient-specific data
- Decide when to reassure, remind, or ask clarifying questions
- Respect patient cognitive limitations
- Format responses simply

**Internally, the agent has:**

- LLM (GPT / Claude / etc.)
- Prompt template with:

  - Patient profile summary
  - Communication rules (tone, repetition, simplicity)

- Tool access:

  - `retrieve_memory()`
  - `retrieve_schedule()`
  - `retrieve_medical_info()`
  - `log_interaction()`

> Think of the agent as a **controller**, not a database.

---

### 3.2 RAG Knowledge Base (Patient Memory)

This is the **core personalization engine**.

#### What goes into RAG?

Structured + unstructured data:

- Medical info (diagnosis, allergies, meds)
- Daily routines
- Family & caregivers
- Personal preferences
- Important life facts (“You live in Paris”, “Your daughter is Anna”)
- Caregiver notes

#### Architecture:

- **Vector database** (per patient or per tenant)
- Documents chunked by topic
- Metadata:

  - patient_id
  - category (medical, routine, family, reminder)
  - priority / sensitivity level
  - last_updated

Example document:

```json
{
  "text": "John takes Metformin 500mg every morning at 8am with breakfast.",
  "metadata": {
    "patient_id": "123",
    "type": "medication",
    "updated_by": "caregiver",
    "timestamp": "2025-01-01"
  }
}
```

---

### 3.3 Caregiver Interface (Control Panel)

This is **critical** and often underestimated.

**Caregiver abilities:**

- Add / edit patient information
- Add reminders
- Correct wrong assumptions
- See what Memo “knows”
- Control what the patient can or cannot see

**Key design principle:**
Caregivers **never touch prompts or embeddings directly**.

They interact with:

- Forms
- Categories
- Plain language fields

Example sections:

- Patient profile
- Medications
- Daily schedule
- Important facts
- One-time reminders
- Repeating reminders

Every update:
→ stored in DB
→ re-embedded into RAG
→ versioned

---

### 3.4 Patient Interface

Keep this **extremely simple**.

Possible modes:

- Chat (text or voice)
- Proactive reminders
- Reassurance mode (“Where am I?”, “What time is it?”)

**Key design rules:**

- Short responses
- Repetition allowed
- No contradictions
- Always grounded in RAG

---

## 4. Data Models (Conceptual)

### Patient

```
Patient
- patient_id
- name
- age
- condition
- communication_preferences
```

### Caregiver

```
Caregiver
- caregiver_id
- role
- permissions
```

### Memory Item (RAG source)

```
MemoryItem
- id
- patient_id
- content
- category
- sensitivity_level
- created_by
- updated_at
```

### Reminder

```
Reminder
- id
- patient_id
- content
- schedule
- recurring
- delivery_method
```

---

## 5. Example Workflows

### Workflow 1: Patient asks a question

> “Do I need to take my medicine now?”

1. Patient UI → Agent
2. Agent detects intent = medication
3. Agent queries RAG for:

   - medication
   - current time

4. Agent generates response:

   - Simple
   - Confident
   - Reassuring

5. Optional: logs interaction

---

### Workflow 2: Caregiver adds a reminder

> “Doctor appointment tomorrow at 10am”

1. Caregiver UI → Backend
2. Stored as structured reminder
3. Embedded into RAG
4. Scheduled notification created
5. Agent can now reference it conversationally

---

### Workflow 3: Patient confusion loop

> “Where am I?” (repeated 10 times)

Agent behavior:

- Always retrieve the same grounding fact
- Avoid escalating language
- Possibly switch to reassurance template

This is **agent logic**, not database logic.

---

## 6. Suggested Initial Tech Stack (Pragmatic)

You can evolve later, but for MVP:

**Backend**

- Python (FastAPI)
- PostgreSQL (structured data)
- Vector DB (Pinecone / Weaviate / FAISS)

**AI**

- LLM API
- Embeddings API
- Agent orchestration (LangChain / custom)

**Frontend**

- Caregiver: Web dashboard (React)
- Patient: Mobile or tablet UI (React Native)
