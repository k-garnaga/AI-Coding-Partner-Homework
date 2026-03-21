# Specification: Multi-Agent Banking Pipeline

## 1. High-Level Objective
Build a Python multi-agent banking pipeline that validates transactions, scores them for fraud risk, and settles or holds them using file-based JSON message passing.

## 2. Mid-Level Objectives
- Transactions with unsupported ISO 4217 currency codes are rejected with an `INVALID_CURRENCY` reason.
- Transactions with non-positive amounts are rejected and never reach fraud or settlement processing.
- Transactions above `$50,000.00` or occurring during unusual hours are assigned a fraud risk score and level.
- Every processed transaction produces a final JSON result in `shared/results/` plus an audit log entry with an ISO 8601 timestamp.
- The pipeline produces a summary report and achieves at least 90% automated test coverage, with a push-blocking gate at 80%.

## 3. Implementation Notes
- Monetary calculations use `decimal.Decimal` only. No transaction amount is processed as a float.
- Currency validation uses an ISO 4217 allowlist for `USD`, `EUR`, `GBP`, and `JPY`.
- Logging writes an audit trail with timestamp, agent name, transaction ID, and outcome.
- Account identifiers are treated as sensitive and are masked in audit logs.
- Agent communication uses JSON files passed through `shared/input/`, `shared/processing/`, `shared/output/`, and `shared/results/`.
- High-risk transactions are held for manual review instead of being settled automatically.

## 4. Context
- **Beginning state**: `sample-transactions.json` exists with raw banking transactions. No agents, no pipeline code, and no shared runtime directories exist.
- **Ending state**: Each transaction is processed by the validator, fraud detector, and settlement processor. Final results land in `shared/results/`, a pipeline summary report is generated, and coverage is at least 90% locally with an 80% push gate.

## 5. Low-Level Tasks

### Task: Transaction Validator
**Prompt**: "Context: We are building a Python banking pipeline that exchanges JSON messages through shared directories. Task: Create `agents/transaction_validator.py` with `process_message(message: dict) -> dict` and a dry-run CLI. Rules: use Decimal for amounts, reject missing required fields, reject non-positive amounts, reject unsupported ISO 4217 currencies, and return reasons in a validation block. Output: a transformed message targeted to the fraud detector when valid or to results when rejected."
**File to CREATE**: `agents/transaction_validator.py`
**Function to CREATE**: `process_message(message: dict) -> dict`
**Details**:
- Check required fields and produce machine-readable rejection codes
- Normalize valid amounts to two decimal places
- Support `--dry-run` validation output for the custom slash command

### Task: Fraud Detector
**Prompt**: "Context: Validated banking transactions are forwarded as JSON messages. Task: Create `agents/fraud_detector.py` with `process_message(message: dict) -> dict`. Rules: score risk using amount, unusual processing hour, and cross-border heuristics; assign LOW, MEDIUM, or HIGH; preserve message structure; and forward to the settlement processor. Output: a message containing `fraud_review.risk_score`, `fraud_review.risk_level`, and `fraud_review.triggers`."
**File to CREATE**: `agents/fraud_detector.py`
**Function to CREATE**: `process_message(message: dict) -> dict`
**Details**:
- Add `+3` for amount above `10000`, `+4` for amount above `50000`
- Add `+2` for transactions between `02:00` and `05:59` UTC
- Add `+2` for cross-border currency-country mismatches

### Task: Settlement Processor
**Prompt**: "Context: Fraud-screened banking transactions need a final disposition. Task: Create `agents/settlement_processor.py` with `process_message(message: dict) -> dict`. Rules: hold HIGH-risk transactions for manual review, settle all other validated transactions, include a settlement batch ID, and write a final decision compatible with result storage. Output: a final message targeted to results with settlement details."
**File to CREATE**: `agents/settlement_processor.py`
**Function to CREATE**: `process_message(message: dict) -> dict`
**Details**:
- Produce `settlement.decision`, `settlement.review_required`, and `settlement_amount`
- Preserve rejected transactions without attempting settlement
- Mark final status as `settled`, `pending_manual_review`, or `rejected`

### Task: Integrator / Orchestrator
**Prompt**: "Context: The agents communicate through JSON files in shared directories. Task: Create `integrator.py` plus orchestration helpers that load `sample-transactions.json`, reset shared directories, route messages through each agent, archive final results, and write a summary report. Rules: every stage must leave JSON artifacts in the file-passing directories, all audit entries need masked account numbers, and all sample transactions must produce result files. Output: a CLI entry point that runs the pipeline end to end."
**File to CREATE**: `integrator.py`
**Function to CREATE**: `run_pipeline(source_path: str | Path, shared_root: str | Path) -> dict`
**Details**:
- Create and clean `shared/input`, `shared/processing`, `shared/output`, `shared/results`, and `shared/audit`
- Write `pipeline-summary.json` and `pipeline-summary.txt`
- Print a human-readable completion summary to the terminal
