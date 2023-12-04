"""Contains the class that represents each record of data
"""
from datetime import datetime

from utils import validate_float, validate_int


class WeatherRecord:
    """Class type for each data record object"""

    def __init__(self, record_data: dict[str, str]) -> None:
        record_date = record_data.get("PKT") or record_data.get("PKST")
        self.date = datetime.strptime(record_date, "%Y-%m-%d")
        self.max_temp = validate_int(record_data["Max TemperatureC"])
        self.min_temp = validate_int(record_data["Min TemperatureC"])
        self.mean_temp = validate_int(record_data["Mean TemperatureC"])
        self.max_humidity = validate_float(record_data["Max Humidity"])
        self.mean_humidity = validate_float(record_data[" Mean Humidity"])

