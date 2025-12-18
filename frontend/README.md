# Frontend Module

**Owner:** Product Engineer

## Purpose

The "Face" of Memo. Delivers the user experience for both Patients and Caregivers.

## Structure

- `/patient`: The simplified, accessible interface for patients (Big buttons, high contrast).
- `/caregiver`: The complex dashboard for settings and history.
- `/components`: Shared UI library.

## Accessibility (A11y)

- **Patient App:** MUST meet WCAG AAA standards.
- **Caregiver App:** MUST meet WCAG AA standards.

## API Integration

- Use the generated client from `/shared` or `/backend` specs.
- NO direct DB calls.
