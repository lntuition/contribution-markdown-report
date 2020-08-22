import sys
import traceback

from base.crawler import crawl_data
from report.language.english import EnglishReportManager


if __name__ == "__main__":
    try:
        _, username, start, end, workdir = sys.argv

        # Fetch date from github
        data = crawl_data(
            username=username,
            start=start,
            end=end,
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
