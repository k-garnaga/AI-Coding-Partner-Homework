from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import uuid


MONEY_QUANTUM = Decimal("0.01")


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def decimal_from_value(value: str | int | float | Decimal) -> Decimal:
    try:
        return Decimal(str(value)).quantize(MONEY_QUANTUM, rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError, TypeError) as error:
        raise ValueError(f"Invalid monetary amount: {value!r}") from error


def amount_to_string(amount: Decimal) -> str:
    return format(amount.quantize(MONEY_QUANTUM, rounding=ROUND_HALF_UP), ".2f")


def mask_account(account_number: str | None) -> str | None:
    if not account_number:
        return None

    suffix = account_number[-4:]
    return f"****{suffix}"


def build_initial_message(transaction: dict) -> dict:
    return {
        "message_id": str(uuid.uuid4()),
        "timestamp": utc_timestamp(),
        "source_agent": "integrator",
        "target_agent": "transaction_validator",
        "message_type": "transaction",
        "data": {
            "transaction_id": transaction["transaction_id"],
            "transaction": deepcopy(transaction),
            "status": "received",
        },
    }


def clone_message(
    message: dict,
    *,
    source_agent: str,
    target_agent: str,
    status: str | None = None,
    extra: dict | None = None,
) -> dict:
    cloned = deepcopy(message)
    cloned["timestamp"] = utc_timestamp()
    cloned["source_agent"] = source_agent
    cloned["target_agent"] = target_agent
    if status is not None:
        cloned["data"]["status"] = status
    if extra:
        cloned["data"].update(deepcopy(extra))
    return cloned
