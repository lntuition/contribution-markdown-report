import pandas as pd
import pytest

from crawler import Crawler
from date import Date, DateInterval


@pytest.mark.parametrize(
    ("str_start", "str_end", "count_start", "count_end"),
    [
        ("2019-07-01", "2019-07-01", 0, 0),
        ("2019-07-01", "2019-07-16", 0, 1),
        ("2019-07-01", "2019-08-01", 0, 2),
        ("2019-07-01", "2019-09-01", 0, 3),
        ("2019-01-01", "2019-12-31", 0, 7),
        ("2017-01-01", "2020-07-01", 0, 2),
    ],
    ids=[
        "One day",
        "Many days",
        "One month",
        "Many months",
        "One year",
        "Many years",
    ],
)
def test_crawler_execute(
    use_fake_request: None, str_start: str, str_end: str, count_start: int, count_end: int
) -> None:
    date_start = Date(str_start)
    date_end = Date(str_end)
    interval = DateInterval(start=date_start, end=date_end)
    data = Crawler.execute(user="lntuition", interval=interval)

    start = data.iloc[0]
    end = data.iloc[-1]

    assert start["date"] == pd.Timestamp(str_start)
    assert end["date"] == pd.Timestamp(str_end)
    assert start["count"] == pd.to_numeric(count_start)
    assert end["count"] == pd.to_numeric(count_end)
