# Implementation Plan — API-404

## Inputs
- Verified research: `context/bugs/API-404/research/verified-research.md`
- App: `homework-4/demo-bug-fix/`

## Goal
Fix `GET /api/users/:id` incorrectly returning 404 for existing numeric IDs.

## Changes

### 1) Fix ID parsing and validation
**File**: `homework-4/demo-bug-fix/src/controllers/userController.js`

**Before** (`userController.js:18–27`):
- Reads `const userId = req.params.id;`
- Finds via `users.find(u => u.id === userId)`

**After**:
- Parse and validate the ID:
  - `const rawId = req.params.id;`
  - `const userId = Number.parseInt(rawId, 10);`
  - If `Number.isNaN(userId)` → `return res.status(400).json({ error: 'Invalid user id' });`
- Find via numeric compare: `users.find(u => u.id === userId)`

### 2) Add tests for the new behavior
**Folder**: `homework-4/demo-bug-fix/tests/`

**Add**: `homework-4/demo-bug-fix/tests/users.api.test.js`
- `GET /api/users/123` → 200 and `{ id: 123 }`
- `GET /api/users/999` → 404
- `GET /api/users/abc` → 400

### 3) Add test tooling
**File**: `homework-4/demo-bug-fix/package.json`
- Add `test` script
- Add dev dependencies: `jest`, `supertest`
- Configure Jest to run in Node environment

## Test Command
From repo root:
```bash
cd homework-4/demo-bug-fix
npm test
```

## Rollback Plan
- Revert `userController.js` change if it breaks routing.
- Keep tests isolated to `demo-bug-fix` folder.
