import os
import json
import logging
import pandas as pd
from . import config

logger = logging.getLogger(__name__)

class TransactionLoader:
    """Handles persistence layers for data layers and analytical reports."""

    def save_processed_data(self, df: pd.DataFrame, filename: str = "cleaned_ledger.csv") -> str:
        """Saves the structured, clean transactional dataset."""
        destination = os.path.join(config.PROCESSED_DATA_DIR, filename)
        df.to_csv(destination, index=False)
        logger.info(f"Load Phase: Clean ledger successfully written to -> {destination}")
        return destination

    def save_analytics_report(self, metrics: dict, filename: str = "analytics_report.json") -> str:
        """Saves the final calculated business metrics as a JSON asset."""
        destination = os.path.join(config.OUTPUT_DIR, filename)
        with open(destination, "w") as f:
            json.dump(metrics, f, indent=4)
        logger.info(f"Load Phase: Analytical KPI profile written to -> {destination}")
        return destination
