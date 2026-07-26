# Fintech Data Platform 🚀

![CI Pipeline](https://github.com/R-DT/fintech-data-platform/actions/workflows/ci.yml/badge.svg)

A modular, Python-based data engineering project that simulates an enterprise fintech transaction platform.

This repository serves as a production-grade portfolio asset demonstrating robust software engineering practices, relational database warehousing, and end-to-end data pipelines.

## 🏗️ System Architecture
```text
Transaction Generator
        │
        ▼
Data Validation (Decoupled Quality Rules)
        │
        ▼
Transformation (Anomaly Cleanup & Repair)
        │
        ▼
PostgreSQL Warehouse (Relational Engine target)
        │
        ▼
Apache Spark Analytics (Distributed Aggregations)
        │
        ▼
Multiple Storage Formats (CSV, Columnar Parquet, JSON Reports)
```

## 📊 Current Status

*   ✅ **Python ETL Pipeline** - Fully operational data extraction, cleaning, and metric calculations.
*   ✅ **Data Validation** - Isolated row-level rule checks using boolean error tracking masks.
*   ✅ **Multiple Storage Options** - Parallel file generation supporting CSV, JSON, and compressed **Parquet** formats.
*   ✅ **PostgreSQL Warehousing** - Live transaction storage managed via the SQLAlchemy **Repository Pattern**.
*   ✅ **Apache Spark Analytics** - Distributed calculation code running multi-core parallel data lake aggregations.
*   ✅ **DevOps Infrastructure** - Automated environment creation via multi-stage Dockerfiles and Docker Compose.
*   ✅ **GitHub Actions CI/CD** - Cloud testing pipelines tracking code quality, style guides, and tests on every push.
*   🚧 **Apache Airflow Orchestration** - Structuring multi-stage workflow DAG scheduling configurations (Active Sprint).
*   🚧 **AWS Data Lake Deployment** - Integrating cloud bucket storage drivers using `boto3`.

## 🏗️ Project Structure

```text
fintech-data-platform/
├── .github/workflows/ci.yml # GitHub Actions linting, type-checking, and test workflows
├── airflow/dags/            # Apache Airflow orchestration workflow scheduling DAGs
├── data/                    # High-performance local storage data lake folders (CSV/Parquet)
├── docker/                  # Virtualization layouts (Dockerfile, docker-compose.yml)
├── docs/                    # Development blueprints and technical system design manuals
├── sql/                     # Warehouse tables, constraints, lookup indexes, and metrics views
├── src/                     # Core processing engine package source files
│   ├── analytics/           # Spark distributed computing application code modules
│   └── ...                  # ETL logic, repositories, validators, and connectors
└── tests/                   # Automated regression unit and integration verification suites
```

## ⚡ Quickstart

### 1. Environment Activation
Ensure you are inside your local environment context before installing package requirements:
```bash
# Activate environment (Windows PowerShell)
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& .\.venv\Scripts\Activate.ps1)

# Install pinned dependencies and register your custom system CLI
pip install -r requirements.txt
pip install -e .
```

### 2. Launch Local Database Cluster Services
Ensure Docker Desktop is active on your machine, then spin up your background warehouse container:
```bash
./scripts/deploy.ps1
```

### 3. Run the Data Ingestion Pipeline
Execute the complete workflow natively from anywhere via the custom CLI:
```bash
fintech-platform
```
