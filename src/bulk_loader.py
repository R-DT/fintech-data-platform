import logging
from typing import Any

from sqlalchemy import insert

from src.database import DatabaseConnector
from src.models import Account, Customer, Merchant, Transaction

logger = logging.getLogger("bulk_loader")


class BulkDataIngestionEngine:
    """Orchestrates high-throughput relational data bulk loading with transactional safety."""

    def __init__(self, db_connector: DatabaseConnector) -> None:
        self.db_connector = db_connector

    def ingest_batch_dataset(self, dataset: dict[str, list[dict[str, Any]]]) -> bool:
        """Loads a normalized dataset batch into Postgres with strict rollback containment."""
        logger.info("Initializing atomic transaction boundary for bulk data load...")

        # FIX: Deploy a 'with' context statement to unpack the Generator Context Manager safely
        try:
            with self.db_connector.get_session() as session:
                # 1. Bulk Load Customers
                if dataset.get("customers"):
                    logger.info(
                        f"Staging {len(dataset['customers'])} customer records..."
                    )
                    session.execute(insert(Customer), dataset["customers"])

                # 2. Bulk Load Accounts
                if dataset.get("accounts"):
                    logger.info(
                        f"Staging {len(dataset['accounts'])} financial account records..."
                    )
                    session.execute(insert(Account), dataset["accounts"])

                # 3. Bulk Load Merchants
                if dataset.get("merchants"):
                    logger.info(
                        f"Staging {len(dataset['merchants'])} merchant identity records..."
                    )
                    session.execute(insert(Merchant), dataset["merchants"])

                # 4. Bulk Load Core Fact Transactions
                if dataset.get("transactions"):
                    logger.info(
                        f"Staging {len(dataset['transactions'])} core financial transaction rows..."
                    )
                    session.execute(insert(Transaction), dataset["transactions"])

                # Commit the atomic batch if all operations succeed
                session.commit()
                logger.info(
                    "Atomic batch upload completed successfully. Changes persisted."
                )
                return True

        except Exception as err: #  noqa: BLE001
            # Catch failures, trigger rollbacks, and isolate corruptions
            logger.error(
                f"Critical failure during bulk processing boundary. Transaction rolled back safely: {err!s}"
            )
            return False
