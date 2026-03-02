# Fix Summary — API-404

## Changes Made

### 1) Parse and validate user id + numeric lookup
- File: `homework-4/demo-bug-fix/src/controllers/userController.js`
- Location (pre-fix): around `getUserById` (`userController.js:18–30`)

**Before**
- `const userId = req.params.id;`
- `users.find(u => u.id === userId)` (always fails because userId is a string)

**After**
- Parse: `Number.parseInt(req.params.id, 10)`
- If `NaN` → `400 { error: 'Invalid user id' }`
- Compare numerically: `users.find(u => u.id === userId)`

Test result after change:
- `npm test` ✅

### 2) Make server test-friendly (avoid open handles)
- File: `homework-4/demo-bug-fix/server.js`
- Location: server startup block (`server.js:23–31`)

**Before**
- Always called `app.listen(...)` on import, causing Jest to hang.

**After**
- Only listen when executed directly: `if (require.main === module) { app.listen(...) }`
- Export `app` for Supertest.

Test result after change:
- `npm test` ✅

### 3) Add automated tests for the fix
- File: `homework-4/demo-bug-fix/tests/users.api.test.js`

New tests:
- `GET /api/users/123` → 200 with `{ id: 123 }`
- `GET /api/users/999` → 404
- `GET /api/users/abc` → 400

Test result after change:
- `npm test` ✅

### 4) Add test tooling
- File: `homework-4/demo-bug-fix/package.json`

Changes:
- Add script: `"test": "jest"`
- Add dev deps: `jest`, `supertest`

Test result after change:
- `npm test` ✅

## Overall Status
- Bug **API-404**: **FIXED**
- Tests: **PASSING**

## Manual Verification
From repo root:
```bash
cd homework-4/demo-bug-fix
npm install
npm start
```
Then:
```bash
curl -i http://localhost:3000/api/users/123
curl -i http://localhost:3000/api/users/abc
```

Expected:
- `/123` → 200 JSON user
- `/abc` → 400 `{ "error": "Invalid user id" }`

## References
- `homework-4/demo-bug-fix/src/controllers/userController.js`
- `homework-4/demo-bug-fix/server.js`
- `homework-4/demo-bug-fix/tests/users.api.test.js`
- `homework-4/demo-bug-fix/package.json`
