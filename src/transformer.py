import logging
import pandas as pd
from src import config


logger = logging.getLogger(__name__)

class TransactionTransformer:
    """Executes cleaning, schema enforcement, and validation on transaction records."""

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cleans and repairs the explicit data anomalies injected into the batch."""
        logger.info("Transform Phase: Initiating cleaning matrix...")
        processed_df = df.copy()

        # 1. Handle Null Amounts: Replace with 0.0 or forward fill (we will default to 0.0)
        null_count = processed_df["Amount"].isnull().sum()
        if null_count > 0:
            logger.warning(f"Transform Phase: Found {null_count} null amounts. Appending default numeric values.")
            processed_df["Amount"] = processed_df["Amount"].fillna(0.0)

        # 2. Schema Enforcement: Coerce Datetime strings safely, dropping unparseable rows
        processed_df["Date"] = pd.to_datetime(processed_df["Date"], errors='coerce')
        corrupt_date_count = processed_df["Date"].isnull().sum()
        if corrupt_date_count > 0:
            logger.warning(f"Transform Phase: Dropping {corrupt_date_count} rows containing unparseable timestamps.")
            processed_df = processed_df.dropna(subset=["Date"])

        # 3. Currency Schema Validation: Filter down to strictly supported system currencies
        initial_rows = len(processed_df)
        processed_df = processed_df[processed_df["Currency"].isin(config.SUPPORTED_CURRENCIES)]
        dropped_currency = initial_rows - len(processed_df)
        if dropped_currency > 0:
            logger.warning(f"Transform Phase: Dropped {dropped_currency} rows due to unsupported currency types.")

        logger.info(f"Transform Phase: Cleaning completed. Retained {len(processed_df)} valid records.")
        return processed_df
