from __future__ import annotations

import json
from pathlib import Path

from pipeline.message_bus import ensure_shared_dirs
from pipeline.models import mask_account, utc_timestamp


def log_event(
    shared_root: str | Path,
    *,
    agent_name: str,
    transaction_id: str,
    outcome: str,
    source_account: str | None = None,
    destination_account: str | None = None,
    detail: dict | None = None,
) -> None:
    paths = ensure_shared_dirs(shared_root)
    audit_path = paths["audit"] / "audit.log"
    entry = {
        "timestamp": utc_timestamp(),
        "agent_name": agent_name,
        "transaction_id": transaction_id,
        "outcome": outcome,
        "source_account": mask_account(source_account),
        "destination_account": mask_account(destination_account),
        "detail": detail or {},
    }
    with audit_path.open("a", encoding="utf-8") as audit_file:
        audit_file.write(json.dumps(entry) + "\n")
