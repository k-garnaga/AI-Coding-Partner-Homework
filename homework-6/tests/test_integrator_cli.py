from __future__ import annotations

import json
import sys
from pathlib import Path

import integrator


def test_integrator_main_runs_pipeline_and_prints_summary(tmp_path: Path, capsys, monkeypatch, sample_transaction: dict) -> None:
    source_file = tmp_path / "transactions.json"
    shared_root = tmp_path / "shared"
    source_file.write_text(json.dumps([sample_transaction]), encoding="utf-8")

    monkeypatch.setattr(
        sys,
        "argv",
        ["integrator.py", "--source", str(source_file), "--shared-root", str(shared_root)],
    )
    integrator.main()

    output = capsys.readouterr().out
    assert "Pipeline completed successfully." in output
    assert "Processed transactions: 1" in output
    assert (shared_root / "results" / "TXN100.json").exists()
