from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

from agents import transaction_validator
from agents.transaction_validator import dry_run_validate_transactions, process_message


def test_validator_accepts_supported_currency_and_positive_amount(sample_message: dict) -> None:
    result = process_message(sample_message)

    assert result["data"]["status"] == "validated"
    assert result["target_agent"] == "fraud_detector"
    assert result["data"]["validation"]["normalized_amount"] == "1500.00"
    assert result["data"]["validation"]["reasons"] == []


def test_validator_rejects_invalid_currency_and_negative_amount(sample_message: dict) -> None:
    invalid_message = copy.deepcopy(sample_message)
    invalid_message["data"]["transaction"]["amount"] = "-10.00"
    invalid_message["data"]["transaction"]["currency"] = "XYZ"

    result = process_message(invalid_message)

    assert result["data"]["status"] == "rejected"
    assert result["target_agent"] == "results"
    assert "INVALID_AMOUNT_NON_POSITIVE" in result["data"]["validation"]["reasons"]
    assert "INVALID_CURRENCY" in result["data"]["validation"]["reasons"]


def test_dry_run_validation_returns_summary_rows(sample_transaction: dict) -> None:
    invalid_transaction = copy.deepcopy(sample_transaction)
    invalid_transaction["transaction_id"] = "TXN101"
    invalid_transaction["currency"] = "XYZ"

    rows = dry_run_validate_transactions([sample_transaction, invalid_transaction])

    assert rows == [
        {"transaction_id": "TXN100", "status": "validated", "reasons": []},
        {"transaction_id": "TXN101", "status": "rejected", "reasons": ["INVALID_CURRENCY"]},
    ]


def test_validator_rejects_missing_fields_and_invalid_amount_format(sample_message: dict) -> None:
    invalid_message = copy.deepcopy(sample_message)
    invalid_message["data"]["transaction"]["destination_account"] = ""
    invalid_message["data"]["transaction"]["amount"] = "abc"

    result = process_message(invalid_message)

    assert result["data"]["status"] == "rejected"
    assert "MISSING_DESTINATION_ACCOUNT" in result["data"]["validation"]["reasons"]
    assert "INVALID_AMOUNT_FORMAT" in result["data"]["validation"]["reasons"]


def test_validator_main_prints_dry_run_table(tmp_path: Path, capsys, monkeypatch, sample_transaction: dict) -> None:
    source_file = tmp_path / "transactions.json"
    invalid_transaction = copy.deepcopy(sample_transaction)
    invalid_transaction["transaction_id"] = "TXN102"
    invalid_transaction["currency"] = "XYZ"
    source_file.write_text(json.dumps([sample_transaction, invalid_transaction]), encoding="utf-8")

    monkeypatch.setattr(sys, "argv", ["transaction_validator.py", "--source", str(source_file), "--dry-run"])
    transaction_validator.main()

    output = capsys.readouterr().out
    assert "transaction_id | status | reasons" in output
    assert "TXN102 | rejected | INVALID_CURRENCY" in output
    assert "total=2 valid=1 invalid=1" in output
