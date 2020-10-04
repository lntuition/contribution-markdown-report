import pandas as pd
import pytest

from crawler import Crawler
from date import Date, DateInterval


@pytest.mark.parametrize(
    ("date_start", "date_end", "count_start", "count_end"),
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
    use_fake_request: None, date_start: str, date_end: str, count_start: int, count_end: int
) -> None:
    interval = DateInterval(start=Date(date_start), end=Date(date_end))
    data = Crawler.execute(user="lntuition", interval=interval)

    start = data.iloc[0]
    end = data.iloc[-1]

    assert start["date"] == pd.Timestamp(date_start)
    assert end["date"] == pd.Timestamp(date_end)
    assert start["count"] == count_start
    assert end["count"] == count_end
