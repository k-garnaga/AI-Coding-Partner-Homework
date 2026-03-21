# How to Run Homework 6

## 1. Install dependencies
```bash
cd homework-6
python3 -m pip install -r requirements.txt
```

## 2. Run the full pipeline
```bash
python integrator.py
```

## 3. Review generated outputs
1. Check `shared/results/` for one JSON result per transaction.
2. Open `shared/results/pipeline-summary.json` for the machine-readable summary.
3. Open `shared/results/pipeline-summary.txt` for the human-readable summary.
4. Review `shared/audit/audit.log` for masked audit entries.

## 4. Validate transactions without settlement
```bash
python agents/transaction_validator.py --dry-run
```

## 5. Run the test suite with coverage
```bash
pytest
```

## 6. Enable the git push coverage gate
```bash
chmod +x .githooks/pre-push
git config core.hooksPath .githooks
```

## 7. Start the custom MCP server
```bash
python mcp/server.py
```

## 8. Configure MCP clients
1. Point your client at `mcp.json` in `homework-6/`.
2. Ensure `context7` is available through `npx -y @upstash/context7-mcp@latest`.
3. Ensure the custom `pipeline-status` server starts with `python mcp/server.py`.

## 9. Run the custom Claude commands
1. Use `/write-spec` to regenerate the specification documents.
2. Use `/validate-transactions` to run validator-only checks.
3. Use `/run-pipeline` to run the full demo workflow.

## 10. Capture submission artifacts
1. Save the required screenshots in `docs/screenshots/`.
2. Embed or link the same screenshots in your pull request description.
