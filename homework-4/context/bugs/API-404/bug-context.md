# Bug Context — API-404

Source bug context: `homework-4/demo-bug-fix/bugs/API-404/bug-context.md`

## Summary
The endpoint `GET /api/users/:id` returns **404 User not found** even for IDs that exist in the in-memory user list.

## Expected
- `GET /api/users/123` returns the user object `{ id: 123, ... }`.

## Actual
- `GET /api/users/123` returns 404.

## Notes
This homework uses the demo app under `homework-4/demo-bug-fix/`.
