# Reminder System Architecture

## Criticality

Reminders are the lifeblood of Memo. Failure to deliver a medication reminder is a sentinel event.

## Components

1.  **Scheduler (Backend):** A reliable job queue (e.g., BullMQ, AWS SQS) that triggers events at specific times.
2.  **Notifier (Backend):** Omnichannel delivery (Push, SMS, Speaker).
3.  **Verifier (AI Agent):** Confirming the patient _understood_ and _acted_.

## The Reminder Loop

1.  **Trigger:** Time T arrives for "Take Medication A".
2.  **Notify:** Backend plays audio/sends notification.
3.  **Interact:**
    - System waits for confirmation.
    - IF no confirmation in 5 mins: Escalation Level 1 (Louder prompt).
    - IF no confirmation in 15 mins: Escalation Level 2 (Call Caregiver).
4.  **AI Role:**
    - The AI handles the _conversation_ during the notification.
    - "It's time for your blue pill, John. It helps with the blood pressure." (Contextualized by Agent).

## Data Model (Stub)

```json
{
  "reminder_id": "uuid",
  "patient_id": "uuid",
  "time_utc": "ISO8601",
  "type": "MEDICATION",
  "payload": {
    "med_name": "Lisinopril",
    "dosage": "10mg"
  },
  "escalation_policy": "STANDARD"
}
```
