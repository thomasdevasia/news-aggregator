from datetime import datetime, timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow.models.dag import DAG

# Operators; we need this to operate!
from airflow.operators.python import PythonOperator


def call_get_user_news():
    print("Hello World")


with DAG(
        "News_collection",
        default_args={
            "depends_on_past": False,
            "email_on_failure": False,
            "email_on_retry": False,
        },
        description="DAG calls the endpoint to get news",
        # every 10 minutes
        schedule_interval=timedelta(minutes=1),
        start_date=datetime(2024, 12, 30, 18, 2),
        catchup=True,
        tags=["something"],
) as dag:

    news_collection = PythonOperator(
        task_id="get_users_news",
        python_callable=call_get_user_news,
        retries=3,
    )

    news_collection
