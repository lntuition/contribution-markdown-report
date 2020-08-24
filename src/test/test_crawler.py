import numpy as np
import pandas as pd
import pytest
import requests

from base.crawler import ParameterException, RequestException, crawl_data


username = "lntuition"
server_status = (
    requests.get(
        f"https://github.com/{username}"
    ).status_code == 200
)
live_test = pytest.mark.skipif(
    server_status == False,  # server dead
    reason="Error at github server, skip live test"
)
dead_test = pytest.mark.skipif(
    server_status == True,  # server live
    reason="No error at github server, skip dead test"
)


def test_wrong_start_date_fmt():
    with pytest.raises(ParameterException):
        crawl_data(
            username=username,
            start="2020/01/01",
            end="2020-07-01",
        )


def test_wrong_end_date_fmt():
    with pytest.raises(ParameterException):
        crawl_data(
            username=username,
            start="2020-01-01",
            end="2020/07/01",
        )


def test_early_end_than_start():
    with pytest.raises(ParameterException):
        crawl_data(
            username=username,
            start="2020-12-25",
            end="2020-07-01",
        )


@live_test
def test_not_exist_username():
    with pytest.raises(RequestException):
        crawl_data(
            username="ItShouldBeNeverExist",
            start="2020-07-01",
            end="2020-12-25",
        )


@dead_test
def test_crawl_data_on_dead_server():
    with pytest.raises(RequestException):
        crawl_data(
            username=username,
            start="2020-07-01",
            end="2020-12-25",
        )


@live_test
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
    ]
)
def test_crawl_data_on_live_server(start, end):
    data = crawl_data(
        username=username,
        start=start,
        end=end,
    )

    assert pd.Timestamp(start) == data.iloc[0]["date"]
    assert pd.Timestamp(end) == data.iloc[-1]["date"]

    assert isinstance(data.iloc[0]["count"], np.integer)
    assert isinstance(data.iloc[-1]["count"], np.integer)
