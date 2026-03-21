from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest

from pipeline.message_bus import ensure_shared_dirs, reset_shared_dirs
from pipeline.models import amount_to_string, decimal_from_value, mask_account


def test_decimal_helpers_and_masking_handle_edge_cases() -> None:
    assert decimal_from_value("12.345") == Decimal("12.35")
    assert amount_to_string(Decimal("12")) == "12.00"
    assert mask_account("ACC-1234") == "****1234"
    assert mask_account(None) is None

    with pytest.raises(ValueError):
        decimal_from_value("not-a-number")


def test_reset_shared_dirs_clears_existing_files(tmp_path: Path) -> None:
    shared_root = tmp_path / "shared"
    paths = ensure_shared_dirs(shared_root)
    (paths["results"] / "stale.json").write_text("{}", encoding="utf-8")

    reset_shared_dirs(shared_root)

    assert not (shared_root / "results" / "stale.json").exists()
    assert (shared_root / "input").exists()