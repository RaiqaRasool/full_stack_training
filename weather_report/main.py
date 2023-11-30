"""main.py
"""
import argparse

from report_generator import ReportGenerator


def main() -> None:
    """Call respective functions based on inputs
    """
    parser = argparse.ArgumentParser(description="Weather Report file")
    parser.add_argument(
        "-e",
        "--year",
        type=int,
        help="Takes year as input for year report"
    )
    parser.add_argument(
        "-a",
        "--month",
        help="Year and month to generate month average report",
    )
    parser.add_argument(
        "-c",
        "--year_month",
        help="Year and month to generate daily report of month with bars",
    )
    args = parser.parse_args()
    report_generator = ReportGenerator()
    if args.year:
        report_generator.yearly_extremes_report(args.year)
    if args.month:
        report_generator.monthly_avg_report(args.month)
    if args.year_month:
        report_generator.daily_month_report(args.year_month)


if __name__ == "__main__":
    main()


