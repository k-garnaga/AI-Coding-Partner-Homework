from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


SERVER_PATH = Path(__file__).resolve().parents[1] / "mcp" / "server.py"
SPEC = importlib.util.spec_from_file_location("homework6_mcp_server", SERVER_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)

list_results = MODULE.list_results
load_summary_text = MODULE.load_summary_text
load_transaction_status = MODULE.load_transaction_status


def test_load_transaction_status_reads_transaction_result(tmp_path: Path) -> None:
    results_dir = tmp_path / "results"
    results_dir.mkdir()
    payload = {
        "data": {
            "transaction_id": "TXN999",
            "status": "settled",
            "fraud_review": {"risk_level": "LOW"},
            "settlement": {"decision": "settled"},
            "validation": {"valid": True, "reasons": []},
        }
    }
    (results_dir / "TXN999.json").write_text(json.dumps(payload), encoding="utf-8")

    status = load_transaction_status("TXN999", results_dir)

    assert status["transaction_id"] == "TXN999"
    assert status["status"] == "settled"
    assert status["settlement"] == {"decision": "settled"}


def test_list_results_prefers_pipeline_summary_json(tmp_path: Path) -> None:
    results_dir = tmp_path / "results"
    results_dir.mkdir()
    summary = {"processed_count": 2, "status_counts": {"settled": 2}}
    (results_dir / "pipeline-summary.json").write_text(json.dumps(summary), encoding="utf-8")

    assert list_results(results_dir) == summary


def test_load_summary_text_reads_text_file(tmp_path: Path) -> None:
    results_dir = tmp_path / "results"
    results_dir.mkdir()
    (results_dir / "pipeline-summary.txt").write_text("Pipeline Summary", encoding="utf-8")

    assert load_summary_text(results_dir) == "Pipeline Summary"


def test_load_transaction_status_raises_for_unknown_transaction(tmp_path: Path) -> None:
    results_dir = tmp_path / "results"
    results_dir.mkdir()

    with pytest.raises(FileNotFoundError):
        load_transaction_status("DOES-NOT-EXIST", results_dir)


def test_list_results_falls_back_to_individual_transaction_files(tmp_path: Path) -> None:
    results_dir = tmp_path / "results"
    results_dir.mkdir()
    for transaction_id, status in (("TXN201", "settled"), ("TXN202", "rejected")):
        payload = {"data": {"transaction_id": transaction_id, "status": status}}
        (results_dir / f"{transaction_id}.json").write_text(json.dumps(payload), encoding="utf-8")

    result = list_results(results_dir)

    assert result == {
        "processed_count": 2,
        "transactions": [
            {"transaction_id": "TXN201", "status": "settled"},
            {"transaction_id": "TXN202", "status": "rejected"},
        ],
    }


def test_mcp_wrappers_use_module_results_dir(tmp_path: Path, monkeypatch) -> None:
    results_dir = tmp_path / "results"
    results_dir.mkdir()
    payload = {
        "data": {
            "transaction_id": "TXN301",
            "status": "settled",
            "fraud_review": {"risk_level": "LOW"},
            "settlement": {"decision": "settled"},
            "validation": {"valid": True, "reasons": []},
        }
    }
    summary = {"processed_count": 1, "status_counts": {"settled": 1}}
    (results_dir / "TXN301.json").write_text(json.dumps(payload), encoding="utf-8")
    (results_dir / "pipeline-summary.json").write_text(json.dumps(summary), encoding="utf-8")
    (results_dir / "pipeline-summary.txt").write_text("Pipeline Summary", encoding="utf-8")

    monkeypatch.setattr(MODULE, "RESULTS_DIR", results_dir)

    assert MODULE.get_transaction_status("TXN301")["status"] == "settled"
    assert MODULE.list_pipeline_results() == summary
    assert MODULE.pipeline_summary() == "Pipeline Summary"
