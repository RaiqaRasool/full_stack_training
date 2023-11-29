"""
This file performs all the operations mentioned in readme for weather man problem
"""
import csv
import os
import argparse
from datetime import datetime


# utility functions =====================
def year_boundary_check(check_year) -> bool:
    """
    Return true if year is between 2004 and 2016
    and false otherwise
    """
    if check_year and 2004 <= check_year <= 2016:
        return True
    return False


def year_month_validation_decorator(func):
    """
    Validate if the year and month given are in the right format
    """

    def wrapper(data, report_month):
        date = report_month.split("/")
        print(
            f"\n=== {func.__name__.replace('_', ' ').title()} for {report_month} ==="
        )
        if len(date) == 2 and all(value != "" for value in date):
            r_year, r_month = map(int, date)
            if year_boundary_check(r_year) and 1 <= r_month <= 12:
                func(data, r_year, r_month)
            else:
                print("This year or month data is not available")
        else:
            print("Please give year and month in correct format -- yyyy/mm")

    return wrapper


def parse_weather_data(weather_row) -> dict:
    """
    parse the weather columns to respective data types
    """
    parsed_weather_row = {}
    for key, value in weather_row.items():
        if key in ("PKT", "PKST"):
            parsed_weather_row["PKT"] = datetime.strptime(
                value, "%Y-%m-%d"
            ).date()
        elif key == " Events":
            parsed_weather_row[key.strip()] = value
        else:
            # key.strip() remove extra spacing in key
            parsed_weather_row[key.strip()] = (
                0.0 if value == "" else float(value)
            )
    return parsed_weather_row


def read_weather_data() -> list:
    """
    Read the data files from weatherfiles folder and return it
    """
    weather_data_dir = os.path.join(os.path.dirname(__file__), "weatherfiles")
    data_files = list(os.listdir(weather_data_dir))
    weather_data_list = []
    for file_path in data_files:
        with open(
            os.path.join(weather_data_dir, file_path), "r", encoding="latin-1"
        ) as f:
            # replace null values with empty string
            csv_reader = csv.DictReader(x.replace("\0", "") for x in f)
            for row in csv_reader:
                weather_row = parse_weather_data(row)
                weather_data_list.append(weather_row)
    return weather_data_list


# main functions ============================
def get_year_report(data, report_year) -> None:
    """
    For a given year this functions display the highest temperature and day,
    lowest temperature and day, most humid day and humidity.
    """
    print(f"\n=== Report of Year {report_year} ===")
    if not year_boundary_check(report_year):
        print("No data for this year exist")
    else:
        highest_temp_idx = 0
        lowest_temp_idx = 0
        highest_humidity_idx = 0
        for idx, row in enumerate(data):
            if row["PKT"].year == report_year:
                if (
                    data[highest_temp_idx]["Max TemperatureC"]
                    < row["Max TemperatureC"]
                ):
                    highest_temp_idx = idx
                if (
                    data[lowest_temp_idx]["Min TemperatureC"]
                    > row["Min TemperatureC"]
                ):
                    lowest_temp_idx = idx
                if (
                    data[highest_humidity_idx]["Max Humidity"]
                    < row["Max Humidity"]
                ):
                    highest_humidity_idx = idx
        highest_temp_row = data[highest_temp_idx]
        lowest_temp_row = data[lowest_temp_idx]
        highest_humidity_row = data[highest_humidity_idx]
        print(
            "Highest:",
            str(highest_temp_row["Max TemperatureC"]) + "C on ",
            highest_temp_row["PKT"].strftime("%B %d"),
        )
        print(
            "Lowest:",
            str(lowest_temp_row["Min TemperatureC"]) + "C on ",
            lowest_temp_row["PKT"].strftime("%B %d"),
        )
        print(
            "Humidity:",
            str(highest_humidity_row["Max Humidity"]) + "% on ",
            highest_humidity_row["PKT"].strftime("%B %d"),
        )


@year_month_validation_decorator
def get_month_avg_report(data, r_year, r_month) -> None:
    """
    For a given month it displaysr the average highest temperature,
    average lowest temperature, average mean humidity.
    """
    sum_highest_temp = 0.0
    sum_lowest_temp = 0.0
    sum_mean_humidity = 0.0
    month_length = 0
    for row in data:
        if row["PKT"].year == r_year and row["PKT"].month == r_month:
            month_length += 1
            sum_highest_temp += row["Max TemperatureC"]
            sum_lowest_temp += row["Min TemperatureC"]
            sum_mean_humidity += row["Mean Humidity"]
    avg_highest_temp = round(sum_highest_temp / month_length, 1)
    avg_lowest_temp = round(sum_lowest_temp / month_length, 1)
    avg_mean_humidity = round(sum_mean_humidity / month_length, 1)
    print(f"Highest Average: {avg_highest_temp}C")
    print(f"Lowest Average: {avg_lowest_temp}C")
    print(f"Average Mean Humidity: {avg_mean_humidity}%")


@year_month_validation_decorator
def get_month_temp_with_bars(data, r_year, r_month) -> None:
    """
    For a given month it draws two horizontal bar charts on the console for the highest
    and lowest temperature on each day. Highest in red and lowest in blue.
    """
    # ANSI escape codes for text colors
    RESET = "\033[0m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    for row in data:
        if row["PKT"].year == r_year and row["PKT"].month == r_month:
            min_temp = int(row["Min TemperatureC"])
            max_temp = int(row["Max TemperatureC"])
            if max_temp:
                high_temp_str = RED
                max_temp = int(row["Max TemperatureC"])
                for _ in range(max_temp):
                    high_temp_str += "+"
                high_temp_str += RESET
            if min_temp:
                low_temp_str = BLUE
                for _ in range(min_temp):
                    low_temp_str += "+"
                low_temp_str += RESET
                temp_str = row["PKT"].strftime("%d") + " "
                temp_str += low_temp_str + high_temp_str + " "
                temp_str += str(min_temp) + "C - " + str(max_temp) + "C"
                print(temp_str)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Weather Report file")
    parser.add_argument(
        "-e", "--year", help="Takes year as input for year report"
    )
    parser.add_argument(
        "-a",
        "--month",
        help="Takes year and month as input for giving month average report",
    )
    parser.add_argument(
        "-c",
        "--month_bar",
        help="Takes year and month as input for giving month average report with colored bars",
    )
    args = parser.parse_args()
    year = args.year
    month = args.month
    month_bar = args.month_bar
    weather_data = read_weather_data()
    if year:
        get_year_report(weather_data, int(year))
    if month:
        get_month_avg_report(weather_data, month)
    if month_bar:
        get_month_temp_with_bars(weather_data, month_bar)
