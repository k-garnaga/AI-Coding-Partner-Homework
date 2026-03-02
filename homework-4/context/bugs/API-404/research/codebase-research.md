# Codebase Research — API-404

## Repro
1. Start server (`homework-4/demo-bug-fix/server.js`).
2. Call: `GET /api/users/123`.

Expected: 200 with user `id: 123`.
Actual: 404 `{ "error": "User not found" }`.

## Route mapping
- The route `GET /api/users/:id` is defined in `homework-4/demo-bug-fix/src/routes/users.js` at lines 10–15.

## Controller logic
- `getUserById(req, res)` reads `req.params.id` into `userId` (string) in `homework-4/demo-bug-fix/src/controllers/userController.js` lines 18–23.
- The in-memory `users` list stores numeric IDs (e.g., `id: 123`) in the same file lines 6–11.
- It then searches via `users.find(u => u.id === userId)` in `userController.js` line 23.

## Root cause
`req.params.id` is a **string** (e.g., "123"), but `users[].id` are **numbers** (e.g., 123). Strict equality `===` compares both type and value, so it never matches and the controller returns 404.

## Proposed fix
- Parse `req.params.id` to a number and validate it.
- Compare numbers: `u.id === parsedId`.
- If the param is not a valid integer, return 400 with a clear error message.

## Expected side effects / edge cases
- `/api/users/abc` should return 400 (invalid id), not 404.
- `/api/users/999` should still return 404 (valid id format, but missing user).
