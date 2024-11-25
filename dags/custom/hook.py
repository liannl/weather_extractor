import requests
from airflow.hooks.base_hook import BaseHook


class WeatherAPIHook(BaseHook):

    def __init__(self, conn_id):
        super().__init__()
        self._conn_id = conn_id

    def get_weather_data(self, city):
        config = self.get_connection(self._conn_id)
        key = config.extra_dejson.get('api_key')
        base_url = f"http://api.weatherapi.com/v1/current.json?key={key}&q={city}"

        response = requests.get(base_url)
        if response.status_code == 200:
            data = response.json()
            return {
                "temp_c": data["current"]["temp_c"],
                "condition": data["current"]["condition"]["text"]
            }
        else:
            raise Exception(f"Error fetching data from Weather API: {response.text}")