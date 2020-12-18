from datetime import date
from typing import List

import pandas as pd
import pytest

from src.extractor import Extractor


def __df_for_fetch_series() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "count": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
            "date": pd.date_range("2010-12-27", "2011-01-09"),
        }
    )


def __series_for_fetch_series(group: str, combinator: str, length: int) -> pd.Series:
    if group == "dayofweek":
        index = [0, 1, 2, 3, 4, 5, 6]
        data_map = {
            ("sum", 0): [9, 11, 13, 15, 17, 19, 21],
            ("sum", 10): [8, 9, 10, 11, 17, 19, 21],
            ("mean", 0): [4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5],
            ("mean", 10): [8, 9, 10, 11, 8.5, 9.5, 10.5],
        }
    elif group == "month":
        index = [0, 11]
        data_map = {
            ("sum", 0): [90, 15],
            ("sum", 10): [90, 5],
            ("mean", 0): [10, 3],
            ("mean", 10): [10, 5],
        }
    elif group == "year":
        index = [2010, 2011]
        data_map = {
            ("sum", 0): [15, 90],
            ("sum", 10): [5, 90],
            ("mean", 0): [3, 10],
            ("mean", 10): [5, 10],
        }

    return pd.Series(data_map[(combinator, length)], index)


@pytest.mark.parametrize("group", ["dayofweek", "month", "year"])
@pytest.mark.parametrize("combinator", ["sum", "mean"])
@pytest.mark.parametrize("length", [0, 10])
def test_fetch_series_right_param(group: str, combinator: str, length: int) -> None:
    df = __df_for_fetch_series()

    series = Extractor("", df).fetch_series(group, combinator, length)

    assert __series_for_fetch_series(group, combinator, length).equals(series)


def test_fetch_series_wrong_group() -> None:
    df = __df_for_fetch_series()

    with pytest.raises(Exception):
        Extractor("", df).fetch_series("NOTGROUP", "sum", 0)


def test_fetch_series_wrong_combinator() -> None:
    df = __df_for_fetch_series()

    with pytest.raises(Exception):
        Extractor("", df).fetch_series("dayofweek", "NOTCOMBINATOR", 0)


def test_fetch_series_wrong_length() -> None:
    df = __df_for_fetch_series()

    with pytest.raises(Exception):
        Extractor("", df).fetch_series("dayofweek", "sum", -1)
