# Fintech Data Platform - System Architecture Manual

This document details the architectural choices, engineering trade-offs, and design patterns implemented across the Fintech Data Platform.

## 🏗️ Core Design Patterns

### 1. Decoupled Ingestion Pipeline (ETL)
The platform avoids monolithic processing by enforcing a strict separation of concerns across the data lifecycle: Extract ➔ Validate ➔ Transform ➔ Load.

### 2. Dependency Injection
No worker module instantiates its own infrastructure connections. The orchestrator (`main.py`) acts as the IoC container, injecting a centralized `Settings` instance and a thread-safe `DatabaseConnector` connection pool down into your data processing workers.

### 3. Repository Pattern
Relational operations are entirely decoupled from business transformation logic. The system uses a dedicated `TransactionRepository` class to handle bulk insertions (`chunksize=500`) and enforce atomicity with secure database transaction rollbacks.
