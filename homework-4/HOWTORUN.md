# Homework 4 — How to Run

## Prereqs
- Node.js 18+ recommended
- npm

## Run the demo API
```bash
cd homework-4/demo-bug-fix
npm install
npm start
```

In another terminal:
```bash
curl -i http://localhost:3000/health
curl -i http://localhost:3000/api/users
curl -i http://localhost:3000/api/users/123
```

## Run tests
After tests are added by the unit-test-generator step:
```bash
cd homework-4/demo-bug-fix
npm test
```

## Run the pipeline (documented)
The pipeline is represented by agent specs under `.github/agents/*.agent.md`.
Artifacts live under `homework-4/context/bugs/API-404/`.

Skills used by agents live under `.github/skills/<skill-name>/SKILL.md`.

Run order (per `TASKS.md`):
1. Bug Researcher (human/AI) → produces `research/codebase-research.md`
2. Bug Research Verifier → produces `research/verified-research.md`
3. Bug Planner (human/AI) → produces `implementation-plan.md`
4. Bug Implementer → produces `fix-summary.md` + applies code changes
5. Security Verifier → produces `security-report.md`
6. Unit Test Generator → produces `test-report.md` + adds tests
