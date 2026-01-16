# Memo – Task Breakdown

## Team Roles (Suggested)

1. **AI / Agent Engineer**
   Owns the assistant logic, RAG, prompting, and reasoning behavior.
2. **Backend / Data Engineer**
   Owns APIs, databases, reminders, authentication, and integrations.
3. **Frontend / Product Engineer**
   Owns caregiver UI, patient UI, UX flows, and usability constraints.

---

# 1. AI / Agent Engineer Tasks

### 1.1 Define Memo’s Agent Identity & Behavior

**Goal:** Create a reliable, safe, patient-aware assistant.

**Tasks**

- Define agent role & tone (reassuring, simple, repetitive-safe)
- Write system prompt template with:

  - Patient summary slot
  - Cognitive adaptation rules
  - Safety constraints (no guessing)

- Define response length & structure rules
- Create fallback responses when info is missing

**Deliverables**

- Versioned system prompt
- Behavior rules documentation

---

### 1.2 RAG Design & Retrieval Logic

**Goal:** Ground all responses in patient data.

**Tasks**

- Define memory categories:

  - Medical
  - Routine
  - Personal facts
  - Caregiver notes
  - Reminders

- Define chunking strategy
- Define metadata schema
- Implement retrieval filtering by:

  - patient_id
  - category
  - recency / priority

**Deliverables**

- RAG schema definition
- Retrieval function spec

---

### 1.3 Agent Tooling & Orchestration

**Goal:** Make the agent _act_, not just chat.

**Tasks**

- Define agent tools:

  - retrieve_memory
  - retrieve_reminders
  - get_current_time
  - log_interaction

- Decide agent flow:

  - classify intent
  - retrieve context
  - generate response

- Handle repetition loops (same question many times)

**Deliverables**

- Agent flow diagram
- Tool calling logic

---

### 1.4 Evaluation & Guardrails

**Goal:** Avoid hallucinations and unsafe outputs.

**Tasks**

- Create test prompts (confusion, stress, repetition)
- Define hallucination detection rules
- Add “I don’t know but I can help” patterns
- Create golden responses for key scenarios

**Deliverables**

- Test prompt set
- Evaluation checklist

---

# 2. Backend / Data Engineer Tasks

### 2.1 Core Backend Architecture

**Goal:** Reliable data & API layer.

**Tasks**

- Setup FastAPI backend
- Design REST / GraphQL APIs
- Define patient & caregiver auth model
- Implement role-based access control

**Deliverables**

- API spec
- Auth & permissions logic

---

### 2.2 Database Design (Structured Data)

**Goal:** Clean separation between structured data & RAG.

**Tasks**

- Design PostgreSQL schemas for:

  - Patients
  - Caregivers
  - Roles
  - Reminders
  - Interaction logs

- Version memory updates
- Audit trail for caregiver edits

**Deliverables**

- ER diagram
- Migration scripts

---

### 2.3 Reminder Engine

**Goal:** Time-based + conversational reminders.

**Tasks**

- Define reminder types:

  - One-time
  - Recurring
  - Conditional

- Implement scheduler (cron / background jobs)
- Trigger notifications
- Sync reminders with RAG embeddings

**Deliverables**

- Reminder logic spec
- Scheduler implementation

---

### 2.4 RAG Infrastructure

**Goal:** Scalable patient memory storage.

**Tasks**

- Choose vector DB
- Implement embedding pipeline
- Create upsert / delete logic
- Handle re-embedding on updates

**Deliverables**

- Vector DB setup
- Memory ingestion pipeline

---

### 2.5 Logging, Monitoring & Compliance

**Goal:** Traceability & safety.

**Tasks**

- Log all interactions
- Tag conversations with intent
- Implement data retention rules
- Prepare for GDPR / HIPAA alignment (conceptual)

**Deliverables**

- Logging schema
- Compliance checklist

---

# 3. Frontend / Product Engineer Tasks

### 3.1 Caregiver Dashboard

**Goal:** Absolute clarity & control.

**Tasks**

- Patient overview page
- Memory editor (categorized forms)
- Reminder creation UI
- Edit / delete memory items
- “What Memo knows” view

**Deliverables**

- Caregiver UI wireframes
- Dashboard implementation

---

### 3.2 Patient Interface

**Goal:** Extreme simplicity.

**Tasks**

- Chat UI (text / voice ready)
- Large fonts, minimal buttons
- One-action help (“I’m confused”)
- Reminder notifications UI

**Deliverables**

- Patient UI flow
- Accessibility checklist

---

### 3.3 UX Safety & Cognitive Design

**Goal:** Reduce stress, avoid overload.

**Tasks**

- Define max response length
- Enforce single-topic responses
- Design repetition-safe UI
- Emergency escalation UX

**Deliverables**

- UX principles doc
- Edge-case flows

---

### 3.4 Integration with Backend & Agent

**Goal:** Seamless data flow.

**Tasks**

- Connect APIs
- Real-time updates (WebSocket / polling)
- Error handling (graceful degradation)
- Offline-safe behavior (optional)

**Deliverables**

- Integration layer
- Error UX patterns

---

# Cross-Team Sync Points (Very Important)

### Weekly Alignment

- Agent logic ↔ reminder system
- Caregiver edits ↔ RAG updates
- UI expectations ↔ backend constraints

### Shared Artifacts

- Memory taxonomy
- Intent definitions
- Error codes & fallback behaviors

---

# MVP Definition (What “Done” Means)

**Patient can:**

- Ask about daily life
- Get correct reminders
- Be reassured consistently

**Caregiver can:**

- Update patient knowledge
- Add reminders
- Trust Memo’s answers

**System can:**

- Avoid hallucinations
- Explain decisions via logs
- Scale to multiple patients
