from datetime import datetime, timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow.models.dag import DAG

# Operators; we need this to operate!
from airflow.operators.python import PythonOperator

import requests

USER_SERVICE_URL = "http://user-service:8002"


def call_get_user_news():
    print("Calling user service")
    response = requests.get(f"{USER_SERVICE_URL}/get_latest_news")
    print(response.json())


with DAG(
        "News_collection",
        default_args={
            "depends_on_past": False,
            "email_on_failure": False,
            "email_on_retry": False,
        },
        description="DAG calls the endpoint to get news",
        # every 10 minutes
        schedule_interval=timedelta(minutes=5),
        start_date=datetime(2025, 1, 19, 8, 0),
        catchup=True,
        tags=["something"],
) as dag:

    news_collection = PythonOperator(
        task_id="get_users_news",
        python_callable=call_get_user_news,
        retries=3,
    )

    news_collection
