from collections.abc import Generator
from contextlib import contextmanager
from os import environ
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from src.config import Settings
from src.logger import setup_logger

logger = setup_logger(__name__)


class DatabaseConnector:
    """Manages secure connection pooling and safe transactions into PostgreSQL."""

    def __init__(self, settings: Settings) -> None:
        # Calculate the absolute project root folder natively from this file's location
        root_dir = Path(__file__).resolve().parent.parent
        env_path = root_dir / ".env"

        # Explicit path-safe loading with forced environment override parameters
        if env_path.exists():
            load_dotenv(dotenv_path=str(env_path), override=True)
        else:
            logger.warning(
                f"Database Environment Alert: No local configuration file detected at {env_path}"
            )

        # Fetch configurations securely out of environment dict layouts
        db_user = environ.get("DB_USER", "postgres")
        db_pass = environ.get(
            "DB_PASS", "your_secure_password_here"
        )  # Default to a placeholder; should be overridden in production
        db_host = environ.get("DB_HOST", "localhost")  # Default safely to IPv4 loopback
        db_port = environ.get("DB_PORT", "5432")
        db_name = environ.get("DB_NAME", "fintech_db")

        if not db_pass:
            logger.warning(
                "Database Core Configuration Warning: DB_PASS environment key is currently unset."
            )

        logger.info(
            f"Database Ingestion Engine: Connecting to host '{db_host}' on port '{db_port}'"
        )

        self.connection_url = (
            f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        )
        self.engine = create_engine(
            self.connection_url, pool_size=10, max_overflow=20, pool_pre_ping=True
        )
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Context manager to ensure transactions are safely committed or rolled back."""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            logger.error("Database Transaction Failure: Issuing rollback command.")
            raise
        finally:
            session.close()

    def test_connection(self) -> bool:
        """Executes a diagnostic verification handshake against the warehouse."""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Database Connection: Live and responding successfully.")
            return True
        # Catch the specific DB driver/SQLAlchemy error instead
        except SQLAlchemyError as e:
            logger.error(f"Database Handshake Failed: {e!s}")
            return False
