import sys
import traceback

from lib.collect.crawler import crawl_data
from lib.base.writer import ReportWriter

if __name__ == "__main__":
    try:
        _, username, start, end, workdir = sys.argv

        # Crawl data
        data = crawl_data(
            username=username,
            start=start,
            end=end,
        )

        # Write report
        report = ReportWriter(
            username=username,
            data=data,
            language="english"
        )
        report.write(
            workdir=workdir,
            filename="README.md",
        )

        sys.exit(0)
    except Exception:
        traceback.print_exc()

        sys.exit(1)
