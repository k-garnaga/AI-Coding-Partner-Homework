---
name: unit-tests-first
description: Guidelines for writing tests that follow FIRST principles (Fast, Independent, Repeatable, Self-validating, Timely). Use when adding tests for bug fixes.
license: MIT
---

## Purpose
Define the FIRST principles for unit tests and how to apply them in this repository.

## FIRST Principles

### F — Fast
- Tests should run quickly (ideally seconds).
- Avoid real network calls; use in-memory HTTP via Supertest for Express.

### I — Independent
- Each test can run alone and in any order.
- No shared mutable state across tests unless reset in `beforeEach`.

### R — Repeatable
- Same input ⇒ same output, regardless of machine/time.
- No reliance on real time, random values without seeding, or external services.

### S — Self-validating
- Assertions are explicit; tests fail with clear messages.
- No manual inspection of logs as a success criterion.

### T — Timely
- Tests are written for new/changed behavior as part of the same change.
- Focus on the bug fix and its edge cases (for example, invalid ID format).

## Repo-specific guidance
- Prefer testing the HTTP layer using `module.exports = app` from `homework-4/demo-bug-fix/server.js`.
- Validate both happy path and error handling (for example, 400/404).
- Keep fixtures minimal and inline.
