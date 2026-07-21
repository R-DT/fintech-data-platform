import os
import logging
import numpy as np
import pandas as pd
from datetime import timedelta
from src import config



# Standard naming-context logger initialization pattern
logger = logging.getLogger(__name__)

class TransactionGenerator:
    """Generates synthetic high-noise banking ledger entries for pipeline testing."""
    
    def __init__(self) -> None:
        # Utilize the modern NumPy RNG engine API
        self.rng = np.random.default_rng(config.RANDOM_SEED)

    def generate(self, filename: str = "raw_ledger.csv") -> str:
        count = config.NUMBER_OF_TRANSACTIONS
        logger.info(f"Initializing generation vector for {count} records...")
        
        data = {
            "TransactionID": [f"TXN{str(i).zfill(6)}" for i in range(1, count + 1)],
            "CustomerID": [f"CUST{str(self.rng.integers(100, 150))}" for _ in range(count)],
            "TransactionType": self.rng.choice(config.TRANSACTION_TYPES, size=count),
            "Amount": np.round(self.rng.uniform(5.0, 1500.0, size=count), 2),
            "Currency": self.rng.choice(config.SUPPORTED_CURRENCIES, size=count, p=[0.8, 0.1, 0.1]),
            "Channel": self.rng.choice(config.PAYMENT_CHANNELS, size=count),
            "Date": [(config.START_DATE + timedelta(days=int(self.rng.integers(0, 180)), hours=int(self.rng.integers(0, 24)))).strftime("%Y-%m-%d %H:%M:%S") for _ in range(count)],
            "Status": self.rng.choice(config.SYSTEM_STATUSES, size=count)
        }
        
        df = pd.DataFrame(data)
        
        # Inject explicit pipeline anomalies
        df.loc[self.rng.choice(df.index, size=15, replace=False), "Amount"] = np.nan
        df.loc[self.rng.choice(df.index, size=10, replace=False), "Date"] = "CORRUPT_DATETIME_STRING"
        
        output_path = os.path.join(config.RAW_DATA_DIR, filename)
        df.to_csv(output_path, index=False)
        logger.info(f"Target raw batch successfully deployed to: {output_path}")
        return output_path
