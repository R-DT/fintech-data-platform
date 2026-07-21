import logging
import pandas as pd
from src.config import Settings

logger = logging.getLogger(__name__)

class TransactionValidator:
    """Handles strict data schema quality checks and boundary validations."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def validate_transactions(self, df: pd.DataFrame) -> dict[str, pd.Series]:
        """Audits the dataset and isolates rows breaking structural boundaries."""
        logger.info("Validation Phase: Auditing ledger schema health profiles...")
        
        # 1. Identify missing amounts
        null_amounts = df["Amount"].isnull()
        
        # 2. Identify unparseable date strings
        parsed_dates = pd.to_datetime(df["Date"], errors='coerce')
        invalid_dates = parsed_dates.isnull()
        
        # 3. Identify unsupported currencies
        invalid_currencies = ~df["Currency"].isin(self.settings.SUPPORTED_CURRENCIES)

        report = {
            "null_amounts": null_amounts,
            "invalid_dates": invalid_dates,
            "invalid_currencies": invalid_currencies
        }
        
        logger.info(f"Validation Phase: Audit complete. Found {null_amounts.sum()} null amounts, {invalid_dates.sum()} corrupt dates.")
        return report
