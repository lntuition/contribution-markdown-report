import pandas as pd
import requests

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from functools import reduce
from typing import Dict, Iterable


class ParameterException(Exception):
    pass


class RequestException(Exception):
    pass


def _iterate_year(start: str, end: str) -> Iterable[int]:
    fmt = "%Y-%m-%d"

    try:
        begin = datetime.strptime(start, fmt).year
        end = datetime.strptime(end, fmt).year + 1
    except ValueError:
        raise ParameterException(
            f"date string must follow such format({fmt})")

    if begin > end:
        raise ParameterException(
            f"start({start}) must be earlier than end({end})")

    return range(begin, end)


def _fetch_raw_data(url: str) -> Iterable[Dict[str, str]]:
    response = requests.get(url)

    status = response.status_code
    if status != 200:
        raise RequestException(f"status code : {status}")

    # key : data-date, value : %Y-%m-%d format string
    # key : data-count, value : integer-type castable string
    return BeautifulSoup(response.text, "html.parser").select(".day")


def crawl_data(username: str, start: str, end: str) -> pd.DataFrame:
    return pd.DataFrame({
        "count": map(
            lambda x: int(x["data-count"]),
            filter(
                lambda x: start <= x["data-date"] <= end,
                reduce(
                    lambda a, b: a + b,
                    map(
                        lambda x: _fetch_raw_data(
                            f"https://github.com/{username}?from={x}-01-01"
                        ),
                        _iterate_year(start=start, end=end)
                    )
                )
            )
        ),
        "date": pd.date_range(start, end),
    })
