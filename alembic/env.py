import importlib.util
import os
from logging.config import fileConfig

from alembic import context

# 1. Resolve absolute physical folder positions
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, os.pardir))

models_path = os.path.join(project_root, "src", "models.py")
config_path = os.path.join(project_root, "src", "config.py")

# 2. Hardened Native File System Loader for models.py
models_spec = importlib.util.spec_from_file_location("dynamic_models", models_path)
models_module = importlib.util.module_from_spec(models_spec)  # type: ignore
models_spec.loader.exec_module(models_module)  # type: ignore
Base = models_module.Base

# 3. Hardened Native File System Loader for config.py
config_spec = importlib.util.spec_from_file_location("dynamic_config", config_path)
config_module = importlib.util.module_from_spec(config_spec)  # type: ignore
config_spec.loader.exec_module(config_module)  # type: ignore
Settings = config_module.Settings

# 4. Bind targets for migration scanning
target_metadata = Base.metadata

config = context.config

# 5. Fetch and assign target database URI with comprehensive fallbacks
app_settings = Settings()

db_url = None
try:
    # Check for direct environment variables first
    db_url = os.getenv("DATABASE_URL") or os.getenv("DB_CONN_STR")

    if not db_url:
        # Evaluate standard Pydantic/dataclass property fields
        if hasattr(app_settings, "DATABASE_URL"):
            db_url = app_settings.DATABASE_URL
        elif hasattr(app_settings, "database_url"):
            db_url = app_settings.database_url
        elif hasattr(app_settings, "DB_CONN_STR"):
            db_url = app_settings.DB_CONN_STR
except Exception:  # noqa: BLE001, S110
    pass

# Hardened Local Fallback: If no string resolves, target your active local Docker container
if not db_url or "driver" in str(db_url):
    db_url = "postgresql+psycopg2://postgres:postgres@localhost:5432/fintech_db"

config.set_main_option("sqlalchemy.url", str(db_url))

if config.config_file_name is not None and os.path.exists(config.config_file_name):
    fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    if not url:
        raise ValueError(
            "Database connection URL missing from migration context config parameters."
        )

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "pyformat"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    from sqlalchemy import create_engine

    connect_url = config.get_main_option("sqlalchemy.url")
    if not connect_url:
        raise ValueError(
            "Database connection URL missing from migration context config parameters."
        )

    connectable = create_engine(connect_url)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
