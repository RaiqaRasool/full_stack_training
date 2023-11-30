"""Responsible for displaying all weather reports
"""
from datetime import datetime

from utils import year_boundary_check
from weather_man import WeatherMan


class ReportGenerator:
    """Displays weather reports"""

    _weather_man: WeatherMan

    def __init__(self) -> None:
        self._weather_man = WeatherMan()

    def yearly_extremes_report(self, year: int) -> None:
        """Prints year extreme values"""
        print(f"\n=== Report for Year {year} === ")
        if year_boundary_check(year):
            (
                highest_temp_record,
                lowest_temp_record,
                highest_humidity_record,
            ) = self._weather_man.get_year_extremes(year)

            print(
                f'Highest:{highest_temp_record.max_temp}C on \
                {highest_temp_record.date.strftime("%B %d")}'
            )
            print(
                f'Lowest:{lowest_temp_record.min_temp}C on \
                {lowest_temp_record.date.strftime("%B %d")}'
            )
            print(
                f'Humidity: {highest_humidity_record.max_humidity}% on \
                {highest_humidity_record.date.strftime("%B %d")}'
            )
        else:
            print("No data for this year exists")

    def monthly_avg_report(self, year_month: str) -> None:
        """Prints month average values"""
        try:
            print(f"\n=== Report for {year_month} === ")
            date = datetime.strptime(year_month, "%Y/%m")
            (
                highest_temp_avg,
                lowest_temp_avg,
                mean_humidity_avg,
            ) = self._weather_man.get_month_avg(date.year, date.month)

            print(f"Highest Temperature Average: {highest_temp_avg}C")
            print(f"Lowest Temperature Average: {lowest_temp_avg}C")
            print(f"Mean Humidity Average: {mean_humidity_avg}%")
        except ValueError as _:
            print("Enter date in the correct format - yyyy/mm")

    def daily_month_report(self, year_month: str) -> None:
        """Print each day max and min temps with bars"""
        try:
            print(f"\n=== Report for {year_month} ===")
            date = datetime.strptime(year_month, "%Y/%m")
            weather_data = self._weather_man.get_month_data(date.year, date.month)

            if weather_data:
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
                        for _ in range(max_temp):
                            high_temp_str += "+"
                        high_temp_str += RESET
                    if min_temp:
                        low_temp_str = BLUE
                        for _ in range(min_temp):
                            low_temp_str += "+"
                        low_temp_str += RESET
                    temp_str = str(record.date.day) + " "
                    if low_temp_str:
                        temp_str += low_temp_str
                    if high_temp_str:
                        temp_str += high_temp_str
                    temp_str += " " + str(min_temp)
                    temp_str += "C - " + str(max_temp) + "C"
                    print(temp_str)
            else:
                print("No data for this month exist")

        except ValueError as _:
            print("Enter date in the correct format - yyyy/mm")
