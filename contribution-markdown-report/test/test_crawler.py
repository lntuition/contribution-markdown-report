import numpy as np
import pandas as pd
import pytest
import requests

from crawler import crawl_data
from date import Date, DateInterval


@pytest.mark.skipif(requests.get(f"https://github.com/").status_code != 200, reason="Error at github server, skip test")
@pytest.mark.parametrize(
    ("start, end"),
    [
        ("2019-07-01", "2019-07-01"),
        ("2019-06-03", "2019-06-18"),
        ("2019-07-01", "2019-08-01"),
        ("2019-07-01", "2019-09-01"),
        ("2019-01-01", "2019-12-31"),
        ("2015-01-16", "2020-06-24"),
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
def test_crawl_data(start, end):
    data = crawl_data(
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
