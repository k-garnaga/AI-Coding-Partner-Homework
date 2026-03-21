from __future__ import annotations

from datetime import datetime

from pipeline.config import CURRENCY_HOME_COUNTRIES
from pipeline.models import clone_message, decimal_from_value


def _is_unusual_hour(timestamp: str) -> bool:
    hour = datetime.fromisoformat(timestamp.replace("Z", "+00:00")).hour
    return 2 <= hour <= 5


def _is_cross_border(transaction: dict) -> bool:
    country = (transaction.get("metadata") or {}).get("country")
    currency = transaction.get("currency")
    allowed_countries = CURRENCY_HOME_COUNTRIES.get(currency, set())
    return bool(country and allowed_countries and country not in allowed_countries)


def _risk_level(score: int) -> str:
    if score >= 7:
        return "HIGH"
    if score >= 3:
        return "MEDIUM"
    return "LOW"


def process_message(message: dict) -> dict:
    if message["data"].get("status") != "validated":
        return clone_message(
            message,
            source_agent="fraud_detector",
            target_agent="results",
            status=message["data"].get("status", "rejected"),
        )

    transaction = message["data"]["transaction"]
    amount = decimal_from_value(transaction["amount"])
    score = 0
    triggers: list[str] = []

    if amount > 10000:
        score += 3
        triggers.append("AMOUNT_OVER_10000")

    if amount > 50000:
        score += 4
        triggers.append("AMOUNT_OVER_50000")

    if _is_unusual_hour(transaction["timestamp"]):
        score += 2
        triggers.append("UNUSUAL_HOUR")

    if _is_cross_border(transaction):
        score += 2
        triggers.append("CROSS_BORDER")

    score = min(score, 10)
    level = _risk_level(score)
    status = "flagged_for_review" if level == "HIGH" else "screened"

    return clone_message(
        message,
        source_agent="fraud_detector",
        target_agent="settlement_processor",
        status=status,
        extra={
            "fraud_review": {
                "risk_score": score,
                "risk_level": level,
                "triggers": triggers,
            }
        },
    )
