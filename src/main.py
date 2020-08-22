import sys
import traceback

from base.crawler import crawl_data
from report.language.english import EnglishReportManager


if __name__ == "__main__":
    try:
        _, username, start_date_str, workdir = sys.argv

        # Fetch date from github
        data = crawl_data(
            username=username,
            start_date_str=start_date_str
        )

        # Generate report
        report = EnglishReportManager()
        report.generate(
            username=username,
            data=data,
            workdir=workdir
        )

        sys.exit(0)
    except Exception:
        traceback.print_exc()

        sys.exit(1)
