import logging

import pandas as pd

from src.database import DatabaseConnector

logger = logging.getLogger(__name__)


class TransactionRepository:
    """Encapsulates all relational warehouse storage writes and query operations."""

    def __init__(self, db: DatabaseConnector) -> None:
        self.db = db

    def bulk_insert_transactions(
        self, df: pd.DataFrame, table_name: str = "transactions"
    ) -> int:
        """Executes a high-velocity bulk insert transaction block."""
        if df.empty:
            logger.warning("Repository Context: DataFrame is empty. Ingestion skipped.")
            return 0

        # Map Pandas headers to target SQL schema column mappings
        db_ready_df = df.copy()
        db_ready_df.columns = [
            "transaction_id",
            "customer_id",
            "transaction_type",
            "amount",
            "currency",
            "channel",
            "transaction_date",
            "status",
        ]

        logger.info(
            f"Repository Context: Committing bulk insert transaction for {len(db_ready_df)} records..."
        )

        # Access the context manager to open a secure atomic session with rollback protection
        with self.db.get_session() as _session:
            db_ready_df.to_sql(
                name=table_name,
                con=self.db.engine,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=500,
            )

        inserted_count = len(db_ready_df)
        logger.info(
            f"Repository Context: Successfully committed transaction batch. Ingested rows: {inserted_count}"
        )
        return inserted_count
