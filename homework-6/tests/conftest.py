from __future__ import annotations

import copy

import pytest


@pytest.fixture
def sample_transaction() -> dict:
    return {
        "transaction_id": "TXN100",
        "timestamp": "2026-03-16T09:00:00Z",
        "source_account": "ACC-1001",
        "destination_account": "ACC-2001",
        "amount": "1500.00",
        "currency": "USD",
        "transaction_type": "transfer",
        "description": "Fixture transfer",
        "metadata": {
            "channel": "online",
            "country": "US",
        },
    }


@pytest.fixture
def sample_message(sample_transaction: dict) -> dict:
    return {
        "message_id": "fixture-message",
        "timestamp": sample_transaction["timestamp"],
        "source_agent": "integrator",
        "target_agent": "transaction_validator",
        "message_type": "transaction",
        "data": {
            "transaction_id": sample_transaction["transaction_id"],
            "transaction": copy.deepcopy(sample_transaction),
            "status": "received",
        },
    }
