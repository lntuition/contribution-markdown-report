from datetime import date
from typing import Mapping

import pandas as pd
import pytest

from src.extractor import Extractor


def __extractor() -> Extractor:
    return Extractor(
        user="lntuition",
        df=pd.DataFrame(
            {
                "count": [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 11, 12, 15, 13],
                "date": pd.date_range("2010-12-27", "2011-01-09"),
            }
        ),
    )


def __expected_series(group: str, combinator: str, length: int) -> pd.Series:
    if group == "dayofweek":
        idx = [0, 1, 2, 3, 4, 5, 6]
        data_map = {
            ("sum", 0): [9, 11, 3, 15, 17, 21, 20],
            ("sum", 10): [8, 9, 0, 11, 17, 21, 20],
            ("mean", 0): [4.5, 5.5, 1.5, 7.5, 8.5, 10.5, 10],
            ("mean", 10): [8, 9, 0, 11, 8.5, 10.5, 10],
        }
    elif group == "month":
        idx = [0, 11]
        data_map = {
            ("sum", 0): [81, 15],
            ("sum", 10): [81, 5],
            ("mean", 0): [9, 3],
            ("mean", 10): [9, 5],
        }
    elif group == "year":
        idx = [2010, 2011]
        data_map = {
            ("sum", 0): [15, 81],
            ("sum", 10): [5, 81],
            ("mean", 0): [3, 9],
            ("mean", 10): [5, 9],
        }

    data = data_map[(combinator, length)]

    return pd.Series(data, idx)


def __expected_cut(length: int) -> pd.Series:
    idx = ["0", "1-2", "3-4", "5-6", "7+"]
    if length == 0:
        data = [1, 2, 2, 2, 7]
    elif length == 10:
        data = [1, 0, 0, 2, 7]

    return pd.Series(data, idx)


def __expected_map(key: str) -> Mapping[str, str]:
    if key == "total":
        return {
            "sum": "96",
            "avg": "6.86",
        }
    elif key == "today":
        return {
            "date": "2011-01-09",
            "count": "13",
            "length": "14",
        }
    elif key == "today-peak":
        return {
            "start": "2011-01-06",
            "length": "4",
        }
    elif key == "max":
        return {
            "date": "2011-01-08",
            "count": "15",
        }
    elif key == "max-peak":
        return {
            "start": "2010-12-27",
            "end": "2011-01-04",
            "length": "9",
        }


def test_fetch_user() -> None:
    ret = __extractor().fetch_user()

    assert "lntuition" == ret


@pytest.mark.parametrize("group", ["dayofweek", "month", "year"])
@pytest.mark.parametrize("combinator", ["sum", "mean"])
@pytest.mark.parametrize("length", [0, 10])
def test_fetch_series(group: str, combinator: str, length: int) -> None:
    ret = __extractor().fetch_series(group, combinator, length).sort_index()

    assert __expected_series(group, combinator, length).equals(ret)


def test_fetch_series_wrong_group() -> None:
    with pytest.raises(Exception):
        __extractor().fetch_series("NOTGROUP", "sum", 0)


def test_fetch_series_wrong_combinator() -> None:
    with pytest.raises(Exception):
        __extractor().fetch_series("dayofweek", "NOTCOMBINATOR", 0)


def test_fetch_series_wrong_length() -> None:
    with pytest.raises(Exception):
        __extractor().fetch_series("dayofweek", "sum", -1)


@pytest.mark.parametrize("length", [0, 10])
def test_fetch_cut(length: int) -> None:
    ret = __extractor().fetch_cut(length).sort_index()

    assert __expected_cut(length).equals(ret)


@pytest.mark.parametrize("key", ["total", "today", "today-peak", "max", "max-peak"])
def test_fetch_map(key: str) -> None:
    ret = __extractor().fetch_map(key)

    assert __expected_map(key) == ret


def test_fetch_map_wrong_key() -> None:
    with pytest.raises(Exception):
        __extractor().fetch_map("NOTKEY")
