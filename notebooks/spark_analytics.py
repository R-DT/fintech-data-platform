import logging
from pathlib import Path
from pyspark.sql import SparkSession # type: ignore
from pyspark.sql.functions import col, sum as _sum, avg, count # type: ignore

# Centralized console tracker tracking for script visibility
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("pyspark_analytics_engine")

def run_distributed_analytics() -> None:
    """Initializes a local Spark Session, processes Parquet data lakes, and aggregates stats."""
    logger.info("Initializing Distributed Spark Session Engine...")
    
    # 1. Establish an isolated local Spark cluster core session
    spark = SparkSession.builder \
        .appName("FintechPlatformSparkAnalytics") \
        .master("local[*]") \
        .getOrCreate()
    
    # Mute internal verbose Spark tracking logs to keep your terminal output clean
    spark.sparkContext.setLogLevel("WARN")

    try:
        # 2. Map file boundaries using your unified pathlib directory structures
        base_dir = Path(__file__).resolve().parent.parent
        parquet_source = base_dir / "data" / "processed" / "cleaned_ledger.parquet"
        report_destination = base_dir / "data" / "reports" / "spark_channel_metrics"

        if not parquet_source.exists():
            raise FileNotFoundError(f"Distributed Ingestion Error: Target Parquet asset not found at {parquet_source}")

        logger.info(f"Ingesting binary columnar Parquet records from data lake location: {parquet_source}")
        
        # 3. Read the data lake file natively into a highly efficient Spark DataFrame
        df = spark.read.parquet(str(parquet_source))
        
        # Display the distributed dataframe schema map to confirm structural types match up
        logger.info("Spark Ingestion Success. Operational Data Schema:")
        df.printSchema()

        # 4. Compute High-Velocity Large-Scale Metrics using Spark Catalyst Optimizers
        logger.info("Calculating distributed transactional metrics across payment channels...")
        channel_metrics = df.groupBy("Channel").agg(
            count("TransactionID").alias("total_transactions"),
            _sum("Amount").alias("gross_volume_usd"),
            avg("Amount").alias("average_transaction_value")
        ).orderBy(col("gross_volume_usd").desc())

        # Show the processed analytics directly to your terminal window screen output
        logger.info("Distributed Calculation Success. Result Ledger Snapshot:")
        channel_metrics.show(truncate=False)

        # 5. Export out partitioned report files into your local storage volumes
        logger.info(f"Writing partitioned business metric snapshots out to storage: {report_destination}")
        channel_metrics.write \
            .mode("overwrite") \
            .parquet(str(report_destination))

        logger.info("PySpark Distributed Analytical Run Complete: Success.")

    except Exception as e:
        logger.error(f"PySpark processing engine encountered a critical disruption: {str(e)}", exc_info=True)
    finally:
        # Explicitly terminate the cluster session context to free up computer RAM memory
        spark.stop()
        logger.info("Spark Session safely deactivated.")

if __name__ == "__main__":
    run_distributed_analytics()
