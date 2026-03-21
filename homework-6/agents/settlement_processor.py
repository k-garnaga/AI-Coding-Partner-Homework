from __future__ import annotations

from datetime import datetime

from pipeline.models import amount_to_string, clone_message, decimal_from_value


def _batch_id(timestamp: str) -> str:
    date = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    return f"SETTLEMENT-{date.strftime('%Y%m%d')}"


def process_message(message: dict) -> dict:
    if message["data"].get("status") == "rejected":
        return clone_message(
            message,
            source_agent="settlement_processor",
            target_agent="results",
            status="rejected",
            extra={
                "settlement": {
                    "decision": "not_processed",
                    "review_required": False,
                }
            },
        )

    transaction = message["data"]["transaction"]
    amount = decimal_from_value(transaction["amount"])
    fraud_level = message["data"].get("fraud_review", {}).get("risk_level", "LOW")
    review_required = fraud_level == "HIGH"

    if review_required:
        decision = "held_for_manual_review"
        status = "pending_manual_review"
    else:
        decision = "settled"
        status = "settled"

    return clone_message(
        message,
        source_agent="settlement_processor",
        target_agent="results",
        status=status,
        extra={
            "settlement": {
                "decision": decision,
                "review_required": review_required,
                "settlement_amount": amount_to_string(amount),
                "batch_id": _batch_id(transaction["timestamp"]),
            }
        },
    )
