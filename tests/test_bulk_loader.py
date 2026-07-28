import unittest
from unittest.mock import MagicMock

from sqlalchemy.exc import SQLAlchemyError

from src.bulk_loader import BulkDataIngestionEngine


class TestBulkDataIngestionEngine(unittest.TestCase):
    def setUp(self) -> None:
        """Initialize mock target context variables for bulk ingestion tracks."""
        self.mock_connector = MagicMock()
        self.mock_session = MagicMock()

        # Wire the connector context manager to return our mock session object
        self.mock_connector.get_session.return_value.__enter__.return_value = (
            self.mock_session
        )
        self.engine = BulkDataIngestionEngine(self.mock_connector)

        # Build basic mock payloads for processing evaluations
        self.sample_dataset = {
            "customers": [{"customer_id": "c1", "first_name": "Test"}],
            "accounts": [{"account_id": "a1", "customer_id": "c1"}],
            "merchants": [{"merchant_id": "m1", "name": "Vendor"}],
            "transactions": [{"transaction_id": "t1", "amount": 10.00}],
        }

    def test_bulk_ingest_success_commits_transaction(self) -> None:
        """Verify that a flawless database write sequence executes an explicit commit."""
        result = self.engine.ingest_batch_dataset(self.sample_dataset)

        self.assertTrue(result)
        self.assertEqual(self.mock_session.execute.call_count, 4)
        self.mock_session.commit.assert_called_once()

    def test_bulk_ingest_failure_triggers_atomic_rollback(self) -> None:
        """Verify that an unexpected exception during table loads prevents commits."""
        # Force a database execution error during transaction insertions
        self.mock_session.execute.side_effect = SQLAlchemyError(
            "Mock constraint violation failure"
        )

        result = self.engine.ingest_batch_dataset(self.sample_dataset)

        self.assertFalse(result)
        self.mock_session.commit.assert_not_called()
        # Context manager automatically handles underlying block rollbacks or closures cleanly


if __name__ == "__main__":
    unittest.main()
