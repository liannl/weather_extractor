from airflow import DAG
from datetime import datetime, timedelta
import logging

from custom.hook import WeatherAPIHook
from custom.operator import WeatherToCSVOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 25),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'extract_weather',
    default_args=default_args,
    description='Read API and insert data into csv',
    schedule_interval=timedelta(days=1),
    catchup=False
)

def _extract_data(conn_id, city):
    logger = logging.getLogger(__name__)
    hook = WeatherAPIHook(conn_id=conn_id)
    logger.info(f"Writing ratings to {hook.get_weather_data(city=city)}")


extract_data = WeatherToCSVOperator(
    task_id="extract_data",
    conn_id="weather_api",
    city="Moscow",
    file_path="/opt/airflow/data/Moscow_20241126.csv",
    dag=dag
)

extract_data