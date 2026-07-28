# 📊 Performance Benchmark Report: SQL vs. Pandas
Generated on: 2026-07-28 17:32:24

This report documents the speed differences between processing complex fintech analytics inside our relational engine vs pulling raw datasets into application memory via Pandas.

## ⏱️ Execution Latency Profiles

| Ingestion Engine / Architecture | Average Retrieval Delay (ms) | Speed Factor |
| :--- | :--- | :--- |
| **PostgreSQL Native Aggregation** | 72.29 ms | **1.0x (Baseline)** |
| **In-Memory Pandas Dataframe** | 506.89 ms | 7.0x slower |

## 💡 Engineering Insights
1. **Network Overlap & Memory Bloat:** Pandas requires pulling *every single row* over the network boundary into application memory before filtering. SQL executes selections straight on the data blocks.
2. **Optimizer Execution Plans:** PostgreSQL leverages internal indexing (`idx_transactions_timestamp`) and parallel bitmap heap scans to achieve minimal operational latencies.
3. **Scale Invariant Limitations:** While Pandas is highly interactive for sub-10,000 row data processing tracks, processing enterprise scale records on data infrastructure layers requires pushing logic downwards to native database kernels.
