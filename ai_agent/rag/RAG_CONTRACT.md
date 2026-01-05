# RAG Contract — Grounded Retrieval Interface

## Input

- `patientId`
- `query`
- optional `filter` array

## Output

- `documents`: array of {id, text, metadata}

Metadata keys:

- category
- created_by
- timestamp

Agent must _always retrieve before answering factual queries_. If no documents returned & answer required, agent should ask clarification.

## Success

- Evidence of relevant docs
- Minimal irrelevant documents
- Tests included under `/ai-agent/tests/rag_tests.*`
