# Fintech Data Platform 🚀

![CI Pipeline](https://github.com)

A modular, Python-based data engineering project that simulates an enterprise fintech transaction platform. 

This repository serves as a production-ready portfolio asset demonstrating modern data architecture, clean software principles, and end-to-end multi-destination data asset pipelines.

## 🛠️ Features Demonstrated

*   **Transaction Generation**: Simulates a live banking ledger with realistic missing values and timestamp anomalies.
*   **Data Validation**: Decouples data quality rule checks inside a standalone validation auditing layer.
*   **ETL Processing**: Extracts raw files, auto-repairs missing numbers, and filters records using validation masks.
*   **Polymorphic Persistence**: Streams data assets to local CSV files, compressed binary **Parquet** files, relational tables, and cloud targets via a unified interface.
*   **PostgreSQL Warehousing**: Deploys structured table definitions, strict integrity constraints, optimization indexes, and permanent summary views natively on the database server.
*   **Distributed Big Data Analytics**: Spins up isolated local **Apache PySpark** clusters to crunch large-scale payment channel aggregations over high-volume data lake layers.
*   **Orchestration & Virtualization**: Schedules daily ingestion tasks, handles network errors, and tracks step retries using automated **Apache Airflow** DAGs and containerized **Docker Compose** networks.
*   **Production DevOps Pipeline**: Enforces strict Pylance type checking, runs automated mock testing matrices, and executes a headless **GitHub Actions CI/CD** virtual server test runner on every single push.

## 🏗️ Project Structure

```text
fintech-data-platform/
├── .github/workflows/      # Automated DevOps cloud infrastructure configurations
│   └── ci.yml              # GitHub Actions continuous integration server pipeline
├── .env.example            # Configuration blueprint template for local database credentials
├── pyproject.toml          # Package metadata, package discovery, and custom CLI script bindings
├── requirements.txt        # Pinned project library dependencies
├── LICENSE                 # Project open-source MIT license
├── README.md               # Quickstart manual and architecture overview
├── data/                   # High-performance local file storage data layers
│   ├── raw/                # Ingested mock transactions containing anomalies
│   ├── processed/          # Clean, schema-enforced CSV and compressed Parquet records
│   └── reports/            # Exported business KPI summaries and PySpark analytics logs
├── docs/                   # Development guides, technical briefs, and design manuals
│   ├── architecture.md     # System-wide design choices and architectural trade-off logs
│   └── roadmap.md          # Technical sprint progression maps
├── notebooks/              # Big data computation scripts
│   └── spark_analytics.py  # Local Apache PySpark distributed processing matrix
├── scripts/                # Infrastructure automation and workflow orchestration tracks
│   ├── deploy.ps1          # One-click environment manager and container build script
│   └── platform_dag.py     # Automated Airflow scheduling DAG using DockerOperators
├── sql/                    # Relational warehouse target layers
│   ├── schema.sql          # Core transactional tables and server-side check constraints
│   ├── indexes.sql         # High-velocity query lookup acceleration indexes
│   ├── views.sql           # Permanent SQL reporting queries and computational pushdown models
│   └── queries.sql         # Ad-hoc analytics query scripts inventory
├── src/                    # Pipeline Core Processing Engine source code
│   ├── config.py           # Application settings, system directory mappings, and type-safe Enums
│   ├── logger.py           # Centralized naming-context logging stream utility
│   ├── main.py             # Global execution orchestrator and argparse command-line interface
│   ├── generator.py        # Generates synthetic banking records using NumPy's RNG API
│   ├── extractor.py        # Safe ingestion step protecting file system error boundaries
│   ├── validator.py        # Checks records against row-level data quality rules
│   ├── transformer.py      # Executes data repairs and schema filtering from validation masks
│   ├── analyzer.py         # Computes core transactional performance statistics
│   ├── database.py         # Manages SQLAlchemy connection pooling and safe transaction sessions
│   └── loader.py           # Polymorphic writer handling multi-destination persistence paths
└── tests/                  # Automated quality testing suites
    ├── test_pipeline.py    # Unit validation checks for transformer repair functions
    └── test_database.py    # Mock integration tests verifying connection handshakes and rollbacks
```

## ⚡ Quickstart

### 1. Environment Initialization
Ensure you are inside your local virtual environment context before installing your dependencies:
```bash
# Activate your environment (Windows PowerShell)
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& .\.venv\Scripts\Activate.ps1)

# Clean install pinned requirements and register local CLI tool paths
pip install -r requirements.txt
pip install -e .
```

### 2. Launch Local Database Services
Ensure Docker Desktop is active on your machine, then spin up your background database container cluster using the one-click automation deployer:
```bash
./scripts/deploy.ps1
```

### 3. Execute the Processing Pipeline
Run the global workflow end-to-end natively via your newly installed custom CLI tool name:
```bash
fintech-platform
```

### 4. Execute Distributed Big Data Reports
Trigger your local Apache PySpark cluster to compute channel performance analytics over your Parquet data lake layer:
```bash
python notebooks/spark_analytics.py
```

### 5. Run Automated Testing Frameworks
Run your unit and integration test assertion suites locally to check for code regressions:
```bash
fintech-platform -m pytest
```
