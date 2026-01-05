<!--
RATIONALE:
This prompt acts as the first-pass router. It categorizes user input into discrete buckets
(Chat, Action, Information) to downstream logic.
This prevents the "Chat" model from trying to execute database writes, and vice versa.
-->

# TASK: INTENT CLASSIFICATION

Analyze the user's input and classify it into exactly ONE of the following categories.

## CATEGORIES

1. **CASUAL_CHAT**: Small talk, greetings, emotional sharing. (e.g., "Hello", "I feel sad")
2. **INFORMATION_QUERY**: Asking for specific facts stored in memory. (e.g., "When is my daughter coming?", "What is my address?")
3. **ACTION_REQUEST**: Asking to perform a system action or change state. (e.g., "Remind me to take pills", "Call my son")
4. **EMERGENCY**: Expressions of pain, fall, danger, fear.

## INPUT

User Text: "{{ user_query }}"

## OUTPUT FORMAT

Return strictly JSON:

```json
{
  "category": "CATEGORY_NAME",
  "confidence": 0.0-1.0,
  "reasoning": "Brief explanation"
}
```
