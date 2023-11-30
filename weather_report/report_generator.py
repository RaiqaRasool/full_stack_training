"""Responsible for displaying all weather reports
"""
from datetime import datetime

from utils import value_error_decorator
from weather_man import WeatherMan


class ReportGenerator:
    """Displays weather reports"""

    def __init__(self, folder_name: str) -> None:
        self._weather_man = WeatherMan(folder_name)

    @value_error_decorator
    def yearly_extremes_report(self, year_date: datetime) -> None:
        """Prints year extreme values"""
        print(f"\n=== Report for Year {year_date.year} === ")
        (
            highest_temp_record,
            lowest_temp_record,
            highest_humidity_record,
        ) = self._weather_man.get_year_extremes(year_date)

        print(
            f'Highest: {highest_temp_record.max_temp}C on \
            {highest_temp_record.date.strftime("%B %d")}'
        )
        print(
            f'Lowest: {lowest_temp_record.min_temp}C on \
            {lowest_temp_record.date.strftime("%B %d")}'
        )
        print(
            f'Humidity: {highest_humidity_record.max_humidity}% on \
            {highest_humidity_record.date.strftime("%B %d")}'
        )

    @value_error_decorator
    def monthly_avg_report(self, year_month: datetime) -> None:
        """Prints month average values"""
        print(f"\n=== Report for {year_month.strftime('%B, %Y')} === ")
        (
            highest_temp_avg,
            lowest_temp_avg,
            mean_humidity_avg,
        ) = self._weather_man.get_month_avg(year_month)

        print(f"Highest Temperature Average: {highest_temp_avg}C")
        print(f"Lowest Temperature Average: {lowest_temp_avg}C")
        print(f"Mean Humidity Average: {mean_humidity_avg}%")

    @value_error_decorator
    def daily_month_report(self, year_month: datetime) -> None:
        """Print each day max and min temps with bars"""
        weather_data = self._weather_man.filter_data(year_month)
        print(f"\n=== Report for {year_month.strftime('%B, %Y')} ===")
        if not weather_data:
            raise ValueError(
                f"No data available for the {year_month.strftime('%m-%Y')}"
            )

        RESET = "\033[0m"
        RED = "\033[91m"
        BLUE = "\033[94m"
        for record in weather_data:
            min_temp = record.min_temp
            max_temp = record.max_temp
            low_temp_str = ""
            high_temp_str = ""
            if max_temp:
                high_temp_str = RED
                high_temp_str += "+" * max_temp
                high_temp_str += RESET
            if min_temp:
                low_temp_str = BLUE
                low_temp_str += "+" * min_temp
                low_temp_str += RESET
            temp_str = str(record.date.day) + " "
            if low_temp_str:
                temp_str += low_temp_str
            if high_temp_str:
                temp_str += high_temp_str
            temp_str += " " + str(min_temp)
            temp_str += "C - " + str(max_temp) + "C"
            print(temp_str)
