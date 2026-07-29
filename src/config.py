import os
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Encapsulates production-grade multi-environment application configurations."""

    # Environment Discriminator Execution Target
    ENV: Literal["DEV", "TEST", "PROD"] = os.getenv("ENV", "DEV")  # type: ignore

    # Database Connection Management Matrices
    DATABASE_URL: str = (
        "postgresql+psycopg2://postgres:postgres@localhost:5432/fintech_db"
    )

    # Cloud Infrastructure Target Parameters
    AWS_S3_BUCKET_NAME: str = "fintech-data-lake-bucket"
    AWS_S3_PROCESSED_KEY: str = "processed/transactions.parquet"

    # Strict Validation Constraints
    SUPPORTED_CURRENCIES: list[str] = ["USD", "EUR", "GBP", "NGN", "KES"]

    # FIX: Restore base physical storage directory parameters for local data exports
    RAW_DATA_DIR: Path = Path("data/raw")
    PROCESSED_DATA_DIR: Path = Path("data/processed")
    REPORTS_DIR: Path = Path("data/reports")

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        # Dynamic runtime adjustments based on your selected target environment
        if self.ENV == "TEST":
            self.DATABASE_URL = "sqlite:///:memory:"
        elif self.ENV == "PROD":
            self.DATABASE_URL = os.getenv(
                "DATABASE_URL",
                "postgresql+psycopg2://admin:secure_prod_pass@prod-db-host:5432/fintech_analytics",
            )
