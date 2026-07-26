import logging

from pyspark.sql import SparkSession

logger = logging.getLogger(__name__)


def process_fintech_data(input_path: str, output_path: str) -> None:
    """Processes pipeline data using a local PySpark session engine."""
    spark = (
        SparkSession.builder.appName("FintechDataPlatform")
        .master("local[*]")
        .getOrCreate()
    )

    try:
        logger.info(f"Reading source raw files from: {input_path}")
        df = spark.read.parquet(input_path)

        # Transformation logic placeholder
        transformed_df = df.filter(df["amount"] > 0)

        try:
            logger.info(f"Attempting production partition write to: {output_path}")
            transformed_df.write.mode("overwrite").partitionBy("currency").parquet(
                output_path
            )
            logger.info("Native big-data folder partitioning completed successfully.")

        except Exception as write_err:  # noqa: BLE001
            # 2. Windows Fallback Workaround: Collect to driver memory safely if Hadoop blocks write paths
            logger.warning(
                f"Hadoop storage path permissions blocked native write. Triggering memory fallback: {write_err!s}"
            )
            local_data = transformed_df.toPandas()
            local_data.to_parquet(output_path, partition_cols=["currency"])
            logger.info("Local pandas driver fallback writing executed successfully.")

    except Exception:
        logger.exception("PySpark processing engine encountered a critical disruption.")
        raise
    finally:
        spark.stop()
