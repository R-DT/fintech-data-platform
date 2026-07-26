from datetime import datetime, timedelta
import airflow  # type: ignore
from airflow import DAG  # type: ignore
from airflow.providers.docker.operators.docker import DockerOperator  # type: ignore
from docker.types import Mount  # type: ignore

# 1. Define explicit operational task SLAs and retry parameters
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,                      # Automatically retry twice if a network drops
    "retry_delay": timedelta(minutes=5) # Wait 5 minutes between retries
}

# 2. Instantiate the global Directed Acyclic Graph tracking coordinator
with DAG(
    dag_id="fintech_platform_etl_orchestrator",
    default_args=default_args,
    description="Automated orchestration loop for daily transaction ledger processing",
    schedule_interval="@daily",        # Run automatically every single midnight
    catchup=False,
    max_active_runs=1
) as dag:

    # 3. Execute the data pipeline securely via an isolated Docker container operator
    execute_pipeline_task = DockerOperator(
        task_id="run_fintech_platform_etl",
        image="fintech-platform:latest",  # Targets your compiled application image
        command="-m run",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="docker_default",     # Connects straight to your postgres network bridge
        mounts=[
            Mount(source="/var/lib/fintech/data", target="/app/data", type="bind")
        ],
        environment={
            "DB_USER": "postgres",
            "DB_PASS": "postgres",
            "DB_HOST": "warehouse_db",     # Resolves cleanly via internal container routing
            "DB_PORT": "5432",
            "DB_NAME": "fintech_db"
        }
    )

    # Clean unused tracking expression assignment for Pylance basic compatibility
    _ = execute_pipeline_task  # type: ignore
