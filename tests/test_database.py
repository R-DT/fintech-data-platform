import pytest
from unittest.mock import MagicMock
from src.config import Settings
from src.database import DatabaseConnector

@pytest.fixture
def settings() -> Settings:
    """Provides a standardized platform Settings instance for dependency injection."""
    return Settings()

def test_database_connector_successful_connection(mocker, settings: Settings) -> None:
    """Verifies that the database manager returns True when a connection handshake succeeds."""
    # Mock the SQLAlchemy engine connection interface
    mock_engine = mocker.patch("src.database.create_engine")
    mock_conn = MagicMock()
    mock_engine.return_value.connect.return_value.__enter__.return_value = mock_conn
    
    # Inject the settings parameter dependency cleanly into the constructor
    connector = DatabaseConnector(settings)
    assert connector.test_connection() is True

def test_database_session_rollback_on_failure(mocker, settings: Settings) -> None:
    """Verifies that the session manager issues a rollback command if an error occurs."""
    mock_sessionmaker = mocker.patch("src.database.sessionmaker")
    mock_session = MagicMock()
    mock_sessionmaker.return_value.return_value = mock_session
    
    # Inject the settings parameter dependency cleanly into the constructor
    connector = DatabaseConnector(settings)
    
    with pytest.raises(ValueError):
        with connector.get_session():
            raise ValueError("Simulated write interruption query crash")
            
    # Verify that rollback and close operations were explicitly executed to protect data
    mock_session.rollback.assert_called_once()
    mock_session.close.assert_called_once()
