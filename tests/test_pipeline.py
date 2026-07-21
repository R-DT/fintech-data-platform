import sys
import os
import pytest
import pandas as pd

# Clear the relative path append lines and import natively
from src.transformer import TransactionTransformer

def test_transformer_cleans_null_amounts():
    """Asserts that missing currency amounts are successfully replaced with 0.0."""
    transformer = TransactionTransformer()
    
    # 1. Create a dummy dataframe with an explicit null amount anomaly
    dirty_data = pd.DataFrame({
        "TransactionID": ["TXN001"],
        "CustomerID": ["CUST101"],
        "TransactionType": ["Deposit"],
        "Amount": [None],  # Null value anomaly
        "Currency": ["NGN"],
        "Channel": ["Mobile App"],
        "Date": ["2026-01-01 10:00:00"],
        "Status": ["Successful"]
    })
    
    # 2. Pass through processing
    cleaned_df = transformer.clean(dirty_data)
    
    # 3. Assert target repairs took place
    assert cleaned_df["Amount"].iloc[0] == 0.0
    assert not cleaned_df["Amount"].isnull().any()

def test_transformer_drops_corrupt_dates():
    """Asserts that unparseable transaction date rows are dropped safely from the batch."""
    transformer = TransactionTransformer()
    
    dirty_data = pd.DataFrame({
        "TransactionID": ["TXN001", "TXN002"],
        "CustomerID": ["CUST101", "CUST102"],
        "TransactionType": ["Deposit", "Withdrawal"],
        "Amount": [500.0, 200.0],
        "Currency": ["NGN", "NGN"],
        "Channel": ["Mobile App", "POS Terminal"],
        "Date": ["2026-01-01 10:00:00", "CORRUPT_DATETIME_STRING"],  # Row 2 is broken
        "Status": ["Successful", "Failed"]
    })
    
    cleaned_df = transformer.clean(dirty_data)
    
    # Assert the corrupt row was deleted and the healthy row survives
    assert len(cleaned_df) == 1
    assert cleaned_df["TransactionID"].iloc[0] == "TXN001"
