import os
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta
from pathlib import Path

# Caminhos
DAG_DIR = os.path.dirname(os.path.abspath(__file__))
GOOGLE_CREDENTIALS_PATH = os.path.join(DAG_DIR, "../credenciais.json")
BASE_SQL_DIR = Path(DAG_DIR) / "../example_dags/sql"
SQL_FILES = {
    "sales_by_month_year": BASE_SQL_DIR / "sales_by_month_year.sql",
    "sales_by_line_brand": BASE_SQL_DIR / "sales_by_line_brand.sql",
    "sales_by_line": BASE_SQL_DIR / "sales_by_line.sql",
    "sales_by_brand": BASE_SQL_DIR / "sales_by_brand.sql",
}

# Exporta a credencial para o bq
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CREDENTIALS_PATH


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 3, 9),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="gold_sales_transform",
    default_args=default_args,
    schedule_interval="0 9 * * *",
    catchup=False,
    tags=["bigquery", "gold"],
) as dag:

    start_task = EmptyOperator(task_id="start")

    tasks = {}

    for name, sql_file in SQL_FILES.items():
        tasks[name] = BashOperator(
            task_id=f"run_{name}",
            bash_command=f"""
            export GOOGLE_APPLICATION_CREDENTIALS={GOOGLE_CREDENTIALS_PATH}

            bq query --use_legacy_sql=false < {sql_file}
            """
        )
    
    end_task = EmptyOperator(task_id="end")

    start_task >> tasks["sales_by_month_year"] >> end_task
    start_task >> tasks["sales_by_line_brand"] >> end_task
    start_task >> tasks["sales_by_line"] >> end_task
    start_task >> tasks["sales_by_brand"] >> end_task