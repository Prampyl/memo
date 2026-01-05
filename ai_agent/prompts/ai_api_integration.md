# AI API Integration Prompt Guide

## Purpose

Define how the agent should call the chosen LLM API (e.g., OpenAI, Anthropic).  
This document instructs the agent _how to send prompts to the model_ during runtime.

## Requirements

- Connect to HTTP LLM endpoint securely
- Pass RAG context + system prompt + user query
- Support streaming responses (optional)
- Respect rate limits

## Preferred Provider Options

We support both:

1. **OpenAI** via the Assistants API (structured JSON with function calls)
2. **Anthropic** via Claude API

The prompt pipeline must follow:

1. Build final prompt by combining:
   - base_system_prompt
   - intent_classification context
   - RAG results
2. Pass to LLM API
3. Receive response
4. If output contains tool calls:
   - Validate schema
   - Dispatch to the tool client
   - Log and loop back

## Example Schema

```json
{
  "model": "openai/gpt-4.1-mini",
  "messages":[
    {"role":"system","content":"..."},
    {"role":"user","content":"..."}
  ],
  "functions":[
    { "name":"createReminder", "parameters": {...}}
  ]
}

Success Criteria

Agent must validate LLM output format before using it.

If ambiguous, the agent should ask for clarification.
```
