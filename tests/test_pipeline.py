import pytest
import pandas as pd
from src.config import Settings
from src.validator import TransactionValidator
from src.transformer import TransactionTransformer

@pytest.fixture
def settings():
    return Settings()

def test_transformer_cleans_null_amounts(settings):
    validator = TransactionValidator(settings)
    transformer = TransactionTransformer(settings)
    
    dirty_data = pd.DataFrame({
        "TransactionID": ["TXN001"],
        "CustomerID": ["CUST101"],
        "TransactionType": ["Deposit"],
        "Amount": [None],
        "Currency": ["NGN"],
        "Channel": ["Mobile App"],
        "Date": ["2026-01-01 10:00:00"],
        "Status": ["Successful"]
    })
    
    report = validator.validate_transactions(dirty_data)
    cleaned_df = transformer.clean_transactions(dirty_data, report)
    
    assert cleaned_df["Amount"].iloc[0] == 0.0
    assert not cleaned_df["Amount"].isnull().any()

def test_validator_flags_unsupported_currencies(settings):
    """Asserts that the validator correctly identifies unsupported currency rows."""
    validator = TransactionValidator(settings)
    
    # Ingest mock row containing an illegal currency code
    dirty_data = pd.DataFrame({
        "TransactionID": ["TXN999"],
        "CustomerID": ["CUST123"],
        "TransactionType": ["Transfer"],
        "Amount": [150.00],
        "Currency": ["GBP"],  # Invalid currency anomaly
        "Channel": ["ATM"],
        "Date": ["2026-01-02 12:00:00"],
        "Status": ["Successful"]
    })
    
    report = validator.validate_transactions(dirty_data)
    assert report["invalid_currencies"].iloc[0] == True

