Run the multi-agent banking pipeline end-to-end.

Steps:
1. Check that `sample-transactions.json` exists
2. Clear `shared/` directories
3. Run the pipeline with `python integrator.py`
4. Show a summary of results from `shared/results/`
5. Report any transactions that were rejected and why

Expected output:
- Pipeline completion status
- Count of settled, pending review, and rejected transactions
- Rejection reasons grouped by transaction ID
