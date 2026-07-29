import logging
from collections.abc import Sequence
from typing import Any

from sqlalchemy.dialects.postgresql import insert

from src.database import DatabaseConnector
from src.models import Transaction

logger = logging.getLogger("delta_loader")


class IdempotentDeltaIngestionEngine:
    """Manages high-throughput incremental delta loading with atomic upsert guarantees."""

    def __init__(self, db_connector: DatabaseConnector) -> None:
        self.db_connector = db_connector

    def get_latest_transaction_watermark(self) -> Any:
        """Fetches the high-watermark timestamp directly from the live database instance."""
        with self.db_connector.get_session() as session:
            from sqlalchemy import func

            max_timestamp = session.query(func.max(Transaction.timestamp)).scalar()
            logger.info(
                f"Retrieved incremental loading high-watermark: {max_timestamp}"
            )
            return max_timestamp

    # FIX: Use Sequence[Dict[Any, Any]] to satisfy invariance constraints across dataframe record dictionary maps
    def upsert_transaction_delta_batch(
        self, transaction_records: Sequence[dict[Any, Any]]
    ) -> bool:
        """Executes an idempotent Postgres ON CONFLICT UPSERT boundary scan loop."""
        if not transaction_records:
            logger.info(
                "Incremental Load: No new data records found above watermark. Skipping upload."
            )
            return True

        try:
            with self.db_connector.get_session() as session:
                logger.info(
                    f"Staging incremental delta block containing {len(transaction_records)} entries..."
                )

                for record in transaction_records:
                    # Construct an native PostgreSQL upsert query statement
                    stmt = insert(Transaction).values(record)
                    upsert_stmt = stmt.on_conflict_do_update(
                        index_elements=["transaction_id"],
                        set_={
                            "amount": stmt.excluded.amount,
                            "currency": stmt.excluded.currency,
                            "status": stmt.excluded.status,
                            "timestamp": stmt.excluded.timestamp,
                        },
                    )
                    session.execute(upsert_stmt)

                session.commit()
                logger.info("Idempotent incremental delta load completed successfully.")
                return True
        except Exception as err:  # noqa: BLE001
            logger.error(
                f"Critical failure during delta loading operation boundaries: {err!s}"
            )
            return False
