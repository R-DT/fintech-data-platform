import logging
import pandas as pd
from src.config import Settings
from src.logger import setup_logger

logger = setup_logger(__name__)

class TransactionValidator:
    """Handles strict data schema quality audits and integrity validations."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def validate_transactions(self, df: pd.DataFrame) -> dict[str, pd.Series]:
        """Audits the raw dataset and maps boolean series identifying anomalies."""
        logger.info("Validation Phase: Checking data quality rules...")

        if df.empty:
            logger.warning("Validation Phase: Ingested DataFrame is empty.")
            return {
                "null_amounts": pd.Series(dtype=bool),
                "invalid_dates": pd.Series(dtype=bool),
                "invalid_currencies": pd.Series(dtype=bool)
            }

        # 1. Audit Rule: Identify missing transaction amounts
        null_amounts = df["Amount"].isnull()

        # 2. Audit Rule: Identify unparseable datetime formats
        parsed_dates = pd.to_datetime(df["Date"], errors="coerce")
        invalid_dates = parsed_dates.isnull()

        # 3. Audit Rule: Identify unsupported business currencies
        invalid_currencies = ~df["Currency"].isin(self.settings.SUPPORTED_CURRENCIES)

        # Generate diagnostic error logs for monitoring tools
        logger.info(
            f"Validation Audit Metrics - "
            f"Null Amounts: {null_amounts.sum()} | "
            f"Corrupt Timestamps: {invalid_dates.sum()} | "
            f"Invalid Currencies: {invalid_currencies.sum()}"
        )

        return {
            "null_amounts": null_amounts,
            "invalid_dates": invalid_dates,
            "invalid_currencies": invalid_currencies
        }
