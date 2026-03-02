# Security Report — API-404

## Summary
Reviewed the files changed for API-404 (ID parsing/validation, server startup guard, tests, and dev dependencies). No high-risk vulnerabilities introduced.

## Findings

### 1) Input validation added (good) — INFO
- Location: `homework-4/demo-bug-fix/src/controllers/userController.js`
- Notes: Converting `req.params.id` to an integer and returning 400 on invalid IDs reduces ambiguity and prevents confusing 404 responses.
- Recommendation: Keep the 400 response; consider additionally enforcing a positive integer constraint if IDs should be positive.

### 2) Potential information disclosure through error messages — LOW
- Location: `homework-4/demo-bug-fix/src/controllers/userController.js`
- Details: Error strings are generic and do not disclose sensitive info. This is acceptable.
- Recommendation: If this were a real system, prefer consistent error shapes and consider localization.

### 3) Dependency hygiene — INFO
- Location: `homework-4/demo-bug-fix/package.json`
- Details: Added `jest` and `supertest` as dev dependencies. `npm audit` during install reported **0 vulnerabilities**.
- Recommendation: Periodically run `npm audit` and keep dev deps updated.

### 4) Server startup guard reduces test flakiness — INFO
- Location: `homework-4/demo-bug-fix/server.js`
- Details: `require.main === module` ensures the process doesn’t keep a listening socket open when imported by tests.

## Notes / Assumptions
- This demo app has no authentication/authorization.
- No database, templates, or secrets handling are present.

## References
- `homework-4/context/bugs/API-404/fix-summary.md`
- `homework-4/demo-bug-fix/src/controllers/userController.js`
- `homework-4/demo-bug-fix/server.js`
- `homework-4/demo-bug-fix/package.json`
