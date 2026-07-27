import random
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any


class NormalizedDataGenerator:
    """Generates synthetic, highly correlated relational fintech datasets."""

    def __init__(self) -> None:
        self.currencies = ["USD", "EUR", "GBP", "CAD", "AUD"]
        self.account_types = ["CHECKING", "SAVINGS", "CREDIT"]
        self.merchant_categories = {
            "Walmart": "GROCERY",
            "Amazon": "RETAIL",
            "Netflix": "ENTERTAINMENT",
            "Exxon": "GAS_STATION",
            "Starbucks": "RESTAURANT",
        }

    def generate_batch_dataset(
        self, customer_count: int, merchant_count: int, transaction_count: int
    ) -> dict[str, list[dict[str, Any]]]:
        """Generates cross-linked dictionary datasets for relational loading."""

        # 1. Generate Static Customers
        customers: list[dict[str, Any]] = []
        for i in range(customer_count):
            c_id = uuid.uuid4()
            customers.append(
                {
                    "customer_id": c_id,
                    "first_name": f"User_{i}",
                    "last_name": f"Surname_{i}",
                    "email": f"user_{i}_{uuid.uuid4().hex[:6]}@fintechplatform.io",
                    "created_at": datetime.now(timezone.utc)
                    - timedelta(days=random.randint(30, 365)),
                }
            )

        # 2. Generate Accounts Linked to Customers
        accounts: list[dict[str, Any]] = []
        for customer in customers:
            # Assign 1 to 2 accounts per customer
            for _ in range(random.randint(1, 2)):
                accounts.append(
                    {
                        "account_id": uuid.uuid4(),
                        "customer_id": customer["customer_id"],
                        "account_number": f"IBAN{random.randint(1000000000000000, 9999999999999999)}",
                        "account_type": random.choice(self.account_types),
                        "balance": round(random.uniform(500.00, 25000.00), 2),
                        "currency": random.choice(self.currencies),
                        "created_at": customer["created_at"]
                        + timedelta(days=random.randint(1, 10)),
                    }
                )

        # 3. Generate Static Merchants
        merchants: list[dict[str, Any]] = []
        merchant_names = list(self.merchant_categories.keys())
        for i in range(merchant_count):
            name = merchant_names[i % len(merchant_names)]
            merchants.append(
                {
                    "merchant_id": uuid.uuid4(),
                    "name": f"{name} #{random.randint(100, 999)}",
                    "category": self.merchant_categories[name],
                    "created_at": datetime.now(timezone.utc) - timedelta(days=365),
                }
            )

        # 4. Generate Core Transactions Linking Accounts & Merchants
        transactions: list[dict[str, Any]] = []
        start_time = datetime.now(timezone.utc) - timedelta(days=14)

        for _ in range(transaction_count):
            account = random.choice(accounts)
            merchant = random.choice(merchants)

            transactions.append(
                {
                    "transaction_id": uuid.uuid4(),
                    "account_id": account["account_id"],
                    "merchant_id": merchant["merchant_id"],
                    "amount": round(random.uniform(5.00, 1200.00), 2),
                    "currency": account[
                        "currency"
                    ],  # Enforce transaction matches account ledger currency
                    "status": random.choice(
                        ["COMPLETED", "COMPLETED", "COMPLETED", "PENDING", "DECLINED"]
                    ),
                    "timestamp": start_time
                    + timedelta(seconds=random.randint(0, 1209600)),
                }
            )

        return {
            "customers": customers,
            "accounts": accounts,
            "merchants": merchants,
            "transactions": transactions,
        }
