import argparse
import sys

import pandas as pd
import pytest

from src.analyzer import TransactionAnalyzer
from src.bulk_loader import BulkDataIngestionEngine
from src.config import Settings
from src.database import DatabaseConnector
from src.delta_loader import (
    IdempotentDeltaIngestionEngine,  # type: ignore[import-not-found]
)
from src.generator import NormalizedDataGenerator
from src.loader import DatabaseLoader
from src.logger import setup_logger
from src.models import Base
from src.quality_tracker import (
    AdvancedDataQualityTracker,  # type: ignore[import-not-found]
)
from src.repository import TransactionRepository
from src.transformer import TransactionTransformer
from src.validator import TransactionValidator

logger = setup_logger("pipeline_orchestrator")


def run_platform_pipeline() -> None:
    """Hardened execution lifecycle engine controlling Sprint 3 production targets."""
    parser = argparse.ArgumentParser(description="Fintech Engine Core CLI.")
    parser.add_argument(
        "-m", "--mode", type=str, default="run", choices=["run", "pytest"]
    )
    args = parser.parse_args()

    if args.mode == "pytest":
        logger.info("=== INITIALIZING PLATFORM AUTOMATED TEST RUNNER ===")
        sys.exit(pytest.main(["tests"]))

    logger.info("=== STARTING FINTECH DATA PLATFORM PIPELINE ===")
    try:
        # 1. Multi-Environment Configuration Bindings
        settings = Settings()
        logger.info(f"Active Runtime Execution Environment Profile: [{settings.ENV}]")

        db_connector = DatabaseConnector(settings)
        if not db_connector.test_connection():
            logger.critical("Aborting pipeline run: Database target is unreachable.")
            sys.exit(1)

        # 2. Automated Schema Provisioning Check
        with db_connector.get_session() as session:
            Base.metadata.create_all(bind=session.connection().engine)
            logger.info("Database Schema Synchronization: Verification check complete.")

        # Dependency Injection Layer Architecture
        generator = NormalizedDataGenerator()
        validator = TransactionValidator(settings)
        transformer = TransactionTransformer(settings)
        analyzer = TransactionAnalyzer(settings)

        # Sprint 3 Engines Injection
        dq_tracker = AdvancedDataQualityTracker(settings.SUPPORTED_CURRENCIES)
        delta_loader = IdempotentDeltaIngestionEngine(db_connector)

        # FIX: Restore bulk_loader variable instantiation block
        bulk_loader = BulkDataIngestionEngine(db_connector)

        # Fix: Instantiate TransactionRepository using db_connector to satisfy type checkers
        repository = TransactionRepository(db_connector)
        loader = DatabaseLoader(settings, repository)

        # 3. Checkpoint Tracking Engine (Incremental High-Watermark Fetch)
        latest_watermark = delta_loader.get_latest_transaction_watermark()

        # 4. Generate Fresh Batch Transaction Data
        dataset = generator.generate_batch_dataset(
            customer_count=50, merchant_count=10, transaction_count=1000
        )

        # 5. Production-Grade Advanced Data Quality Profiling Audit
        raw_tx_df = pd.DataFrame(dataset["transactions"])
        dq_report = dq_tracker.profile_transaction_dataset(raw_tx_df)

        if not dq_report["passed_quality_gate"]:
            logger.warning(
                "Pipeline Alert: Batch data failed strict quality metrics thresholds."
            )

        # FIX: Load parent tables first via the high-throughput batch engine
        # to ensure foreign key rows exist before inserting any dependent transactions
        parent_tables_dataset = {
            "customers": dataset.get("customers", []),
            "accounts": dataset.get("accounts", []),
            "merchants": dataset.get("merchants", []),
            "transactions": [],  # Leave blank on this call so our incremental delta loader can execute updates independently below
        }

        # Ingest core lookup identities safely
        bulk_loader.ingest_batch_dataset(parent_tables_dataset)

        # 6. Filtering Fresh Records Above the Timestamp Checkpoint Marker
        if latest_watermark:
            raw_tx_df["timestamp"] = pd.to_datetime(raw_tx_df["timestamp"])
            fresh_records_df = raw_tx_df[
                raw_tx_df["timestamp"] > pd.to_datetime(latest_watermark)
            ]
            logger.info(
                f"Incremental Filter: Isolated {len(fresh_records_df)} fresh rows above watermark."
            )
        else:
            fresh_records_df = raw_tx_df

        # 7. Idempotent Delta Load Upsert Execution Invariant
        fresh_records_list = fresh_records_df.to_dict(orient="records")
        if not delta_loader.upsert_transaction_delta_batch(fresh_records_list):
            logger.error(
                "Delta load operation encountered database processing rollback."
            )

        # Standard Downstream Processing Tracks
        validation_report = validator.validate_transactions(raw_tx_df)
        cleaned_data = transformer.clean_transactions(raw_tx_df, validation_report)
        metrics = analyzer.calculate_metrics(cleaned_data)

        # Store Local Snapshots and Reports
        loader.save_to_csv(cleaned_data)
        parquet_path = loader.save_to_parquet(cleaned_data)
        loader.save_json_report(metrics)
        loader.upload_to_s3(parquet_path, settings.AWS_S3_PROCESSED_KEY)

        logger.info("=== PIPELINE RUN COMPLETE: SUCCESS ===")

    except Exception as e:
        logger.critical(
            f"Pipeline crashed during execution lifecycle: {e!s}", exc_info=True
        )
        sys.exit(1)


if __name__ == "__main__":
    run_platform_pipeline()
