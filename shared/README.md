# Shared Library

**Owner:** Joint Ownership (Backend Lead + Frontend Lead)

## Purpose

This directory contains the **Contracts** and **Constants** shared between the Backend and Frontend.
IT MUST NOT CONTAIN BUSINESS LOGIC.

## Contents

- `/schemas`: JSON schemas or TypeScript interfaces for data models.
- `/constants`: System-wide constants (enums, config keys).

## Rules

1.  **No Secrets:** Never put API keys or secrets here.
2.  **No Node Dependencies:** This code should run in Browser and Node environments.
3.  **Strict Typing:** All Typescript must be strict.
