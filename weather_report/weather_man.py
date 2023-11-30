"""weather_man.py
   Has class that handle all data related functions
"""
import csv
import os
from datetime import datetime
from statistics import mean
from typing import List, Optional, Tuple

from weather_record import WeatherRecord


class WeatherMan:
    """Class responsible for handling all functions on weather data"""

    def __init__(self, folder_name: str) -> None:
        self._weather_records: List[WeatherRecord] = []
        weather_data_dir = os.path.join(os.path.dirname(__file__), folder_name)
        data_files = list(os.listdir(weather_data_dir))
        for file_path in data_files:
            with open(
                os.path.join(weather_data_dir, file_path), "r", encoding="latin-1"
            ) as f:
                csv_reader = csv.DictReader(x.replace("\0", "") for x in f)
                for record in csv_reader:
                    self._weather_records.append(WeatherRecord(record))

    def filter_data(
        self,
        target_date: datetime,
        by_day: Optional[bool] = False,
        by_year: Optional[bool] = False,
    ) -> List[WeatherRecord]:
        """Filter weather data based on the given date and filtration level.
        The filtration level can be specified as 'day', 'year', or by default it is
        'month of a year'."""

        def day_filter(curr: datetime, target: datetime) -> bool:
            return (curr.day, curr.month, curr.year) == (
                target.day,
                target.month,
                target.year,
            )

        def month_filter(curr: datetime, target: datetime) -> bool:
            return (curr.month, curr.year) == (target.month, target.year)

        def year_filter(curr: datetime, target: datetime) -> bool:
            return curr.year == target.year

        if by_day:
            filter_ = day_filter
        elif by_year:
            filter_ = year_filter
        else:
            filter_ = month_filter

        data = list(
            filter(
                lambda record: filter_(record.date, target_date),
                self._weather_records,
            )
        )

        return data

    def get_year_extremes(
        self, year_date: datetime
    ) -> Tuple[WeatherRecord, WeatherRecord, WeatherRecord]:
        """Return max and min values of temp and max of humidity
        for given year
        """
        year_data = self.filter_data(year_date, by_year=True)
        if not year_data:
            raise ValueError(f"No data available for year {year_date.strftime('%Y')}")
        return (
            max(year_data, key=lambda record: record.max_temp),
            min(year_data, key=lambda record: record.min_temp),
            max(year_data, key=lambda record: record.max_humidity),
        )

    def get_month_avg(self, date: datetime) -> Tuple[float, float, float]:
        """Return average of mean humidity, highest and lowest temps
        for given month of the year
        """
        month_data = self.filter_data(date)
        if not month_data:
            raise ValueError(
                f"No data available for the {date.month} month of {date.year}"
            )

        return (
            round(mean(record.max_temp for record in month_data), 1),
            round(mean(record.min_temp for record in month_data), 1),
            round(mean(record.mean_humidity for record in month_data), 1),
        )
