"""Responsible for displaying all weather reports
"""
from datetime import datetime
from enum import Enum

from weather_man import WeatherMan


class Color(Enum):
    """Enum with color codes"""

    RESET = "\033[0m"
    RED = "\033[91m"
    BLUE = "\033[94m"


class ReportGenerator:
    """Displays weather reports"""

    def __init__(self, data_dir: str) -> None:
        self._weather_man = WeatherMan(data_dir)

    def generate_yearly_extremes_report(self, year_date: datetime) -> None:
        """Prints year extreme values"""
        print(f"\n=== Report for Year {year_date.year} === ")
        year_data = self._weather_man.filter_data(year_date, by_year=True)
        if not year_data:
            print(f"No data for {year_date.year} exists")
            return

        (
            highest_temp_record,
            lowest_temp_record,
            highest_humidity_record,
        ) = self._weather_man.get_year_extremes(year_data)
        print(
            f'Highest: {highest_temp_record.max_temp}C on {highest_temp_record.date.strftime("%B %d")}'
        )
        print(
            f'Lowest: {lowest_temp_record.min_temp}C on {lowest_temp_record.date.strftime("%B %d")}'
        )
        print(
            f'Humidity: {highest_humidity_record.max_humidity}% on {highest_humidity_record.date.strftime("%B %d")}'
        )

    def generate_monthly_avg_report(self, year_month: datetime) -> None:
        """Prints month average values"""
        print(f"\n=== Report for {year_month.strftime('%B, %Y')} === ")
        year_data = self._weather_man.filter_data(year_month)
        if not year_data:
            print(f"No data for {year_month.strftime('%m - %Y')} exists")
            return

        (
            highest_temp_avg,
            lowest_temp_avg,
            mean_humidity_avg,
        ) = self._weather_man.get_month_avg(year_data)
        print(f"Highest Temperature Average: {highest_temp_avg}C")
        print(f"Lowest Temperature Average: {lowest_temp_avg}C")
        print(f"Mean Humidity Average: {mean_humidity_avg}%")

    def generate_daily_month_report(self, year_month: datetime) -> None:
        """Print each day max and min temps with bars"""
        weather_data = self._weather_man.filter_data(year_month)
        print(f"\n=== Report for {year_month.strftime('%B, %Y')} ===")
        if not weather_data:
            print(f"No data available for the {year_month.strftime('%m-%Y')}")
            return

        for record in weather_data:
            min_temp = record.min_temp
            max_temp = record.max_temp
            rec_day = str(record.date.day)
            print(f"{rec_day} ", end="")
            print(Color.BLUE.value + ("+" * min_temp), end="")
            print(Color.RED.value + ("+" * max_temp), end=" ")
            print(Color.RESET.value, end="")
            print(f"{min_temp}C - {max_temp}C")

