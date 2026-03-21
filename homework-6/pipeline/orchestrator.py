from __future__ import annotations

import json
from pathlib import Path

from agents.fraud_detector import process_message as fraud_process_message
from agents.settlement_processor import process_message as settlement_process_message
from agents.transaction_validator import process_message as validator_process_message
from pipeline.audit import log_event
from pipeline.config import DEFAULT_SAMPLE_FILE, DEFAULT_SHARED_ROOT
from pipeline.message_bus import archive_result, move_to_processing, publish_output, queue_input, read_json, reset_shared_dirs, write_json
from pipeline.models import build_initial_message, utc_timestamp


AGENT_CHAIN = [
    ("transaction_validator", validator_process_message),
    ("fraud_detector", fraud_process_message),
    ("settlement_processor", settlement_process_message),
]


def _run_stage(shared_root: Path, stage_name: str, processor, message: dict) -> dict:
    input_path = queue_input(shared_root, message, stage_name)
    processing_path = move_to_processing(shared_root, input_path, message, stage_name)
    staged_message = read_json(processing_path)
    result = processor(staged_message)
    publish_output(shared_root, result, stage_name)
    return result


def _result_summary(processed_messages: list[dict]) -> dict:
    status_counts: dict[str, int] = {}
    risk_counts: dict[str, int] = {}

    for message in processed_messages:
        status = message["data"]["status"]
        status_counts[status] = status_counts.get(status, 0) + 1

        risk_level = message["data"].get("fraud_review", {}).get("risk_level")
        if risk_level:
            risk_counts[risk_level] = risk_counts.get(risk_level, 0) + 1

    rejected = [
        {
            "transaction_id": message["data"]["transaction_id"],
            "reasons": message["data"].get("validation", {}).get("reasons", []),
        }
        for message in processed_messages
        if message["data"]["status"] == "rejected"
    ]

    return {
        "generated_at": utc_timestamp(),
        "processed_count": len(processed_messages),
        "status_counts": status_counts,
        "risk_counts": risk_counts,
        "rejected_transactions": rejected,
    }


def _summary_text(summary: dict) -> str:
    lines = [
        "Pipeline Summary",
        f"generated_at: {summary['generated_at']}",
        f"processed_count: {summary['processed_count']}",
        f"status_counts: {summary['status_counts']}",
        f"risk_counts: {summary['risk_counts']}",
        f"rejected_transactions: {summary['rejected_transactions']}",
    ]
    return "\n".join(lines)


def run_pipeline(source_path: str | Path = DEFAULT_SAMPLE_FILE, shared_root: str | Path = DEFAULT_SHARED_ROOT) -> dict:
    source = Path(source_path)
    shared = Path(shared_root)
    reset_shared_dirs(shared)
    transactions = json.loads(source.read_text(encoding="utf-8"))
    processed_messages: list[dict] = []

    for transaction in transactions:
        message = build_initial_message(transaction)
        transaction_id = transaction["transaction_id"]
        log_event(
            shared,
            agent_name="integrator",
            transaction_id=transaction_id,
            outcome="queued",
            source_account=transaction.get("source_account"),
            destination_account=transaction.get("destination_account"),
        )

        for stage_name, processor in AGENT_CHAIN:
            message = _run_stage(shared, stage_name, processor, message)
            log_event(
                shared,
                agent_name=stage_name,
                transaction_id=transaction_id,
                outcome=message["data"]["status"],
                source_account=transaction.get("source_account"),
                destination_account=transaction.get("destination_account"),
                detail={
                    "target_agent": message["target_agent"],
                },
            )
            if message["target_agent"] == "results":
                break

        archive_result(shared, message)
        processed_messages.append(message)

    summary = _result_summary(processed_messages)
    write_json(shared / "results" / "pipeline-summary.json", summary)
    (shared / "results" / "pipeline-summary.txt").write_text(_summary_text(summary), encoding="utf-8")
    return summary
