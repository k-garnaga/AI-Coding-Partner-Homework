from __future__ import annotations

import argparse
import json
from pathlib import Path

from pipeline.config import DEFAULT_SAMPLE_FILE, REQUIRED_TRANSACTION_FIELDS, SUPPORTED_CURRENCIES
from pipeline.models import amount_to_string, clone_message, decimal_from_value


def dry_run_validate_transactions(transactions: list[dict]) -> list[dict]:
    results = []
    for transaction in transactions:
        message = {
            "message_id": "dry-run",
            "timestamp": transaction.get("timestamp", ""),
            "source_agent": "integrator",
            "target_agent": "transaction_validator",
            "message_type": "transaction",
            "data": {
                "transaction_id": transaction.get("transaction_id", "unknown"),
                "transaction": transaction,
                "status": "received",
            },
        }
        processed = process_message(message)
        results.append(
            {
                "transaction_id": processed["data"]["transaction_id"],
                "status": processed["data"]["status"],
                "reasons": processed["data"]["validation"]["reasons"],
            }
        )
    return results


def process_message(message: dict) -> dict:
    transaction = message["data"]["transaction"]
    missing_fields = sorted(field for field in REQUIRED_TRANSACTION_FIELDS if not transaction.get(field))
    reasons: list[str] = []
    normalized_amount = None

    if missing_fields:
        reasons.extend(f"MISSING_{field.upper()}" for field in missing_fields)

    try:
        amount = decimal_from_value(transaction.get("amount"))
        normalized_amount = amount_to_string(amount)
        if amount <= 0:
            reasons.append("INVALID_AMOUNT_NON_POSITIVE")
    except ValueError:
        reasons.append("INVALID_AMOUNT_FORMAT")

    currency = transaction.get("currency")
    if currency not in SUPPORTED_CURRENCIES:
        reasons.append("INVALID_CURRENCY")

    is_valid = not reasons
    next_target = "fraud_detector" if is_valid else "results"
    status = "validated" if is_valid else "rejected"

    return clone_message(
        message,
        source_agent="transaction_validator",
        target_agent=next_target,
        status=status,
        extra={
            "validation": {
                "valid": is_valid,
                "reasons": reasons,
                "normalized_amount": normalized_amount,
            }
        },
    )


def _render_table(rows: list[dict]) -> str:
    lines = ["transaction_id | status | reasons", "--- | --- | ---"]
    for row in rows:
        reason_text = ", ".join(row["reasons"]) if row["reasons"] else "-"
        lines.append(f"{row['transaction_id']} | {row['status']} | {reason_text}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate transactions for the banking pipeline.")
    parser.add_argument("--source", default=str(DEFAULT_SAMPLE_FILE), help="Path to the JSON transaction file.")
    parser.add_argument("--dry-run", action="store_true", help="Validate transactions without running the full pipeline.")
    args = parser.parse_args()

    transactions = json.loads(Path(args.source).read_text(encoding="utf-8"))
    rows = dry_run_validate_transactions(transactions)
    valid_count = sum(1 for row in rows if row["status"] == "validated")
    invalid_count = len(rows) - valid_count

    if args.dry_run:
        print(_render_table(rows))
        print()
        print(f"total={len(rows)} valid={valid_count} invalid={invalid_count}")


if __name__ == "__main__":
    main()
