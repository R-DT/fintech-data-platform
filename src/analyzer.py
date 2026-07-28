import logging

import pandas as pd

logger = logging.getLogger(__name__)


class TransactionAnalyzer:
    """Computes downstream core analytical accounting metrics aggregates."""

    def __init__(self, settings) -> None:
        self.settings = settings

    def calculate_metrics(self, df: pd.DataFrame) -> dict:
        """Aggregates transactional values across the dataset."""
        logger.info(
            "Analyzer Phase: Aggregates metric ledger tracking sheet updates..."
        )

        if df.empty:
            logger.warning("Analyzer Phase: Received empty Dataframe asset.")
            return {
                "total_volume": 0.0,
                "transaction_count": 0,
                "average_transaction_value": 0.0,
            }

        # FIX: Shift legacy capitalized strings down to lowercase columns
        total_volume = float(df["amount"].sum())
        transaction_count = len(df)
        average_value = float(df["amount"].mean()) if transaction_count > 0 else 0.0

        metrics = {
            "total_volume": round(total_volume, 2),
            "transaction_count": transaction_count,
            "average_transaction_value": round(average_value, 2),
        }

        logger.info(
            f"Metrics Calculated - Volume: {metrics['total_volume']} | "
            f"Count: {metrics['transaction_count']}"
        )
        return metrics
