import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# =====================================================================
# STAGE 0: DATA CREATION ENVIRONMENT (Do not modify this block)
# =====================================================================
np.random.seed(42)
rows = 1000

raw_data = {
    "log_id": range(1000, 1000 + rows),
    "event_timestamp": [(datetime(2026, 7, 1) + timedelta(minutes=int(i) * 15)).strftime("%Y/%m/%d %H:%M:%S") for i in range(rows)],
    "user_identity": [f" USER_{np.random.randint(1, 50)} " if np.random.rand() > 0.05 else None for _ in range(rows)],
    "network_metric": [np.random.uniform(10.0, 500.0) if np.random.rand() > 0.08 else np.nan for _ in range(rows)],
    "operation_status": np.random.choice(["success", "SUCCESS", "failed", "FAILED", "pending"], size=rows)
}

# Inject explicit system anomalies to handle
raw_data["event_timestamp"][10] = "invalid_date_format_9999"
raw_data["event_timestamp"][50] = None

df_raw = pd.DataFrame(raw_data)
print("--- RAW INGESTED DATAFRAME DIAGNOSTICS ---")
df_raw.info()
print("\nFirst 5 Dirty Rows:")
print(df_raw.head())
print("="*60 + "\n")

# =====================================================================
# YOUR TASKS START HERE
# Build out the transformation steps below
# =====================================================================

def transform_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    # Make a distinct memory copy to prevent SettingWithCopyWarning
    df_clean = df.copy()
    
    # -----------------------------------------------------------------
    # TASK 1: Time-Series Integrity
    # Convert 'event_timestamp' to a true datetime vector.
    # Coerce errors so invalid strings become NaT (Not a Time), then drop any row missing a timestamp.
    # -----------------------------------------------------------------
    df_clean["event_timestamp"] = pd.to_datetime(df_clean["event_timestamp"], errors="coerce")
    df_clean = df_clean.dropna(subset=["event_timestamp"])
    
    # -----------------------------------------------------------------
    # TASK 2: Text Normalization
    # Strip accidental whitespace characters from 'user_identity'.
    # Standardize 'operation_status' so all strings are completely LOWERCASE.
    # Fill any remaining missing values in 'user_identity' with 'UNKNOWN_USER'.
    # -----------------------------------------------------------------
    df_clean["user_identity"] = df_clean["user_identity"].str.strip().fillna("UNKNOWN_USER")
    df_clean["operation_status"] = df_clean["operation_status"].str.lower()
    
    # -----------------------------------------------------------------
    # TASK 3: Vectorized Outlier & Null Processing
    # Fill missing values in 'network_metric' with the overall median value.
    # Create an explicit warning column named 'latency_tier' using numpy.where:
    # If network_metric > 400 -> 'CRITICAL', otherwise -> 'NORMAL'.
    # -----------------------------------------------------------------
    metric_median=df_clean["network_metric"].median()
    df_clean["network_metric"]=df_clean["network_metric"].fillna(metric_median)
    df_clean["latency_tier"]=np.where(df_clean["network_metric"]>400, "CRITICAL", "NORMAL")    
    
    # -----------------------------------------------------------------
    # TASK 4: RAM & Memory Optimization
    # Convert 'operation_status' and 'latency_tier' into 'category' data types.
    # -----------------------------------------------------------------
    df_clean["operation_status"]=df_clean["operation_status"].astype("category")
    df_clean["latency_tier"]=df_clean["latency_tier"].astype("category")


    return df_clean

# Execute your pipeline code
df_final = transform_pipeline(df_raw)

# ---------------------------------------------------------------------
# TASK 5: Aggregation Check
# After your pipeline works, group df_final by 'operation_status' and 
# calculate the average 'network_metric' and total counts per group.
# ---------------------------------------------------------------------
summary_report = df_final.groupby("operation_status", observed=False).agg(
    Avg_Latency=("network_metric", "mean"),
    Total_Logs=("log_id", "count")
).reset_index()

print("\n" + "="*20 + " FINAL PIPELINE SUMMARY " + "="*20)
print(summary_report)