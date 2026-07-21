import logging
import pandas as pd
from src.config import Settings

logger = logging.getLogger(__name__)

class TransactionAnalyzer:
    """Calculates financial aggregation performance metrics."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def calculate_metrics(self, df: pd.DataFrame) -> dict:
        logger.info("Analytics Phase: Calculating core metrics profile...")
        
        if df.empty:
            logger.warning("Analytics Phase: Dataset is empty.")
            return {}

        metrics = {
            "total_transaction_count": int(len(df)),
            "total_volume": float(df["Amount"].sum()),
            "average_value": float(df["Amount"].mean()),
            "status_breakdown": df["Status"].value_counts().to_dict(),
            "channel_volume": df["Channel"].value_counts().to_dict()
        }

        logger.info("Analytics Phase: Metrics calculation completed.")
        return metrics
