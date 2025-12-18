# Memory Taxonomy: Structured vs. Semantic

## Overview

Cognitive impairment assistance requires two types of memory. We must strictly distinguish them to avoid hallucinations and ensure medical accuracy.

## 1. Structured Data (The "Hard" Facts)

**Location:** SQL / Relational DB
**Owner:** Backend Team
**Nature:** Rigid, verifiable, critical.

- **Examples:**
  - Medication Schedule (Time, Dosage)
  - Caregiver Contact Info
  - Emergency Protocols
  - User Profile (Name, Age, Diagnosis)

**Usage:** Passed to the AI as _Context_ in the prompt. The AI cannot "guess" this; it must be provided.

## 2. Semantic Memory (The "Soft" Context)

**Location:** Vector Database (RAG)
**Owner:** AI Agent Team
**Nature:** Fuzzy, narrative, associative.

- **Examples:**
  - "The patient was anxious yesterday evening."
  - "They prefer to be called 'Captain' in the mornings."
  - "They didn't like the red pill."

**Usage:** Retrieved via similarity search to color the interaction or provide empathy.

## Write Path Rules

1.  **Caregiver Updates:** Go to Structured Data (Backend).
2.  **Daily Interactions:** Go to Semantic Memory (AI Agent logs).
3.  **Conflict Resolution:** Structured Data ALWAYS overrides Semantic Memory.

## TODOs

- [ ] Define PII scrubbing pipeline for Semantic Memory.
- [ ] Create tools for the Agent to "flag" a semantic memory that should be structural (e.g., "Patient has a new pain").
