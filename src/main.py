import os
import sys
import traceback

from base.crawler import crawl_data
from report.language.english import EnglishReportManager


if __name__ == "__main__":
    try:
        username = os.environ["GITHUB_ACTOR"]
        start_date_str = os.environ["INPUT_START_DATE"]

        # Fetch date from github
        data = crawl_data(username, start_date_str)

        # Generate report
        report = EnglishReportManager()
        report.generate(username, data)

        sys.exit(0)
    except Exception:
        traceback.print_exc()

        sys.exit(1)
