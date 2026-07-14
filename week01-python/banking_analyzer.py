import os
import logging
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# Configure structured logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def generate_mock_transactions(output_path: str, count: int = 800):
    """Generates 500-1,000 simulated transactions with built-in data noise."""
    logging.info(f"Generating {count} simulated banking transactions...")
    np.random.seed(42)
    
    channels = ["Mobile App", "Web Portal", "POS Terminal", "ATM", "USSD"]
    types = ["Deposit", "Withdrawal", "Transfer", "Bill Payment"]
    statuses = ["Successful", "Successful", "Successful", "Failed", "Pending"]
    currencies = ["NGN", "USD", "EUR"]
    
    start_date = datetime(2026, 1, 1)
    
    data = {
        "TransactionID": [f"TXN{str(i).zfill(6)}" for i in range(1, count + 1)],
        "CustomerID": [f"CUST{str(np.random.randint(100, 150))}" for _ in range(count)],
        "CustomerName": [f"Customer_{i[-3:]}" for i in [f"CUST{str(np.random.randint(100, 150))}" for _ in range(count)]],
        "TransactionType": np.random.choice(types, size=count),
        "Amount": np.round(np.random.uniform(5.0, 1500.0, size=count), 2),
        "Currency": np.random.choice(currencies, size=count, p=[0.8, 0.1, 0.1]),
        "Channel": np.random.choice(channels, size=count),
        "Date": [(start_date + timedelta(days=int(np.random.randint(0, 180)), hours=int(np.random.randint(0, 24)))).strftime("%Y-%m-%d %H:%M:%S") for _ in range(count)],
        "Status": np.random.choice(statuses, size=count)
    }
    
    df = pd.DataFrame(data)
    
    # Inject dirty data structures for testing
    df.loc[np.random.choice(df.index, size=15, replace=False), "Amount"] = np.nan
    df.loc[np.random.choice(df.index, size=10, replace=False), "Date"] = "CORRUPT_TIMESTAMP_DATA"
    df.loc[np.random.choice(df.index, size=12, replace=False), "CustomerID"] = None
    
    df.to_csv(output_path, index=False)
    logging.info(f"Raw landing file generated successfully at: {output_path}")

def run_etl_pipeline(input_path: str):
    """Executes the core Ingest, Validate, Transform, Aggregate, and Publish cycle."""
    logging.info("Initializing ETL Pipeline Engine...")
    
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Source file target missing: {input_path}")
        
    # STAGE 1: INGESTION
    df = pd.read_csv(input_path)
    
    # STAGE 2: VALIDATION & TRANSFORMATION
    logging.info("Validating schema fields and enforcing type integrity...")
    
    # Convert dates and isolate invalid formats
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    initial_count = len(df)
    
    # Drop rows missing critical architectural keys
    df = df.dropna(subset=["TransactionID", "CustomerID", "Date"])
    
    # Handle numerical null missing values using column median metrics
    amount_median = df["Amount"].median()
    df["Amount"] = df["Amount"].fillna(amount_median)
    
    # Standardize string categories
    df["Status"] = df["Status"].str.strip().str.capitalize()
    df["Channel"] = df["Channel"].str.strip()
    
    logging.info(f"Validation complete. Purged {initial_count - len(df)} corrupt log lines.")
    
    # STAGE 3: AGGREGATION & METRICS COMPUTATION
    logging.info("Running pipeline analytical metrics computations...")
    
    total_val = df["Amount"].sum()
    avg_val = df["Amount"].mean()
    max_val = df["Amount"].max()
    min_val = df["Amount"].min()
    
    status_counts = df["Status"].value_counts()
    success_count = status_counts.get("Successful", 0)
    failed_count = status_counts.get("Failed", 0)
    
    # Dimensional timelines profiles
    df["Day"] = df["Date"].dt.to_period("D")
    df["Month"] = df["Date"].dt.to_period("M")
    
    daily_totals = df.groupby("Day")["Amount"].sum().reset_index()
    monthly_totals = df.groupby("Month")["Amount"].sum().reset_index()
    
    # Categorical segments profiles
    top_customers = df.groupby(["CustomerID", "CustomerName"])["Amount"].sum().reset_index()
    top_10_customers = top_customers.sort_values(by="Amount", ascending=False).head(10)
    
    channel_totals = df.groupby("Channel")["Amount"].sum().reset_index()
    
    # STAGE 4: OUTPUT PUBLISHING
    logging.info("Exporting analytical data products...")
    
    # Export cleaned dataset
    df.drop(columns=["Day", "Month"]).to_csv("clean_transactions.csv", index=False)
    
    # Generate structural summary artifact
    with open("summary.csv", "w") as f:
        f.write("Metric,Value\n")
        f.write(f"Total Transaction Value,{total_val:.2f}\n")
        f.write(f"Average Transaction Value,{avg_val:.2f}\n")
        f.write(f"Largest Transaction,{max_val:.2f}\n")
        f.write(f"Smallest Transaction,{min_val:.2f}\n")
        f.write(f"Successful Transactions Count,{success_count}\n")
        f.write(f"Failed Transactions Count,{failed_count}\n")
    
    # Append structured channel breakdowns to summary file
    channel_totals.rename(columns={"Channel": "Metric", "Amount": "Value"}).to_csv("summary.csv", mode="a", index=False)
    
    # PRINT CONSOLE REPORT
    print("\n" + "="*20 + " MONIEPOINT BANKING ANALYSIS REPORT " + "="*20)
    print(f"Total Transaction Volume processed: {total_val:,.2f} NGN Equivalent")
    print(f"Average Transaction Size          : {avg_val:,.2f} NGN")
    print(f"Maximum Single Transaction Value  : {max_val:,.2f} NGN")
    print(f"Minimum Single Transaction Value  : {min_val:,.2f} NGN")
    print(f"Successful Processing Signals      : {success_count} jobs")
    print(f"Failed Processing Signals          : {failed_count} jobs")
    print("\n--- TOP 5 CUSTOMERS BY VALUE ---")
    print(top_10_customers.head(5).to_string(index=False))
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    raw_csv_target = "raw_moniepoint_transactions.csv"
    generate_mock_transactions(raw_csv_target, count=850)
    run_etl_pipeline(raw_csv_target)
    
