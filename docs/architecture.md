# Fintech Data Platform - System Architecture Manual

This document details the architectural choices, engineering trade-offs, and design patterns implemented across the Fintech Data Platform.

## 🏗️ Architectural Core Patterns

### 1. Decoupled Processing Pipeline (ETL)
The platform avoids monolithic scripting by enforcing a strict functional separation of duties across the data lifecycle:
*   **Ingestion (`extractor.py`)**: Abstracted file system reading utilizing structural error-boundary protection.
*   **Audit (`validator.py`)**: Programmable row-level data quality rule checking isolated from business logic.
*   **Repair (`transformer.py`)**: Structural recovery vector executing vector-cleaning and index-safe row filtering based on validation masks.
*   **Computation (`analyzer.py`)**: Memory-efficient performance KPI profiling.
*   **Persistence (`loader.py`)**: Polymorphic, multi-destination target interface layer.

### 2. Dependency Injection Lifecycle
To maximize testability and eliminate hardcoded environment bindings, no component instantiates its own dependencies. The orchestrator (`main.py`) acts as the IoC container, injecting a centralized `Settings` instance and a `DatabaseConnector` instance down into the data workers.

### 3. Polymorphic Persistence Layer
The loader utilizes class inheritance (`DatabaseLoader` inheriting from `FileLoader`) to support extensible multi-destination persistence strategies. The system routes clean data streams into local files (CSV), highly optimized compressed columnar formats (Parquet), local database tables (PostgreSQL), and cloud object storage (AWS S3) simultaneously via a unified interface.

## 💾 Relational Data Warehouse Layer

### 1. Schema Enforcement & Check Constraints
The PostgreSQL storage layer implements strict relational data definitions (DDL) inside `sql/schema.sql`. High financial data integrity is guaranteed natively on the database server through explicit numeric scaling bounds (`NUMERIC(15, 2)`) and domain state validation checks (`CHECK (currency IN ('NGN', 'USD', 'EUR'))`).

### 2. Computational Pushdown (SQL Views)
To preserve application server memory (Pandas), large-scale metric aggregations are pushed down directly to the relational engine. Permanent summary views (`view_transaction_summary`, `view_channel_velocity`) leverage the database catalyst optimizations natively.

### 3. Storage Optimization & Indexes
High-velocity query lookup paths are indexed (`sql/indexes.sql`) across the primary tracking keys (`customer_id`, `transaction_date`, `status`) to avoid costly sequential table scans as the warehouse database scales.

## ⚙️ Infrastructure & Automated CI/CD

### 1. Multi-Stage Docker Container Virtualization
The application `Dockerfile` utilizes a two-stage compilation pattern:
*   **Stage 1 (`builder`)**: Ingests system-level build tools and compiles dense database driver binaries.
*   **Stage 2 (`runner`)**: Copies *only* the compiled dependencies and source modules into a minimal Python runtime footprint, reducing the final image surface area and attack vector.

### 2. Self-Healing Multi-Service Orchestration
The multi-container stack (`docker-compose.yml`) leverages a container healthcheck loop (`pg_isready`). The application container waits passively for the database container to achieve a fully healthy, operational state before running the ETL code, eliminating container race conditions.

### 3. Automated Regression Verification (CI)
A headless GitHub Actions runner (`.github/workflows/ci.yml`) mimics production deployments by standing up a live, isolated container database instance, installing pinned local dependencies, and executing automated unit testing verification check matrices on every commit loop.
