import logging
import pandas as pd
from src.config import Settings

logger = logging.getLogger(__name__)

class TransactionTransformer:
    """Executes data repair, cleanup adjustments, and currency normalization."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def clean_transactions(self, df: pd.DataFrame, validation_report: dict[str, pd.Series]) -> pd.DataFrame:
        logger.info("Transform Phase: Repairing data entries...")
        
        # Apply boolean mask filters to the original dataframe BEFORE index changes happen
        clean_df = df[~validation_report["invalid_currencies"]].copy()

        # 1. Action Null Amounts: Repair with fallback numeric 0.0 value
        clean_df["Amount"] = clean_df["Amount"].fillna(0.0)

        # 2. Action Corrupt Dates: Coerce safely and drop unparseable rows
        clean_df["Date"] = pd.to_datetime(clean_df["Date"], errors='coerce')
        clean_df = clean_df.dropna(subset=["Date"])

        logger.info(f"Transform Phase: Clean complete. Retained {len(clean_df)} records.")
        return clean_df

