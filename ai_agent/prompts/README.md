# Prompt Templates — Usage & Expectations

This folder contains all prompts used to guide the agent’s decision-making and tool interactions.

## 1) Base System Prompt (`base_system_prompt.md`)

Defines general agent behavior, safety rules, guardrails, and constraints.

Expectations:

- Must include explicit planning steps
- Must instruct the agent to output structured JSON for any tool call
- Must require clarifying questions when ambiguous

Output Schema:
{
"plan": [...],
"toolCalls": [...],
"finalAnswer": "..."
}

## 2) Intent Classifier (`intent_classifier_prompt.md`)

Routes user inputs into workflows:

- `simple_answer`
- `reminder_operation`
- `memory_update`
- `clarification_needed`

Output Schema:
{"intent":"simple_answer","confidence":0.82}

## 3) Simple Response Template (`simple_response_template.md`)

Used when a direct answer grounded in RAG is sufficient.

Expectations:

- Include RAG context blocks
- Return short answers with grounding
- If missing data, escalate to clarifying question

Output Schema:
Same as Base System Prompt.

## 4) Tool Call Template (`tool_call_template.json`)

Defines JSON typing for invoking documented tools (DB, reminder API, logs).

Example:

{
"tool":"reminderApi",
"function":"createReminder",
"args":{...}
}

Ensure all tools conform to this schema before use.
