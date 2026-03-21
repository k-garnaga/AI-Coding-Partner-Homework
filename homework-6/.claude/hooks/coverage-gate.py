from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TEST_COMMAND = [
    sys.executable,
    "-m",
    "pytest",
    "--cov=agents",
    "--cov=pipeline",
    "--cov=integrator",
    "--cov=mcp",
    "--cov-report=term-missing",
    "--cov-fail-under=80",
]


def _load_context() -> dict:
    if sys.stdin.isatty():
        return {}

    payload = sys.stdin.read().strip()
    if not payload:
        return {}

    try:
        return json.loads(payload)
    except json.JSONDecodeError:
        return {}


def _command_from_context(context: dict) -> str:
    return str(
        context.get("command")
        or context.get("params", {}).get("command")
        or context.get("tool_input", {}).get("command")
        or ""
    )


def _emit_response(continue_execution: bool, message: str) -> int:
    print(json.dumps({"continue": continue_execution, "message": message}))
    return 0 if continue_execution else 2


def main() -> int:
    if "--git-hook" in sys.argv:
        command = "git push"
    else:
        context = _load_context()
        command = _command_from_context(context)

    if "git push" not in command:
        return _emit_response(True, "Coverage gate skipped because the command is not git push.")

    completed = subprocess.run(
        TEST_COMMAND,
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    if completed.returncode == 0:
        return _emit_response(True, "Coverage gate passed.")

    message = "Coverage gate failed. Run pytest and raise coverage to at least 80% before pushing."
    print(completed.stdout)
    print(completed.stderr, file=sys.stderr)
    return _emit_response(False, message)


if __name__ == "__main__":
    raise SystemExit(main())
