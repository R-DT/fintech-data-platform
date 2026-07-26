import logging
from pathlib import Path
from pyspark.sql import SparkSession  # type: ignore
from pyspark.sql.functions import col, sum as _sum, avg, count  # type: ignore

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("pyspark_analytics_engine")

def run_distributed_analytics() -> None:
    logger.info("Initializing Distributed Spark Session Engine...")
    
    spark = SparkSession.builder \
        .appName("FintechPlatformSparkAnalytics") \
        .master("local[*]") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")

    try:
        base_dir = Path(__file__).resolve().parent.parent
        parquet_source = base_dir / "data" / "processed" / "cleaned_ledger.parquet"
        report_destination = base_dir / "data" / "reports" / "spark_channel_metrics"

        if not parquet_source.exists():
            raise FileNotFoundError(f"Distributed Ingestion Error: Target Parquet asset not found at {parquet_source}")

        logger.info(f"Ingesting binary columnar Parquet records from data lake: {parquet_source}")
        df = spark.read.parquet(str(parquet_source))
        
        logger.info("Calculating distributed transactional metrics across payment channels...")
        channel_metrics = df.groupBy("Channel").agg(
            count("TransactionID").alias("total_transactions"),
            _sum("Amount").alias("gross_volume_usd"),
            avg("Amount").alias("average_transaction_value")
        ).orderBy(col("gross_volume_usd").desc())

        logger.info("Distributed Calculation Success. Result Ledger Snapshot:")
        channel_metrics.show(truncate=False)

        try:
            # 1. Attempt production-grade columnar partitioning natively (Works inside Linux Docker/Airflow)
            logger.info(f"Attempting native Parquet folder partitioning -> {report_destination}")
            channel_metrics.write \
                .mode("overwrite") \
                .partitionBy("Channel") \
                .parquet(str(report_destination))
            logger.info("Native big-data folder partitioning completed successfully.")
            
        except Exception as write_err:
            # 2. Windows Fallback Workaround: Collect to driver memory safely if Hadoop blocks write paths
            logger.warning(f"Native folder partition blocked by local host file system: {str(write_err)}")
            logger.info("Triggering driver-side memory fallback write routine...")
            
            csv_backup = base_dir / "data" / "reports" / "spark_channel_metrics.csv"
            csv_backup.parent.mkdir(parents=True, exist_ok=True)
            
            pandas_df = channel_metrics.toPandas()
            pandas_df.to_csv(csv_backup, index=False)
            logger.info(f"Fallback Execution Success: Clean metrics written to file -> {csv_backup}")

    except Exception as e:
        logger.error(f"PySpark processing engine encountered a critical disruption: {str(e)}", exc_info=True)
    finally:
        spark.stop()
        logger.info("Spark Session safely deactivated.")

if __name__ == "__main__":
    run_distributed_analytics()
