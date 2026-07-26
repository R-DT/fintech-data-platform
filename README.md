# Fintech Data Platform 🚀

![CI Pipeline](https://github.com)

A modular, Python-based data engineering project that simulates a fintech transaction platform.

This platform serves as a production-ready portfolio asset demonstrating modern data architecture, clean code principles, and end-to-end data pipelines.

## 🏗️ System Data Flow
```text
Transaction Generator
        │
        ▼
Data Validation (Decoupled Rules)
        │
        ▼
Transformation (Anomaly Cleanup)
        │
        ▼
PostgreSQL Warehouse (SQL Storage)
        │
        ▼
Apache Spark Analytics (Big Data Aggregations)
        │
        ▼
Multiple Storage Formats (CSV, Parquet, JSON Reports)
```

## 🛠️ Features Demonstrated

*   **Transaction Generation**: Simulates a live banking ledger with realistic missing values and timestamp anomalies.
*   **Data Validation**: Separates validation rules from transformation logic to evaluate record health.
*   **ETL Processing**: Extracts raw files, auto-repairs missing numbers, and filters records using validation masks.
*   **Multiple Storage Options**: Saves output datasets to CSV, compressed binary Parquet formats, and SQL databases.
*   **SQL Optimization**: Configures tables, explicit constraints, lookup acceleration indexes, and summary views natively on the database server.
*   **Apache Spark Analytics**: Processes parallel dataset transformations and metrics calculations.
*   **Orchestration & Infrastructure**: Automates workflow triggers, container networks, and task error parameters via Airflow and Docker.

## 🏗️ Project Structure

```text
fintech-data-platform/
├── .github/workflows/ci.yml # Automated testing runner workflow blueprint
├── data/                    # Local storage volumes for raw and processed datasets
├── docker/                  # Environment orchestration layers (Docker Compose, Dockerfile)
├── docs/                    # Design manuals and architectural trade-off logs
├── scripts/                 # Airflow DAG schedules, Spark scripts, and deployers
├── sql/                     # Structured schemas, indexes, views, and ad-hoc queries
├── src/                     # Core processing engine source code package modules
└── tests/                   # Automated regression verification test suites
```

## ⚡ Quickstart

### 1. Environment Setup
Activate your isolated virtual environment and install the required dependencies:
```bash
# Windows PowerShell
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& .\.venv\Scripts\Activate.ps1)

# Install packages
pip install -r requirements.txt
pip install -e .
```

### 2. Run the Data Pipeline
Execute the complete ETL workflow natively via the custom CLI:
```bash
fintech-platform
```
