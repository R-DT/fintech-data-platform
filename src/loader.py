import logging
from abc import ABC, abstractmethod
from pathlib import Path
import json
import pandas as pd
from src.config import Settings

logger = logging.getLogger(__name__)

class BaseLoader(ABC):
    """Abstract baseline interface for extensible multi-destination pipeline loaders."""
    
    @abstractmethod
    def save_data(self, df: pd.DataFrame, target_name: str) -> str:
        pass

class FileLoader(BaseLoader):
    """Production file system persistence driver handles CSV and JSON outputs."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def save_data(self, df: pd.DataFrame, target_name: str = "cleaned_ledger.csv") -> str:
        destination: Path = self.settings.PROCESSED_DATA_DIR / target_name
        destination.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(destination, index=False)
        logger.info(f"Load Phase: Data written to file -> {destination}")
        return str(destination)

    def save_report(self, metrics: dict, target_name: str = "analytics_report.json") -> str:
        destination: Path = self.settings.REPORTS_DIR / target_name
        destination.parent.mkdir(parents=True, exist_ok=True)
        with open(destination, "w") as f:
            json.dump(metrics, f, indent=4)
        logger.info(f"Load Phase: Report written to file -> {destination}")
        return str(destination)
