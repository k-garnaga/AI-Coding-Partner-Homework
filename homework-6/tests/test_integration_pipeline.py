from __future__ import annotations

import json
from pathlib import Path

from pipeline.orchestrator import run_pipeline


def test_pipeline_processes_all_sample_transactions(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[1]
    source_file = project_root / "sample-transactions.json"
    shared_root = tmp_path / "shared"

    summary = run_pipeline(source_path=source_file, shared_root=shared_root)

    result_files = sorted(path for path in (shared_root / "results").glob("TXN*.json"))
    assert len(result_files) == 8
    assert summary["processed_count"] == 8
    assert summary["status_counts"] == {
        "settled": 5,
        "pending_manual_review": 1,
        "rejected": 2,
    }
    assert summary["risk_counts"] == {
        "LOW": 4,
        "MEDIUM": 1,
        "HIGH": 1,
    }

    txn005 = json.loads((shared_root / "results" / "TXN005.json").read_text(encoding="utf-8"))
    txn006 = json.loads((shared_root / "results" / "TXN006.json").read_text(encoding="utf-8"))
    txn007 = json.loads((shared_root / "results" / "TXN007.json").read_text(encoding="utf-8"))

    assert txn005["data"]["status"] == "pending_manual_review"
    assert txn006["data"]["validation"]["reasons"] == ["INVALID_CURRENCY"]
    assert txn007["data"]["validation"]["reasons"] == ["INVALID_AMOUNT_NON_POSITIVE"]


def test_pipeline_audit_log_masks_account_numbers(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[1]
    source_file = project_root / "sample-transactions.json"
    shared_root = tmp_path / "shared"

    run_pipeline(source_path=source_file, shared_root=shared_root)

    audit_log = (shared_root / "audit" / "audit.log").read_text(encoding="utf-8")

    assert "ACC-1001" not in audit_log
    assert "****1001" in audit_log
    assert '"agent_name": "transaction_validator"' in audit_log
