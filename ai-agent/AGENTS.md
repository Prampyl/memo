# AI-Agent Subsystem — Agents Instructions

## Project Context

This folder implements the **AI Agent** for Memo:

- Intent classification and routing
- RAG-augmented responses
- Structured tool usage (DB + Reminders + Logging)
- Safety audit and guardrails

The agent must align with Anthropic’s principles:

- Use simple prompt + retrieval first
- Only escalate to multi-step orchestration if required
- Log all planning and tool usage explicitly
- Tools must be documented clearly before use :contentReference[oaicite:1]{index=1}

## Responsibilities

1. **Intent Router**
2. **Prompt Templates**
3. **RAG Integration**
4. **Orchestrator / Planner**
5. **Tool Interfaces**
6. **Logging & Safety**
7. **Evaluation & Tests**

## Output Expectations

Whenever possible, code must:

- Use strong typing (TypeScript / Python types)
- Include tests stubbed under `/ai-agent/tests/`
- Include inline TODOs when assumptions are unknown
- Return logs in structured JSON

## File Creation Scaffold

The agent must generate files in this order:

1. Prompt templates in `ai-agent/prompts/`
2. Tool contracts in `ai-agent/tools/`
3. RAG interface in `ai-agent/rag/`
4. Router in `ai-agent/orchestrator/router.*`
5. Simple workflows in `ai-agent/orchestrator/simple_response.*`
6. Multi-step orchestrator
7. Evaluation tests in `ai-agent/tests/`

## Naming Conventions

- Use `camelCase` for functions
- Use `PascalCase` for types and classes
- Expose public interfaces through `index.*` barrels

## Coding Standards

- Don’t assume backend details — call documented tool APIs
- Write example API calls
- Tests must include happy and edge cases
- Guard against hallucination (return refusal or clarification if missing data)
