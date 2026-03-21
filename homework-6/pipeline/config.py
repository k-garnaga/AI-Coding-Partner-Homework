from pathlib import Path


SUPPORTED_CURRENCIES = {"USD", "EUR", "GBP", "JPY"}
CURRENCY_HOME_COUNTRIES = {
    "USD": {"US"},
    "EUR": {"DE", "FR", "ES", "IT", "NL", "BE", "PT", "IE"},
    "GBP": {"GB"},
    "JPY": {"JP"},
}
REQUIRED_TRANSACTION_FIELDS = {
    "transaction_id",
    "timestamp",
    "source_account",
    "destination_account",
    "amount",
    "currency",
    "transaction_type",
}
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SAMPLE_FILE = PROJECT_ROOT / "sample-transactions.json"
DEFAULT_SHARED_ROOT = PROJECT_ROOT / "shared"
SHARED_DIRECTORIES = ("input", "processing", "output", "results", "audit")
