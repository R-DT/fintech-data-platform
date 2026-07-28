import logging

import pandas as pd

from src.config import Settings

logger = logging.getLogger(__name__)


class TransactionTransformer:
    """Executes data repair, cleanup adjustments, and currency normalization."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def clean_transactions(
        self, df: pd.DataFrame, validation_report: dict[str, pd.Series]
    ) -> pd.DataFrame:
        logger.info("Transform Phase: Cleaning data and repairing anomalies...")

        # Keep original columns to restore casing before returning
        original_columns = df.columns.tolist()

        # Create lowercase copy for internal operations
        df_lower = df.rename(columns=str.lower)

        # Apply boolean mask filters to lowercase copy (mask indexes align)
        clean_lower = df_lower.loc[~validation_report["invalid_currencies"]].copy()

        # 1. Action Null Amounts: Repair with fallback numeric 0.0 value
        clean_lower["amount"] = clean_lower["amount"].fillna(0.0)

        # 2. Action Corrupt Dates: Coerce safely and drop unparseable rows
        clean_lower["timestamp"] = pd.to_datetime(
            clean_lower["timestamp"], errors="coerce"
        )
        clean_lower = clean_lower.dropna(subset=["timestamp"])

        # Restore original column names (map lowercase names back)
        restore_map = {col.lower(): col for col in original_columns}
        clean_df = clean_lower.rename(columns=lambda c: restore_map.get(c, c))

        logger.info(
            f"Transform Phase: Clean complete. Retained {len(clean_df)} records."
        )
        return clean_df
