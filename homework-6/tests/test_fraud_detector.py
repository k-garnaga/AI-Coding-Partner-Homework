from __future__ import annotations

import copy

from agents.fraud_detector import process_message


def test_fraud_detector_scores_high_risk_transaction(sample_message: dict) -> None:
    validated_message = copy.deepcopy(sample_message)
    validated_message["data"]["status"] = "validated"
    validated_message["data"]["transaction"]["amount"] = "60000.00"
    validated_message["data"]["transaction"]["timestamp"] = "2026-03-16T03:15:00Z"
    validated_message["data"]["transaction"]["metadata"]["country"] = "DE"

    result = process_message(validated_message)

    assert result["data"]["status"] == "flagged_for_review"
    assert result["data"]["fraud_review"] == {
        "risk_score": 10,
        "risk_level": "HIGH",
        "triggers": ["AMOUNT_OVER_10000", "AMOUNT_OVER_50000", "UNUSUAL_HOUR", "CROSS_BORDER"],
    }


def test_fraud_detector_scores_low_risk_transaction(sample_message: dict) -> None:
    validated_message = copy.deepcopy(sample_message)
    validated_message["data"]["status"] = "validated"

    result = process_message(validated_message)

    assert result["data"]["status"] == "screened"
    assert result["target_agent"] == "settlement_processor"
    assert result["data"]["fraud_review"] == {
        "risk_score": 0,
        "risk_level": "LOW",
        "triggers": [],
    }
