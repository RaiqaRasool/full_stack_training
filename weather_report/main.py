"""main.py
"""
import argparse
from datetime import datetime

from report_generator import ReportGenerator


def main() -> None:
    """Call respective functions based on inputs"""
    parser = argparse.ArgumentParser(description="Weather Report file")
    parser.add_argument(
        "-d",
        "--data_folder",
        required=True,
        type=str,
        help="Data folder name",
    )
    parser.add_argument(
        "-e",
        "--year",
        type=lambda x: datetime.strptime(x, "%Y"),
        help="Year for year report",
    )
    parser.add_argument(
        "-a",
        "--month",
        type=lambda x: datetime.strptime(x, "%Y/%m"),
        help="Year and month in format yyyy/mm to generate month average report",
    )
    parser.add_argument(
        "-c",
        "--year_month",
        type=lambda x: datetime.strptime(x, "%Y/%m"),
        help="Year and month in format yyyy/mm to generate daily report of month with bars",
    )
    args = parser.parse_args()
    report_generator = ReportGenerator(args.data_folder)
    if args.year:
        report_generator.yearly_extremes_report(args.year)
    if args.month:
        report_generator.monthly_avg_report(args.month)
    if args.year_month:
        report_generator.daily_month_report(args.year_month)


if __name__ == "__main__":
    main()
