## Memo Functional Specification

### 1. Vision
Memo is a proactive AI assistant designed to support individuals living with cognitive impairments (e.g. Alzheimer’s). It combines voice interaction, contextual intelligence (IoT sensors), and caregiver/clinician tools. Goal: ensure safety, medication adherence, hydration, emotional support, and reduce caregiver burden.

### 2. Personas & Stakeholders
1. Primary User (Patient) – interacts via voice, needs reminders, reassurance, simple choices.
2. Family Caregiver – monitors activity, updates “life repertoire” (preferences, family info), receives alerts.
3. Clinician – reviews aggregated data (adherence, engagement), downloads reports, manages care plans.
4. Administrator – configures hardware sensors, manages patient accounts.

### 3. Core Functional Areas
1. Voice Assistant (Patient Device)
   - Wake-on-presence (sensor triggered) + manual activation.
   - Proactive reminders (medication, hydration, appointments, activities).
   - Conversational responses with empathic tone.
   - Cognitive stimulation games (memory, music, storytelling).
   - Family personalization (mentions relatives, favourite memories).
   - Speech-to-text input (optional), text-to-speech output.

2. Context Awareness & IoT Integration
   - Presence sensors (e.g. PIR) detect entry in key rooms (kitchen, bedroom).
   - Data ingestion from sensors every 2s (configurable).
   - Rules engine linking context → reminder (e.g. kitchen + morning → vitamins).
   - Device health monitoring (sensor connectivity, low battery alerts).

3. Patient Data Layer
   - Profile (name, preferred name, languages, routines).
   - Family tree + contacts (spouse, children, caregivers, emergency contacts).
   - Medical plans (medications, schedules, dosage notes).
   - Preferences (voice tone, pace, favourite games, sensitive topics).
   - History (interactions, confirmations, declined reminders).

4. Caregiver Portal
   - Dashboard: current status, latest reminders, adherence metrics.
   - Timeline: chronological log of interactions (time, context, patient response).
   - Alerts: missed medication, prolonged presence, low engagement.
   - Life Repertoire editor: update stories, preferences, family info.
   - Communication: send gentle messages or schedule in-person check-ins.

5. Clinician Console
   - Analytics: adherence %, hydration frequency, interaction count, mood indicators.
   - Report export (PDF/CSV) per patient or cohort.
   - Care plan management: set goals, update routines, assign tasks to caregivers.
   - Clinical notes: add observations, track interventions.

6. Administration
   - User management (patients, caregivers, clinicians).
   - Device provisioning: assign physical device + sensors to patient.
   - Security roles and permissions.
   - Audit logs.

### 4. Functional Requirements
1. Voice Assistant:
   - FR-VA-01: System shall provide a configurable wake phrase and sensor trigger.
   - FR-VA-02: System shall support TTS with selectable voices and speech rate.
   - FR-VA-03: System shall understand basic STT commands (Yes/No, simple sentences).
   - FR-VA-04: System shall run pre-scripted demos for testing.

2. Proactive Reminders:
   - FR-PR-01: Reminders tied to schedules and context.
   - FR-PR-02: Confirmation capture (taken, skipped, remind later).
   - FR-PR-03: Escalation logic (notify caregiver if repeated misses).

3. Games & Cognitive Stim:
   - FR-GAME-01: Support multiple game types (memory cards, music, storytelling).
   - FR-GAME-02: Track participation and feedback.

4. Patient Database:
   - FR-DB-01: Store structured patient info (profile, family, routines, meds).
   - FR-DB-02: Provide API to read/write patient data with validation.
   - FR-DB-03: Version changes for auditing.

5. Caregiver Portal:
   - FR-CP-01: Authentication with caregiver role.
   - FR-CP-02: Real-time dashboard with sensor + assistant status.
   - FR-CP-03: Editor for life repertoire (stories, preferences).
   - FR-CP-04: Alert management (acknowledge, escalate).

6. Clinician Portal:
   - FR-CL-01: Role-based access with patient assignments.
   - FR-CL-02: Aggregate metrics per patient.
   - FR-CL-03: Exportable monthly report.

7. Admin:
   - FR-AD-01: Create/manage user accounts & roles.
   - FR-AD-02: Assign devices and sensors.
   - FR-AD-03: System health dashboards.

### 5. Non-Functional Requirements
1. Reliability: 99% uptime target, offline fallback for local reminders.
2. Security: HIPAA / GDPR compliance, encrypted data at rest/in transit, RBAC.
3. Privacy: Consent management for family data, anonymized analytics.
4. Performance: Voice response < 1.5s after prompt; sensor polling customizable.
5. Accessibility: Large text options, high-contrast UI, multilingual support.

### 6. Technical Architecture (High-Level)
1. Frontend (web + embedded device UI).
2. Backend API (Node.js/Express) + LLM proxy.
3. Sensor ingestion service (polling or MQTT).
4. Database (PostgreSQL or MongoDB) for patient data + logs.
5. File storage for audio snippets / reports.
6. Integration with LLM provider (Gemini or equivalent) via secure backend call.

### 7. Data Model Overview
**Patient**
```
{
  id,
  profile: { name, preferredName, dob, languages },
  family: { spouse, children[], caregiver, emergencyContacts[] },
  medical: { medications[], allergies, doctor },
  routines: { morning, afternoon, evening },
  preferences: { tone, pace, sensitiveTopics[] },
  history: [{ timestamp, type, detail }]
}
```

**Interaction Log**
```
{
  id,
  patientId,
  timestamp,
  channel (voice / portal / sensor),
  context (location, trigger),
  message,
  response,
  outcome (confirmed, skipped, escalated)
}
```

### 8. User Journeys (Example)
1. Patient enters kitchen (sensor triggers) → Memo greets → reminder to take vitamins → patient confirms → caregiver sees log → clinician sees adherence update.
2. Caregiver logs in → notices missed hydration alert → sends personalized message → Memo delivers message vocally.
3. Clinician exports monthly report → reviews engagement trends → adjusts care plan.

### 9. Future Extensions
1. Multi-language support (FR/EN).
2. Predictive analytics (detect anomalies, mood changes).
3. Wearable integration (heart rate, sleep).
4. In-home display with photo sharing.
5. Remote firmware updates for IoT devices.

### 10. Success Metrics
1. Patient adherence increase (medication/hydration).
2. Reduction in caregiver alerts/escalations.
3. Positive mood indicators / engagement rate.
4. Clinician report usage.
5. System reliability & response time.

---
This specification serves as the foundation for a production-ready Memo platform, encompassing patient-facing assistant, caregiver and clinician tooling, data layer, and operational requirements.

