import os
import logging
import pandas as pd
from . import config

logger = logging.getLogger(__name__)

class TransactionExtractor:
    """Handles raw data ingestion vectors and file boundary validation."""

    def extract(self, filename: str = "raw_ledger.csv") -> pd.DataFrame:
        """Loads raw CSV data from the configured storage directory."""
        source_path = os.path.join(config.RAW_DATA_DIR, filename)
        logger.info(f"Extract Phase: Targeting file locator -> {source_path}")

        if not os.path.exists(source_path):
            error_msg = f"Extraction failed: File not found at target locator: {source_path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        try:
            df = pd.read_csv(source_path)
            logger.info(f"Extract Phase: Successfully ingested {len(df)} records.")
            return df
        except Exception as e:
            logger.exception("Extract Phase: Critical exception encountered during CSV read sequence.")
            raise e
