# Tool Specifications for AI Agent

## Database API

GET /memory?patient_id=...
Returns:

- `facts`: array of {id, text, category, updated_at}

## Reminder API

POST /reminders
Body:
{
"patientId": "...",
"message": "...",
"schedule": "ISO8601"
}

Returns:
{
"id": "...",
"status": "scheduled"
}

## Logging API

POST /logs
Body:
{
"requestId": "...",
"agentPlan": [...],
"toolCalls": [...],
"response": "..."
}

# Success Criteria

- All tools must validate input
- Agents must never call tools directly without following schema
- Tests for each tool must be created in `/tests/`
