import logging
from pathlib import Path
import pandas as pd
from src.config import Settings

logger = logging.getLogger(__name__)

class TransactionExtractor:
    """Handles raw data ingestion from local storage volumes."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def extract_transactions(self, filename: str = "raw_ledger.csv") -> pd.DataFrame:
        source_path: Path = self.settings.RAW_DATA_DIR / filename
        logger.info(f"Extract Phase: Reading from -> {source_path}")

        if not source_path.exists():
            error_msg = f"Extraction failed: File not found at {source_path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        try:
            df = pd.read_csv(source_path)
            logger.info(f"Extract Phase: Ingested {len(df)} records.")
            return df
        except Exception as e:
            logger.exception("Extract Phase: Failed to parse raw CSV data stream.")
            raise e
