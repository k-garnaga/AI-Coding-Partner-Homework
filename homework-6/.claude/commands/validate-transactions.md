Validate all transactions in `sample-transactions.json` without processing them.

Steps:
1. Run the validator in dry-run mode with `python agents/transaction_validator.py --dry-run`
2. Report total count, valid count, invalid count, and reasons for rejection
3. Show the result table for every transaction

Expected output:
- Markdown table with `transaction_id`, `status`, and `reasons`
- Summary counts for valid and invalid records
