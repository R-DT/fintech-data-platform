import logging
from pathlib import Path
import json
import pandas as pd
from sqlalchemy import text
from src.config import Settings
from src.database import DatabaseConnector

logger = logging.getLogger(__name__)

class FileLoader:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def save_to_csv(self, df: pd.DataFrame, target_name: str = "cleaned_ledger.csv") -> str:
        destination: Path = self.settings.PROCESSED_DATA_DIR / target_name
        destination.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(destination, index=False)
        logger.info(f"Load Phase: Clean transactions saved to CSV -> {destination}")
        return str(destination)

    def save_json_report(self, metrics: dict, target_name: str = "analytics_report.json") -> str:
        destination: Path = self.settings.REPORTS_DIR / target_name
        destination.parent.mkdir(parents=True, exist_ok=True)
        with open(destination, "w") as f:
            json.dump(metrics, f, indent=4)
        logger.info(f"Load Phase: Business report saved to JSON -> {destination}")
        return str(destination)

    def save_to_parquet(self, df: pd.DataFrame, target_name: str = "cleaned_ledger.parquet") -> str:
        """Saves the cleaned dataset into compressed, high-performance columnar Parquet files."""
        destination: Path = self.settings.PROCESSED_DATA_DIR / target_name
        destination.parent.mkdir(parents=True, exist_ok=True)

        # Write to disk using the pyarrow columnar compression backend engine
        df.to_parquet(destination, index=False, engine="pyarrow", compression="snappy")
        logger.info(f"Load Phase: Clean transactions saved to Parquet data lake -> {destination}")
        return str(destination)

class DatabaseLoader(FileLoader):
    def __init__(self, settings: Settings, db_connector: DatabaseConnector) -> None:
        super().__init__(settings)
        self.db = db_connector

    def load_to_postgres(self, df: pd.DataFrame, table_name: str = "transactions") -> int:
        """Inserts clean records into PostgreSQL and returns the successful record count."""
        if df.empty:
            logger.warning("Load Phase: DataFrame is empty. Skipping database insert.")
            return 0
            
        logger.info(f"Load Phase: Preparing bulk insert for {len(df)} transactions into SQL...")
        
        db_ready_df = df.copy()
        db_ready_df.columns = [
            "transaction_id", "customer_id", "transaction_type", 
            "amount", "currency", "channel", "transaction_date", "status"
        ]

        try:
            with self.db.get_session() as session:
                # Use standard Pandas bulk upload logic linked directly to your engine connection
                db_ready_df.to_sql(
                    name=table_name,
                    con=self.db.engine,
                    if_exists="append",
                    index=False,
                    method="multi",
                    chunksize=500
                )
            
            inserted_records = len(db_ready_df)
            logger.info(f"Load Phase: Successfully ingested {inserted_records} records into table '{table_name}'.")
            return inserted_records
            
        except Exception as e:
            logger.error(f"Load Phase: Database ingestion failed. Rollback triggered. Details: {str(e)}")
            raise e
