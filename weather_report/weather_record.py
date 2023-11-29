"""Contains the class that represents each record of data
"""
from datetime import datetime
from utils import int_, float_


class WeatherRecord:
    """Class type for each data record object
    """

    def __init__(self, record_data: dict[str, str]) -> None:
        date_key = next(
            (key for key in record_data.keys() if 'PK' in key),
            ''
            )

        self.date = datetime.strptime(record_data[date_key], "%Y-%m-%d")
        self.max_temp = int_(record_data["Max TemperatureC"])
        self.min_temp = int_(record_data["Min TemperatureC"])
        self.mean_temp = int_(record_data["Mean TemperatureC"])
        self.max_humidity = float_(record_data["Max Humidity"])
        self.mean_humidity = float_(record_data[" Mean Humidity"])
