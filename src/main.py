import argparse
import sys

import pandas as pd
import pytest

from src.analyzer import TransactionAnalyzer
from src.bulk_loader import BulkDataIngestionEngine
from src.config import Settings
from src.database import DatabaseConnector
from src.generator import NormalizedDataGenerator
from src.loader import DatabaseLoader
from src.logger import setup_logger
from src.repository import TransactionRepository
from src.transformer import TransactionTransformer
from src.validator import TransactionValidator

logger = setup_logger("pipeline_orchestrator")


def run_platform_pipeline() -> None:
    """Entry point for the fintech-platform CLI, managing both ETL runs and testing."""
    parser = argparse.ArgumentParser(
        description="Fintech Data Platform Core Ingestion and Testing CLI Tool."
    )

    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        default="run",
        choices=["run", "pytest", "pytests"],
        help="Specify the engine operation mode.",
    )

    args = parser.parse_args()

    # 1. Intercept Testing Mode
    if args.mode in ["pytest", "pytests"]:
        logger.info("=== INITIALIZING PLATFORM AUTOMATED TEST RUNNER ===")
        exit_code = pytest.main(["tests"])
        sys.exit(exit_code)

    # 2. Execute Normal ETL Ingestion Mode
    logger.info("=== STARTING FINTECH DATA PLATFORM PIPELINE ===")
    try:
        # Initialize Settings and Database Infrastructure
        settings = Settings()
        db_connector = DatabaseConnector(settings)

        # Run an active health handshake check against your PostgreSQL Docker container
        if not db_connector.test_connection():
            logger.critical(
                "Pipeline execution aborted: Database target is unreachable."
            )
            sys.exit(1)

        # Defensive Programming: Pre-bind variables to clear unbound warnings
        cleaned_data = pd.DataFrame()
        metrics: dict = {}

        # Dependency Injection Lifecycle Architecture
        generator = NormalizedDataGenerator()
        validator = TransactionValidator(settings)
        transformer = TransactionTransformer(settings)
        analyzer = TransactionAnalyzer(settings)
        bulk_loader = BulkDataIngestionEngine(db_connector)

        # Instantiate your repository and inject it straight into your loader
        repository = TransactionRepository(db_connector)
        loader = DatabaseLoader(settings, repository)

        # Operational ETL pipeline run sequence matching the normalized tables
        dataset = generator.generate_batch_dataset(
            customer_count=50, merchant_count=10, transaction_count=1000
        )

        # 3. High-Throughput Bulk Relational Database Loading Ingest Track
        bulk_success = bulk_loader.ingest_batch_dataset(dataset)
        if not bulk_success:
            logger.error(
                "Bulk ingestion sequence encountered isolated processing rollback."
            )

        # Load the generated core transactions component into a DataFrame for downstream processing
        raw_data = pd.DataFrame(dataset["transactions"])

        validation_report = validator.validate_transactions(raw_data)
        cleaned_data = transformer.clean_transactions(raw_data, validation_report)
        metrics = analyzer.calculate_metrics(cleaned_data)

        # Persist data assets safely to file storage and AWS cloud layers
        loader.save_to_csv(cleaned_data)
        parquet_path = loader.save_to_parquet(cleaned_data)
        loader.save_json_report(metrics)

        # Stream your compressed Parquet snapshot into your AWS S3 Cloud Lake target
        loader.upload_to_s3(parquet_path, settings.AWS_S3_PROCESSED_KEY)

        logger.info("=== PIPELINE RUN COMPLETE: SUCCESS ===")

    except Exception as e:
        logger.critical(
            f"Pipeline crashed during execution lifecycle: {e!s}", exc_info=True
        )
        sys.exit(1)


if __name__ == "__main__":
    run_platform_pipeline()
