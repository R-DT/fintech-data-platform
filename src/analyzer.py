import logging
import pandas as pd

logger = logging.getLogger(__name__)

class TransactionAnalyzer:
    """Executes financial aggregation matrix calculations on cleaned ledgers."""

    def calculate_metrics(self, df: pd.DataFrame) -> dict:
        """Computes core business KPIs across the transaction batch."""
        logger.info("Analytics Phase: Commencing aggregation metrics calculation...")
        
        if df.empty:
            logger.warning("Analytics Phase: Cleaned dataframe is empty. Returning blank metrics.")
            return {}

        metrics = {
            "total_transaction_count": int(len(df)),
            "total_volume_usd_equiv": float(df["Amount"].sum()),
            "average_transaction_value": float(df["Amount"].mean()),
            "status_distribution": df["Status"].value_value_counts().to_dict() if hasattr(df["Status"], "value_value_counts") else df["Status"].value_counts().to_dict(),
            "channel_velocity": df["Channel"].value_counts().to_dict(),
            "highest_value_alerts": df[df["Amount"] > 1200][["TransactionID", "CustomerID", "Amount"]].to_dict(orient="records")
        }

        logger.info("Analytics Phase: Aggregations calculated successfully.")
        return metrics
