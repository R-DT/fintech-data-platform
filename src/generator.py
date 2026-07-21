import logging
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from src.config import Settings

logger = logging.getLogger(__name__)

class TransactionGenerator:
    """Generates synthetic transactions for pipeline data pipeline testing."""
    
    def __init__(self, settings: Settings) -> None:
        # Dependency Injection of Platform Settings
        self.settings = settings
        self.rng = np.random.default_rng(settings.RANDOM_SEED)

    def generate_transactions(self, filename: str = "raw_ledger.csv") -> str:
        count = self.settings.NUMBER_OF_TRANSACTIONS
        logger.info(f"Generating {count} mock transactions...")
        
        start_date = datetime.strptime(self.settings.START_DATE_STR, "%Y-%m-%d")
        
        data = {
            "TransactionID": [f"TXN{str(i).zfill(6)}" for i in range(1, count + 1)],
            "CustomerID": [f"CUST{str(self.rng.integers(100, 150))}" for _ in range(count)],
            "TransactionType": self.rng.choice(self.settings.TYPES, size=count),
            "Amount": np.round(self.rng.uniform(5.0, 1500.0, size=count), 2),
            "Currency": self.rng.choice(self.settings.SUPPORTED_CURRENCIES, size=count, p=[0.8, 0.1, 0.1]),
            "Channel": self.rng.choice(self.settings.CHANNELS, size=count),
            "Date": [(start_date + timedelta(days=int(self.rng.integers(0, 180)), hours=int(self.rng.integers(0, 24)))).strftime("%Y-%m-%d %H:%M:%S") for _ in range(count)],
            "Status": self.rng.choice(self.settings.STATUS_POOL, size=count)
        }
        
        df = pd.DataFrame(data)
        
        # Inject anomalies for validation and transformation checks
        df.loc[self.rng.choice(df.index, size=15, replace=False), "Amount"] = np.nan
        df.loc[self.rng.choice(df.index, size=10, replace=False), "Date"] = "CORRUPT_DATETIME_STRING"
        
        output_path = self.settings.RAW_DATA_DIR / filename
        # Ensure parent folder exists automatically via pathlib
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        df.to_csv(output_path, index=False)
        logger.info(f"Raw transactions written to: {output_path}")
        return str(output_path)
