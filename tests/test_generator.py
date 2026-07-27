import unittest
import uuid

from src.generator import NormalizedDataGenerator


class TestNormalizedDataGenerator(unittest.TestCase):
    def setUp(self) -> None:
        """Initialize generator system for tracking integrity metrics."""
        self.generator = NormalizedDataGenerator()
        self.customer_count = 10
        self.merchant_count = 5
        self.transaction_count = 50

        self.dataset = self.generator.generate_batch_dataset(
            customer_count=self.customer_count,
            merchant_count=self.merchant_count,
            transaction_count=self.transaction_count,
        )

    def test_dataset_contains_all_target_tables(self) -> None:
        """Assert dataset structural surface matches target entities."""
        expected_keys = {"customers", "accounts", "merchants", "transactions"}
        self.assertTrue(expected_keys.issubset(self.dataset.keys()))

    def test_relational_link_integrity(self) -> None:
        """Verify cross-table key connections resolve to real generated entities."""
        customer_ids = {c["customer_id"] for c in self.dataset["customers"]}
        account_ids = {a["account_id"] for a in self.dataset["accounts"]}
        merchant_ids = {m["merchant_id"] for m in self.dataset["merchants"]}

        # 1. Assert accounts belong to valid customers
        for account in self.dataset["accounts"]:
            self.assertIn(account["customer_id"], customer_ids)
            self.assertIsInstance(account["account_id"], uuid.UUID)

        # 2. Assert transactions map strictly to existing accounts and merchants
        for tx in self.dataset["transactions"]:
            self.assertIn(tx["account_id"], account_ids)
            self.assertIn(tx["merchant_id"], merchant_ids)
            self.assertIsInstance(tx["transaction_id"], uuid.UUID)

    def test_currency_alignment_invariant(self) -> None:
        """Validate transaction record currency matches its parent ledger origin."""
        account_currency_map = {
            a["account_id"]: a["currency"] for a in self.dataset["accounts"]
        }

        for tx in self.dataset["transactions"]:
            parent_account_currency = account_currency_map[tx["account_id"]]
            self.assertEqual(tx["currency"], parent_account_currency)


if __name__ == "__main__":
    unittest.main()
