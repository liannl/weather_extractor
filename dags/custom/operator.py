import pandas as pd

from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from custom.hook import WeatherAPIHook



class WeatherToCSVOperator(BaseOperator):
    @apply_defaults
    def __init__(
            self, conn_id, op_kwargs, **kwargs,
    ):
        super(WeatherToCSVOperator , self).__init__(**kwargs)

        self._conn_id = conn_id
        self._op_kwargs = op_kwargs

    def execute(self, context):
        hook = WeatherAPIHook(self._conn_id)

        self.log.info( f"Fetching weather in {self._op_kwargs['city']}")
        result = hook.get_weather_data(city=self._op_kwargs['city'])

        self.log.info(f"Create DataFrame")
        df = pd.DataFrame([result])

        self.log.info(f"Writing weather to {self._op_kwargs['file_path']}")
        df.to_csv(self._op_kwargs['file_path'], index=False)

        self.log.info(f"Weather data written to {self._op_kwargs['file_path']}")