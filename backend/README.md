# Backend Module

**Owner:** Backend Data Engineer

## Purpose

The "Body" of the system. Manages data persistence, authentication, and the reminder scheduler.

## Boundaries

- **NO AI Logic:** Do not put prompt construction here.
- **NO Frontend Code:** This is a pure API (REST/GraphQL).

## Modules

- `/api`: API Controllers.
- `/models`: Database entities.
- `/reminders`: The critical reminder scheduling engine.
- `/services`: Domain logic.

## Getting Started

1.  Run migrations: `npm run db:migrate`
2.  Start server: `npm run start`
