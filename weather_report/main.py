"""main.py
"""
import argparse

from report_generator import ReportGenerator
from utils import validate_date


def main() -> None:
    """Call respective functions based on inputs"""
    parser = argparse.ArgumentParser(description="Weather Report file")
    parser.add_argument(
        "-d",
        "--data_dir",
        required=True,
        type=str,
        help="Name of data directory",
    )
    parser.add_argument(
        "-e",
        "--year",
        type=lambda x: validate_date(x, "%Y"),
        help="Year for year report",
    )
    parser.add_argument(
        "-a",
        "--month",
        type=validate_date,
        help="Year and month in format yyyy/mm to generate month average report",
    )
    parser.add_argument(
        "-c",
        "--year_month",
        type=validate_date,
        help="Year and month in format yyyy/mm to generate daily report of month with bars",
    )
    args = parser.parse_args()
    report_generator = ReportGenerator(args.data_dir)
    if args.year:
        report_generator.generate_yearly_extremes_report(args.year)
    if args.month:
        report_generator.generate_monthly_avg_report(args.month)
    if args.year_month:
        report_generator.generate_daily_month_report(args.year_month)


if __name__ == "__main__":
    main()

