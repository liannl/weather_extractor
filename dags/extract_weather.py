from airflow.decorators import dag
from datetime import datetime, timedelta
from custom.operator import WeatherToCSVOperator
from airflow.utils.task_group import TaskGroup


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 25),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
city = ["Moscow", "Paris", "Berlin"]

@dag(
    default_args=default_args,
    description='Read API and insert data into CSV',
    schedule_interval=timedelta(days=1),
    catchup=False
)
def extract_weather_dag_for():

    with TaskGroup('tasks_for') as tasks_for:
        for i in range(city.__len__()):
            WeatherToCSVOperator(
                task_id=f"extract_data_from_{city[i]}",
                conn_id="weather_api",
                city=city[i],
                file_path=f"/opt/airflow/data/{city[i]}_20241126.csv",
            )

    tasks_for

dag = extract_weather_dag_for()

# city = ["Moscow", "Paris", "Berlin"],
# file_path = [
#     "/opt/airflow/data/Moscow_20241126.csv",
#     "/opt/airflow/data/Paris_20241126.csv",
#     "/opt/airflow/data/Berlin_20241126.csv",
# ]
