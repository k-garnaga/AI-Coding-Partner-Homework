# Homework 6: AI-Powered Multi-Agent Banking Pipeline

Created by: Garnaga Kostiantyn

This project implements a file-based banking pipeline that reads raw transactions, validates each record, scores it for fraud risk, and either settles the transaction or holds it for manual review. The implementation is deliberately deterministic so the behavior is easy to test, audit, and explain.

The system is organized as cooperating agents connected by JSON messages in shared directories. That keeps the flow visible on disk, makes the pipeline easy to demo, and supports the custom MCP server, which can answer questions about processed transactions directly from `shared/results/`.

## Agent Responsibilities
- `transaction_validator`: validates required fields, positive decimal amounts, and supported ISO 4217 currency codes.
- `fraud_detector`: assigns a fraud risk score and level based on amount, timing, and country-currency mismatch.
- `settlement_processor`: settles low- and medium-risk transactions or holds high-risk transactions for manual review.
- `integrator`: orchestrates file movement, audit logging, reporting, and final result storage.

## Architecture
```text
sample-transactions.json
        |
        v
  integrator.py
        |
        v
shared/input/*.json
        |
        v
transaction_validator
        |
        v
shared/output/*.json
        |
        v
fraud_detector
        |
        v
shared/output/*.json
        |
        v
settlement_processor
        |
        v
shared/results/*.json
        |
        +--> pipeline-summary.json
        +--> pipeline-summary.txt
        +--> MCP tools/resources
```

## Tech Stack
| Area | Choice |
| --- | --- |
| Language | Python 3.11+ |
| Money handling | `decimal.Decimal` |
| Testing | `pytest`, `pytest-cov` |
| MCP | `fastmcp`, `context7` |
| Messaging | JSON files in shared directories |

## Project Layout
- `agents/`: validator, fraud, and settlement agents.
- `pipeline/`: shared runtime utilities for messages, audit logging, and orchestration.
- `mcp/server.py`: custom FastMCP server for querying pipeline results.
- `tests/`: unit and integration coverage.
- `.claude/commands/`: slash-command style workflow files.
- `.claude/settings.json`: hook configuration for the coverage gate.

## Deliverables Included
- Specification and agent context documents.
- End-to-end pipeline implementation.
- Coverage gate hook plus reusable git hook.
- Custom Claude commands for spec generation, validation, and pipeline execution.
- MCP configuration for context7 and pipeline status queries.

## Remaining Submission Work
- Screenshots are stored in `docs/screenshots/` and should be embedded in the pull request description.
- Keep `shared/` as runtime-generated output; it is excluded from version control to keep the review focused on source files.
