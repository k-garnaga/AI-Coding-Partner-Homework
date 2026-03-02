# Test Report — API-404

## Changed Code Under Test
From `fix-summary.md`, the behavior change is in:
- `homework-4/demo-bug-fix/src/controllers/userController.js` (parse/validate `:id`, numeric lookup)
- `homework-4/demo-bug-fix/server.js` (do not listen during tests)

## Tests Added
File: `homework-4/demo-bug-fix/tests/users.api.test.js`

Test cases:
1. Existing numeric ID returns 200
   - Exercises the fixed numeric comparison.
2. Missing user returns 404
   - Ensures old behavior remains correct for valid IDs.
3. Invalid ID format returns 400
   - Exercises the new input validation.

## FIRST Self-Check (per `skills/unit-tests-FIRST.md`)
- **Fast**: Uses in-memory Express app via Supertest; no real port binding.
- **Independent**: Tests do not share state; no ordering assumptions.
- **Repeatable**: Deterministic static fixtures; no time/random.
- **Self-validating**: Explicit assertions on status codes and response bodies.
- **Timely**: Tests cover the bug fix and its edge cases only.

## How Tests Were Run
Command:
```bash
cd homework-4/demo-bug-fix
npm test
```

Result:
- Test suites: **1 passed**
- Tests: **3 passed**

## References
- `homework-4/demo-bug-fix/tests/users.api.test.js`
- `homework-4/demo-bug-fix/src/controllers/userController.js`
- `homework-4/demo-bug-fix/server.js`
- Skill: `homework-4/skills/unit-tests-FIRST.md`
