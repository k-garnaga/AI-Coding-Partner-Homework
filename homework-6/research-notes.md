# Research Notes

## Query 1: Decimal handling for monetary arithmetic
- Search: `Python Decimal quantize ROUND_HALF_UP use context7`
- context7 library ID: `/python/cpython`
- Applied: standardized amount parsing through `Decimal(str(value))` and forced two-decimal formatting before agents emit normalized amounts or settlement outputs.

## Query 2: pytest coverage gate and temporary directories
- Search: `pytest coverage fail-under tmp_path use context7`
- context7 library ID: `/pytest-dev/pytest`
- Applied: used `tmp_path` for integration tests so `shared/` state is isolated, and wired the coverage gate to run `pytest --cov ... --cov-fail-under=80` before push.

## Query 3: FastMCP tools and resources
- Search: `FastMCP tool resource example use context7`
- context7 library ID: `/jlowin/fastmcp`
- Applied: exposed `get_transaction_status`, `list_pipeline_results`, and the `pipeline://summary` resource from `mcp/server.py` using FastMCP decorators.
