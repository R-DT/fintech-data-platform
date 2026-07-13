# Data Engineering Bootcamp - API Extraction Pipeline

A robust, isolated Python ETL pipeline that extracts structured post payloads from a REST API, parses the data into structured Pandas DataFrames, and preserves archival states using dynamic temporal file naming schemas.

## Features
- **Environment Isolation:** Complete structural containment using local Python virtual environments (`.venv`).
- **Resilient Network Layer:** Configured transport tier error catching (`requests.RequestException`) with connection drop and timeout monitoring.
- **Dynamic File Archiving:** Generates timestamped data dumps (`api_data_YYYY-MM-DD.csv`) to retain analytical run history.
- **Structured Operations Logging:** Integrates Python's native `logging` module to surface execution contexts over fragile standard print flags.

## Project Structure
```text
VMpy/
├── .gitignore              # Protects repository from bloated .venv traces
├── main.py                 # Core production extraction script
├── requirements.txt        # Isolated environment dependency footprint
└── api_data_YYYY-MM-DD.csv # Temporal target dataset output
```

## Setup & Execution

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd data-engineering-bootcamp/VMpy
   ```

2. **Spin up your local container environment:**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install exact structural package variants:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Trigger pipeline execution:**
   ```bash
   python main.py
   ```
