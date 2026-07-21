import sys
from src.config import Settings
from src.logger import setup_logger
from src.generator import TransactionGenerator
from src.extractor import TransactionExtractor
from src.validator import TransactionValidator
from src.transformer import TransactionTransformer
from src.analyzer import TransactionAnalyzer
from src.loader import FileLoader

logger = setup_logger("pipeline_orchestrator")

def run_platform_pipeline():
    logger.info("=== STARTING REFACTORED FINTECH DATA PLATFORM PIPELINE ===")
    
    try:
        # 1. Centralized Configuration Initialization
        settings = Settings()

        # 2. Dependency Injection Lifecycle Initialization
        generator = TransactionGenerator(settings)
        extractor = TransactionExtractor(settings)
        validator = TransactionValidator(settings)
        transformer = TransactionTransformer(settings)
        analyzer = TransactionAnalyzer(settings)
        loader = FileLoader(settings)

        # 3. Synchronous Pipeline Execution Lifecycle Trace
        generator.generate_transactions()
        raw_data = extractor.extract_transactions()
        
        # Isolated Audit Validation Step
        validation_report = validator.validate_transactions(raw_data)
        
        # Clean and aggregate
        cleaned_data = transformer.clean_transactions(raw_data, validation_report)
        metrics = analyzer.calculate_metrics(cleaned_data)
        
        # Output persistence
        loader.save_data(cleaned_data)
        loader.save_report(metrics)
        
        logger.info("=== PIPELINE RUN COMPLETE: SUCCESS ===")

    except Exception as e:
        logger.critical(f"Pipeline crashed during execution: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    run_platform_pipeline()
