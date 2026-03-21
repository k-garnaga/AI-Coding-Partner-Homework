from __future__ import annotations

import copy

from agents.settlement_processor import process_message


def test_settlement_processor_settles_low_risk_transaction(sample_message: dict) -> None:
    screened_message = copy.deepcopy(sample_message)
    screened_message["data"]["status"] = "screened"
    screened_message["data"]["fraud_review"] = {
        "risk_score": 0,
        "risk_level": "LOW",
        "triggers": [],
    }

    result = process_message(screened_message)

    assert result["data"]["status"] == "settled"
    assert result["data"]["settlement"]["decision"] == "settled"
    assert result["data"]["settlement"]["settlement_amount"] == "1500.00"


def test_settlement_processor_holds_high_risk_transaction(sample_message: dict) -> None:
    reviewed_message = copy.deepcopy(sample_message)
    reviewed_message["data"]["status"] = "flagged_for_review"
    reviewed_message["data"]["fraud_review"] = {
        "risk_score": 10,
        "risk_level": "HIGH",
        "triggers": ["AMOUNT_OVER_10000", "AMOUNT_OVER_50000"],
    }

    result = process_message(reviewed_message)

    assert result["data"]["status"] == "pending_manual_review"
    assert result["data"]["settlement"]["decision"] == "held_for_manual_review"
    assert result["data"]["settlement"]["review_required"] is True


def test_settlement_processor_preserves_rejected_transaction(sample_message: dict) -> None:
    rejected_message = copy.deepcopy(sample_message)
    rejected_message["data"]["status"] = "rejected"

    result = process_message(rejected_message)

    assert result["data"]["status"] == "rejected"
    assert result["data"]["settlement"] == {
        "decision": "not_processed",
        "review_required": False,
    }
