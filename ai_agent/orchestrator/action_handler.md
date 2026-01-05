# Action Workflow Handler

## Purpose

Implement orchestrator logic for _structured actions_ (e.g., reminders, updates).

## Responsibilities

- Accept intent from router
- Build structured plan
- Execute LLM planning prompts
- Call tools in order:
  - API: createReminder/getReminders
  - API: updateMemory/addMemory
- Validate responses
- Return final user response

## Example Flow

1. User: “Remind me daily at 8 AM to take pills.”
2. Router -> `action_reminder`
3. Orchestrator:
   a. Generate plan (LLM)
   b. Validate plan
   c. Call reminder API
   d. Confirm to user

## Edge Cases

- Partial time info
- Conflicting existing reminders
