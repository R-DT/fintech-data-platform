from enum import Enum
from pathlib import Path


class TransactionStatus(str, Enum):
    SUCCESSFUL = "Successful"
    FAILED = "Failed"
    PENDING = "Pending"


class PaymentChannel(str, Enum):
    MOBILE_APP = "Mobile App"
    WEB_PORTAL = "Web Portal"
    POS_TERMINAL = "POS Terminal"
    ATM = "ATM"
    USSD = "USSD"


class TransactionType(str, Enum):
    DEPOSIT = "Deposit"
    WITHDRAWAL = "Withdrawal"
    TRANSFER = "Transfer"
    BILL_PAYMENT = "Bill Payment"


class Settings:
    """Centralized configuration manager for platform parameters and directory paths."""

    def __init__(self) -> None:
        # Path Routing Maps via Pathlib
        self.BASE_DIR: Path = Path(__file__).resolve().parent.parent
        self.RAW_DATA_DIR: Path = self.BASE_DIR / "data" / "raw"
        self.PROCESSED_DATA_DIR: Path = self.BASE_DIR / "data" / "processed"
        self.REPORTS_DIR: Path = self.BASE_DIR / "data" / "reports"

        # Tracking the .env file path for environment variables
        self.ENV_FILE_PATH: Path = self.BASE_DIR / ".env"

        # Engine Control Parameters
        self.NUMBER_OF_TRANSACTIONS: int = 1000
        self.START_DATE_STR: str = "2026-01-01"
        self.RANDOM_SEED: int = 42

        # Domain Configuration Profiles
        self.SUPPORTED_CURRENCIES: list[str] = ["NGN", "USD", "EUR"]
        self.CHANNELS: list[str] = [c.value for c in PaymentChannel]
        self.TYPES: list[str] = [t.value for t in TransactionType]
        self.STATUS_POOL: list[str] = [
            TransactionStatus.SUCCESSFUL.value,
            TransactionStatus.SUCCESSFUL.value,
            TransactionStatus.SUCCESSFUL.value,
            TransactionStatus.FAILED.value,
            TransactionStatus.PENDING.value,
        ]
        # AWS Cloud Data Lake Infrastructure Targets
        self.AWS_S3_BUCKET_NAME: str = "fintech-data-platform-lake"
        self.AWS_S3_RAW_KEY: str = "raw/transactions.csv"
        self.AWS_S3_PROCESSED_KEY: str = "processed/cleaned_ledger.parquet"
