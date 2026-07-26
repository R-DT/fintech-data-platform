import json
import logging
from pathlib import Path

import pandas as pd

from src.config import Settings
from src.repository import TransactionRepository

logger = logging.getLogger(__name__)


class FileLoader:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def save_to_csv(
        self, df: pd.DataFrame, target_name: str = "cleaned_ledger.csv"
    ) -> str:
        destination: Path = self.settings.PROCESSED_DATA_DIR / target_name
        destination.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(destination, index=False)
        logger.info(f"Load Phase: Clean transactions saved to CSV -> {destination}")
        return str(destination)

    def save_json_report(
        self, metrics: dict, target_name: str = "analytics_report.json"
    ) -> str:
        destination: Path = self.settings.REPORTS_DIR / target_name
        destination.parent.mkdir(parents=True, exist_ok=True)
        with open(destination, "w") as f:
            json.dump(metrics, f, indent=4)
        logger.info(f"Load Phase: Business report saved to JSON -> {destination}")
        return str(destination)

    def save_to_parquet(
        self, df: pd.DataFrame, target_name: str = "cleaned_ledger.parquet"
    ) -> str:
        """Saves the cleaned dataset into compressed, high-performance columnar Parquet files."""
        destination: Path = self.settings.PROCESSED_DATA_DIR / target_name
        destination.parent.mkdir(parents=True, exist_ok=True)

        # Write to disk using the pyarrow columnar compression backend engine
        df.to_parquet(destination, index=False, engine="pyarrow", compression="snappy")
        logger.info(
            f"Load Phase: Clean transactions saved to Parquet data lake -> {destination}"
        )
        return str(destination)


class DatabaseLoader(FileLoader):
    """Handles multi-destination file persistence and relational repository routing."""

    def __init__(self, settings: Settings, repository: TransactionRepository) -> None:
        super().__init__(settings)
        # Inject the Repository Pattern layer directly
        self.repo = repository

    def load_to_postgres(self, df: pd.DataFrame) -> int:
        """Delegates relational writes to the database repository subsystem."""
        try:
            return self.repo.bulk_insert_transactions(df)
        except Exception:
            logger.error(
                "Load Phase Exception: Database write intercepted and rolled back."
            )
            raise

    def upload_to_s3(self, local_file_path: str, s3_target_key: str) -> bool:
        """Streams a local data asset snapshot securely into an AWS S3 cloud storage bucket."""
        import boto3
        from botocore.exceptions import ClientError, NoCredentialsError

        logger.info(
            f"Load Phase: Initiating AWS S3 cloud transfer vector to bucket -> {self.settings.AWS_S3_BUCKET_NAME}"
        )

        # Initialize the AWS S3 client mapping
        s3_client = boto3.client("s3")
        local_path = Path(local_file_path)

        if not local_path.exists():
            logger.error(
                f"Load Phase: S3 Upload aborted. Local file not found at {local_file_path}"
            )
            return False

        try:
            s3_client.upload_file(
                Filename=str(local_path),
                Bucket=self.settings.AWS_S3_BUCKET_NAME,
                Key=s3_target_key,
            )
            logger.info(
                f"Load Phase: Successfully deployed cloud asset -> s3://{self.settings.AWS_S3_BUCKET_NAME}/{s3_target_key}"
            )
            return True
        except NoCredentialsError:
            # Handles local development gracefully when running without active cloud credentials
            logger.warning(
                "Load Phase: AWS credentials missing. Skipping S3 upload. (Perfect for local dev mode)"
            )
            return False
        except ClientError as e:
            logger.error(
                f"Load Phase: Secure S3 deployment connection dropped. Details: {e!s}"
            )
            return False
