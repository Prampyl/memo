# Backend API for AI Agent

This API exposes backend tools to the AI Agent via FastAPI.

## Required Endpoints

### Memory

GET /memory?patientId=...
POST /memory

### Reminders

GET /reminders?patientId=...
POST /reminders

### Logs

POST /logs

## Must Use

- Pydantic schemas
- JWT or API key auth

## Example FastAPI route

```python
@router.post("/reminders")
async def create_reminder(body: ReminderCreate):
    return await reminder_service.create(body)

Successful agent design requires this API before meaningful integration tests can run.
```
