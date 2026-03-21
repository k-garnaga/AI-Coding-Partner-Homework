from __future__ import annotations

import json
from pathlib import Path

from fastmcp import FastMCP


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_ROOT / "shared" / "results"
mcp = FastMCP("pipeline-status")


def _transaction_file(transaction_id: str, results_dir: Path | None = None) -> Path:
    root = results_dir or RESULTS_DIR
    return root / f"{transaction_id}.json"


def load_transaction_status(transaction_id: str, results_dir: Path | None = None) -> dict:
    file_path = _transaction_file(transaction_id, results_dir)
    if not file_path.exists():
        raise FileNotFoundError(f"No result found for transaction_id={transaction_id}")
    payload = json.loads(file_path.read_text(encoding="utf-8"))
    return {
        "transaction_id": transaction_id,
        "status": payload["data"]["status"],
        "fraud_review": payload["data"].get("fraud_review", {}),
        "settlement": payload["data"].get("settlement", {}),
        "validation": payload["data"].get("validation", {}),
    }


def list_results(results_dir: Path | None = None) -> dict:
    root = results_dir or RESULTS_DIR
    summary_file = root / "pipeline-summary.json"
    if summary_file.exists():
        return json.loads(summary_file.read_text(encoding="utf-8"))

    result_files = sorted(path for path in root.glob("*.json") if path.name != "pipeline-summary.json")
    transactions = []
    for result_file in result_files:
        payload = json.loads(result_file.read_text(encoding="utf-8"))
        transactions.append(
            {
                "transaction_id": payload["data"]["transaction_id"],
                "status": payload["data"]["status"],
            }
        )
    return {
        "processed_count": len(transactions),
        "transactions": transactions,
    }


def load_summary_text(results_dir: Path | None = None) -> str:
    root = results_dir or RESULTS_DIR
    summary_text_file = root / "pipeline-summary.txt"
    if summary_text_file.exists():
        return summary_text_file.read_text(encoding="utf-8")
    return "No pipeline summary has been generated yet."


@mcp.tool(name="get_transaction_status")
def get_transaction_status(transaction_id: str) -> dict:
    return load_transaction_status(transaction_id)


@mcp.tool(name="list_pipeline_results")
def list_pipeline_results() -> dict:
    return list_results()


@mcp.resource("pipeline://summary")
def pipeline_summary() -> str:
    return load_summary_text()


if __name__ == "__main__":
    mcp.run()
