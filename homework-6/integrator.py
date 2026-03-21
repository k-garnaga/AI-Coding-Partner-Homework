from __future__ import annotations

import argparse

from pipeline.config import DEFAULT_SAMPLE_FILE, DEFAULT_SHARED_ROOT
from pipeline.orchestrator import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the homework 6 banking pipeline.")
    parser.add_argument("--source", default=str(DEFAULT_SAMPLE_FILE), help="Path to the source transaction JSON file.")
    parser.add_argument("--shared-root", default=str(DEFAULT_SHARED_ROOT), help="Directory for pipeline message passing.")
    args = parser.parse_args()

    summary = run_pipeline(source_path=args.source, shared_root=args.shared_root)
    print("Pipeline completed successfully.")
    print(f"Processed transactions: {summary['processed_count']}")
    print(f"Status counts: {summary['status_counts']}")
    print(f"Risk counts: {summary['risk_counts']}")
    if summary["rejected_transactions"]:
        print("Rejected transactions:")
        for rejected in summary["rejected_transactions"]:
            print(f"- {rejected['transaction_id']}: {', '.join(rejected['reasons'])}")


if __name__ == "__main__":
    main()
