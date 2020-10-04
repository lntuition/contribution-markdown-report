import numpy as np
import pandas as pd
import pytest

from crawler import Crawler
from date import Date, DateInterval


@pytest.mark.parametrize(
    ("start, end"),
    [
        ("2019-07-01", "2019-07-01"),
        ("2019-06-03", "2019-06-18"),
        ("2019-07-01", "2019-08-01"),
        ("2019-07-01", "2019-09-01"),
        ("2019-01-01", "2019-12-31"),
        ("2017-01-16", "2020-06-24"),
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
def test_crawler_execute(use_fake_request, start, end):
    data = Crawler.execute(
        user="lntuition",
        interval=DateInterval(
            start=Date(start),
            end=Date(end),
        ),
    )

    assert data.iloc[0]["date"] == pd.Timestamp(start)
    assert data.iloc[-1]["date"] == pd.Timestamp(end)

    assert isinstance(data.iloc[0]["count"], np.integer)
    assert isinstance(data.iloc[-1]["count"], np.integer)
