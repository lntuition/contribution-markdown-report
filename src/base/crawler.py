from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from requests import get
from typing import Dict


CrawledDataType = Dict[datetime, int]


class RequestException(Exception):
    pass


def crawl_data(username: str, start_date_str: str) -> CrawledDataType:
    data = {}

    date_format = "%Y-%m-%d"
    start = datetime.strptime(start_date_str, date_format)
    end = datetime.today() - timedelta(days=1)

    for year in range(start.year, end.year + 1):
        response = get(f"https://github.com/{username}?from={year}-01-01")

        status = response.status_code
        if status != 200:
            raise RequestException(f"status code : {status}")

        html = BeautifulSoup(response.text, "html.parser")
        for element in html.select(".day"):
            date = datetime.strptime(element["data-date"], date_format)

            if date < start:
                continue
            elif date > end:
                break

            # After python 3.6 dict acts like OrderedDict
            data[date] = int(element["data-count"])

    return data
