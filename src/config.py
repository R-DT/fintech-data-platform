import os
from datetime import datetime

# Absolute Path Routing Maps
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "reports") # Updated to map your reports layout!


# Engine Parameter Configurations
NUMBER_OF_TRANSACTIONS: int = 1000
START_DATE: datetime = datetime(2026, 1, 1)
RANDOM_SEED: int = 42

# Financial Domain Constraints
SUPPORTED_CURRENCIES: list[str] = ["NGN", "USD", "EUR"]
PAYMENT_CHANNELS: list[str] = ["Mobile App", "Web Portal", "POS Terminal", "ATM", "USSD"]
TRANSACTION_TYPES: list[str] = ["Deposit", "Withdrawal", "Transfer", "Bill Payment"]
SYSTEM_STATUSES: list[str] = ["Successful", "Successful", "Successful", "Failed", "Pending"]
