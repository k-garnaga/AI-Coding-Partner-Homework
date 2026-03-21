# Agents Configuration — Homework 6 Banking Pipeline

## 1. Assumed Tech Stack
- Language: Python 3.11+
- Runtime: standard library + FastMCP
- Testing: pytest and pytest-cov
- Data exchange: JSON files written through shared directories
- MCP: context7 plus a custom `pipeline-status` FastMCP server

## 2. Domain Rules
1. Money correctness comes first. Use `Decimal`, never `float`.
2. Currency validation is allowlist-based and limited to supported ISO 4217 codes.
3. Transactions with invalid amounts or currencies stop at validation.
4. High-risk transactions are held for manual review rather than auto-settled.
5. Audit logging is append-only and masks sensitive account identifiers.

## 3. Security Requirements
- Treat every input transaction as untrusted and validate before scoring or settlement.
- Do not log plaintext account numbers.
- Keep file writes scoped to the homework-6 workspace.
- Fail closed on validation errors and malformed amounts.

## 4. Agent Responsibilities
- `transaction_validator`: validates schema, amount, and currency; emits rejection reasons.
- `fraud_detector`: applies deterministic risk heuristics and attaches fraud metadata.
- `settlement_processor`: decides whether to settle or hold for review.
- `integrator`: manages directories, sequencing, auditing, and reporting.

## 5. Coding Guidelines
- Prefer small pure functions for validation, scoring, and status mapping.
- Keep message envelopes stable across agents.
- Use CLI entry points only where the homework requires operator-facing commands.
- Keep logs and summary reports machine-readable.

## 6. Testing Expectations
- Unit tests for each agent.
- Integration test for the full pipeline using isolated temporary directories.
- Tests for MCP query helpers.
- Coverage target of at least 90%, with a blocking push gate at 80%.

## 7. Stop Conditions
- Stop and clarify if the required shared-directory protocol changes.
- Stop and clarify if more currencies or region rules must be supported.
- Stop and clarify if settlement must include fees, exchange rates, or ledger persistence.
