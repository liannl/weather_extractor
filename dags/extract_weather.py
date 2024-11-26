from datetime import datetime, timedelta
from custom.operator import WeatherToCSVOperator
from airflow.decorators import dag


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 25),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

@dag(
    default_args=default_args,
    description='Read API and insert data into CSV',
    schedule_interval=timedelta(days=1),
    catchup=False
)
def extract_weather_dag():
    WeatherToCSVOperator.partial(
        task_id="extract_data",
        conn_id="weather_api"
    ).expand(
        op_kwargs=[
            {"city": "Moscow", "file_path": "/opt/airflow/data/Moscow_20241126.csv"},
            {"city": "Paris", "file_path": "/opt/airflow/data/Paris_20241126.csv"},
            {"city": "Berlin", "file_path": "/opt/airflow/data/Berlin_20241126.csv"},
        ]
    )

dag = extract_weather_dag()