"""Contains the class that represents each record of data
"""
from datetime import datetime

from utils import convert_to_float, convert_to_int


class WeatherRecord:
    """Class type for each data record object"""

    def __init__(self, record_data: dict[str, str]) -> None:
        date = record_data.get("PKT") or record_data.get("PKST")
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.max_temp = convert_to_int(record_data["Max TemperatureC"])
        self.min_temp = convert_to_int(record_data["Min TemperatureC"])
        self.mean_temp = convert_to_int(record_data["Mean TemperatureC"])
        self.max_humidity = convert_to_float(record_data["Max Humidity"])
        self.mean_humidity = convert_to_float(record_data[" Mean Humidity"])

