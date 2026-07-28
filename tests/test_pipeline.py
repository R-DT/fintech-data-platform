import pandas as pd
import pytest

from src.config import Settings
from src.transformer import TransactionTransformer
from src.validator import TransactionValidator


@pytest.fixture
def settings():
    """Inject configuration settings."""
    return Settings()


def test_transformer_cleans_null_amounts(settings):
    validator = TransactionValidator(settings)
    transformer = TransactionTransformer(settings)

    # Shift mock dataframe schema columns to match lowercase database properties
    dirty_data = pd.DataFrame(
        {
            "transaction_id": ["TXN001"],
            "customer_id": ["CUST101"],
            "transaction_type": ["Deposit"],
            "amount": [None],
            "currency": ["USD"],
            "channel": ["Mobile App"],
            "timestamp": ["2026-01-01 10:00:00"],
            "status": ["COMPLETED"],
        }
    )

    report = validator.validate_transactions(dirty_data)
    clean_data = transformer.clean_transactions(dirty_data, report)

    # FIX: Deploy index pointer references to fetch explicit item positions
    assert clean_data["amount"].iloc[0] == 0.0
    assert len(clean_data) == 1


def test_validator_flags_unsupported_currencies(settings):
    validator = TransactionValidator(settings)

    # Shift mock dataframe schema columns to match lowercase database properties
    invalid_data = pd.DataFrame(
        {
            "transaction_id": ["TXN002"],
            "customer_id": ["CUST102"],
            "transaction_type": ["Withdrawal"],
            "amount": [150.00],
            "currency": ["XYZ"],  # Invalid currency code token
            "channel": ["ATM"],
            "timestamp": ["2026-01-01 11:00:00"],
            "status": ["COMPLETED"],
        }
    )

    report = validator.validate_transactions(invalid_data)
    # FIX: Deploy index pointer references to fetch explicit item positions
    assert report["invalid_currencies"].iloc[0] == True
