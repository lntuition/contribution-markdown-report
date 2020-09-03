import pandas as pd
import requests

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from functools import reduce
from typing import cast, Dict, List, Sequence


RawData = List[Dict[str, str]]


class ParameterException(Exception):
    pass


class RequestException(Exception):
    pass


def _iterate_year(start: str, finish: str) -> Sequence[int]:
    fmt = "%Y-%m-%d"

    try:
        begin = datetime.strptime(start, fmt)
        end = datetime.strptime(finish, fmt)
    except ValueError:
        raise ParameterException(
            f"date string must follow such format({fmt})")

    if begin > end:
        raise ParameterException(
            f"start({start}) must be earlier than finish({finish})")

    return range(begin.year, end.year + 1)


def _fetch_raw_data(url: str) -> RawData:
    response = requests.get(url)

    status = response.status_code
    if status != 200:
        raise RequestException(f"status code : {status}")

    # key : data-date, value : %Y-%m-%d format string
    # key : data-count, value : integer-type castable string
    return BeautifulSoup(response.text, "html.parser").select(".day")


def crawl_data(username: str, start: str, finish: str) -> pd.DataFrame:
    return pd.DataFrame({
        "count": map(
            lambda x: int(x["data-count"]),
            filter(
                lambda x: start <= x["data-date"] <= finish,
                reduce(
                    lambda a, b: cast(RawData, a) + cast(RawData, b),
                    map(
                        lambda x: _fetch_raw_data(
                            f"https://github.com/{username}?from={x}-01-01"
                        ),
                        _iterate_year(start=start, finish=finish)
                    ),
                )
            )
        ),
        "date": pd.date_range(start, finish),
    })
