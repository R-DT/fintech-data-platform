import importlib.util
import os
from logging.config import fileConfig

from alembic import context

# 1. Resolve absolute physical folder positions
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, os.pardir))

models_path = os.path.join(project_root, "src", "models.py")
config_path = os.path.join(project_root, "src", "config.py")

# Debugging Safeguard: Print paths if files cannot be discovered on disk
if not os.path.exists(models_path) or not os.path.exists(config_path):
    print(f"\n[ALEMBIC DEBUG] Current Working Directory: {os.getcwd()}")
    print(f"[ALEMBIC DEBUG] Expected Project Root: {project_root}")
    print(
        f"[ALEMBIC DEBUG] Looking for models at: {models_path} (Exists: {os.path.exists(models_path)})"
    )
    print(
        f"[ALEMBIC DEBUG] Looking for config at: {config_path} (Exists: {os.path.exists(config_path)})\n"
    )

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

# 5. Fetch and assign target database URI
app_settings = Settings()
db_url = getattr(
    app_settings, "DATABASE_URL", getattr(app_settings, "database_url", None)
)
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)
