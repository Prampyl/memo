# AI Agent Module

**Owner:** AI Agent Engineer

## Purpose

This directory houses the "Brain" of Memo. It handles prompt engineering, RAG (Retrieval Augmented Generation), and LLM orchestration.

## Boundaries (Strict)

- **NO UI Logic:** You do not build interfaces here. You build APIs/Functions that return text/JSON.
- **NO Direct DB Access:** You rely on the `/backend` API or the specific Vector DB for retrieval.
- **Stateless:** Your agents should ideally be stateless, relying on Context passed in.

## Directory Structure

- `/prompts`: Raw text files or Jinja2 templates for prompts.
- `/rag`: Logic for embedding and retrieving semantic memory.
- `/tools`: Function calling definitions (e.g., "ScheduleReminder").
- `/evaluation`: Scripts to test "hallucinations" and "safety".

## Getting Started

1.  Add your keys to `.env` (but do not commit them!).
2.  Run `python evaluation/run_safety_check.py` to ensure baseline safety.
