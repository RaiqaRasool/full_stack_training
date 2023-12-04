"""weather_man.py
   Has class that handle all data related functions
"""
import csv
import os
from datetime import datetime
from statistics import mean
from typing import Dict, List, Optional, Tuple

from weather_record import WeatherRecord


class WeatherMan:
    """Class responsible for handling all functions on weather data"""

    def __init__(self, data_dir: str) -> None:
        self._weather_records: Dict[int, Dict[int, Dict[int, WeatherRecord]]] = {}
        data_dir_path = os.path.join(os.path.dirname(__file__), data_dir)
        data_files = list(os.listdir(data_dir_path))
        for file_path in data_files:
            with open(
                os.path.join(data_dir_path, file_path), "r", encoding="latin-1"
            ) as f:
                csv_reader = csv.DictReader(x.replace("\0", "") for x in f)
                for record in csv_reader:
                    weather_record = WeatherRecord(record)
                    year = weather_record.date.year
                    month = weather_record.date.month
                    day = weather_record.date.day
                    self._weather_records.setdefault(year, {}).setdefault(month, {})[
                        day
                    ] = weather_record

    def filter_data(
        self,
        target_date: datetime,
        by_day: Optional[bool] = False,
        by_year: Optional[bool] = False,
    ) -> List[WeatherRecord]:
        """Filter weather data based on the given date and filtration level.
        The filtration level can be specified as 'day', 'year', or by default it is
        'month of a year'."""
        month = target_date.month
        year = target_date.year
        if by_year:
            filtered_data = [
                day
                for month in self._weather_records.get(year, {}).values()
                for day in month.values()
            ]
        else:
            filtered_data = list(self._weather_records.get(year,{}).get(month,{}).values())

        return filtered_data

    def get_year_extremes(
        self, year_data: List[WeatherRecord]
    ) -> Tuple[WeatherRecord, WeatherRecord, WeatherRecord]:
        """Return max and min values of temp and max of humidity
        for given year
        """
        return (
            max(year_data, key=lambda record: record.max_temp),
            min(year_data, key=lambda record: record.min_temp),
            max(year_data, key=lambda record: record.max_humidity),
        )

    def get_month_avg(
        self, month_data: List[WeatherRecord]
    ) -> Tuple[float, float, float]:
        """Return average of mean humidity, highest and lowest temps
        for given month of the year
        """
        return (
            round(mean(record.max_temp for record in month_data), 1),
            round(mean(record.min_temp for record in month_data), 1),
            round(mean(record.mean_humidity for record in month_data), 1),
        )

