"""weather_man.py
   Has class that handle all data related functions
"""
import csv
from typing import List, Dict, Tuple
import os

from weather_record import WeatherRecord


class WeatherMan:
    """Class responsible for handling all functions on weather data
    """

    _weather_records: List[WeatherRecord] = []

    def __init__(self) -> None:
        if not WeatherMan._weather_records:
            weather_data = self._get_folder_data()
            for record in weather_data:
                WeatherMan._weather_records.append(WeatherRecord(record))

    def _get_folder_data(self) -> List[Dict[str, str]]:
        weather_data_dir = os.path.join(
                                        os.path.dirname(__file__),
                                        'weatherfiles'
                                        )
        data_files = list(os.listdir(weather_data_dir))
        data = []
        for file_path in data_files:
            with open(
                os.path.join(weather_data_dir, file_path),
                "r", encoding="latin-1"
            ) as f:
                csv_reader = csv.DictReader(x.replace("\0", "") for x in f)
                data.extend(list(csv_reader))
        return data

    def get_month_data(self, year: int, month: int) -> List[WeatherRecord]:
        """Return data of a particular month of a year
        """
        month_data = []
        for record in self._weather_records:
            if (record.date.year, record.date.month) == (year, month):
                month_data.append(record)
        return month_data

    def get_year_extremes(self, year: int) -> Tuple[WeatherRecord,
                                                    WeatherRecord,
                                                    WeatherRecord]:
        """Return max and min values of temp and max of humidity
           for given year
        """
        highest_temp_idx = 0
        lowest_temp_idx = 0
        highest_humidity_idx = 0
        weather_data = self._weather_records
        for idx, record in enumerate(weather_data):
            if record.date.year == year:
                if (
                    weather_data[highest_temp_idx].max_temp
                    < record.max_temp
                ):
                    highest_temp_idx = idx
                if (
                    weather_data[lowest_temp_idx].min_temp
                    > record.min_temp
                ):
                    lowest_temp_idx = idx
                if (
                    weather_data[highest_humidity_idx].max_humidity
                    < record.max_humidity
                ):
                    highest_humidity_idx = idx

        return (
                weather_data[highest_temp_idx],
                weather_data[lowest_temp_idx],
                weather_data[highest_humidity_idx],
        )

    def get_month_avg(self, year: int, month: int) -> Tuple[float,
                                                            float,
                                                            float]:
        """Return average of mean humidity, highest and lowest temps
           for given month of the year
        """
        sum_highest_temp = 0.0
        sum_lowest_temp = 0.0
        sum_mean_humidity = 0.0
        month_length = 0
        for record in self._weather_records:
            if (record.date.year, record.date.month) == (year, month):
                month_length += 1
                sum_highest_temp += record.max_temp
                sum_lowest_temp += record.min_temp
                sum_mean_humidity += record.mean_humidity
        return (
                round(sum_highest_temp / month_length, 1),
                round(sum_lowest_temp / month_length, 1),
                round(sum_mean_humidity / month_length, 1)
            )
