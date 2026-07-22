import argparse
import sys
import pytest
from src.config import Settings
from src.logger import setup_logger
from src.generator import TransactionGenerator
from src.extractor import TransactionExtractor
from src.validator import TransactionValidator
from src.transformer import TransactionTransformer
from src.analyzer import TransactionAnalyzer
from src.database import DatabaseConnector
from src.loader import DatabaseLoader

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
        help="Specify the engine operation mode."
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
        db_connector = DatabaseConnector()

        # Run an active health handshake check against your PostgreSQL Docker container
        if not db_connector.test_connection():
            logger.critical("Pipeline execution aborted: Database target is unreachable.")
            sys.exit(1)

        # Dependency Injection Lifecycle
        generator = TransactionGenerator(settings)
        extractor = TransactionExtractor(settings)
        validator = TransactionValidator(settings)
        transformer = TransactionTransformer(settings)
        analyzer = TransactionAnalyzer(settings)
        
        # Inject BOTH settings and the database connection manager into your loader
        loader = DatabaseLoader(settings, db_connector)

        # Operational ETL pipeline run sequence
        generator.generate_transactions()
        raw_data = extractor.extract_transactions()
        
        validation_report = validator.validate_transactions(raw_data)
        cleaned_data = transformer.clean_transactions(raw_data, validation_report)
        metrics = analyzer.calculate_metrics(cleaned_data)
        
        # Persist data assets safely to both file storage and SQL database layers
        loader.save_to_csv(cleaned_data)
        loader.save_to_parquet(cleaned_data)
        loader.save_json_report(metrics)
        loader.load_to_postgres(cleaned_data)
        
        logger.info("=== PIPELINE RUN COMPLETE: SUCCESS ===")

    except Exception as e:
        logger.critical(f"Pipeline crashed during execution lifecycle: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    run_platform_pipeline()
