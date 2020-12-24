from datetime import date
from typing import List

import pytest
from freezegun import freeze_time

from src.date import DateRange


def test_range_right_period() -> None:
    try:
        DateRange(
            start=date(2017, 7, 1),
            end=date(2020, 6, 29),
        )
    except Exception as error:
        pytest.fail(f"{error} : Unexpected exception")


def test_range_wrong_period() -> None:
    with pytest.raises(Exception):
        DateRange(
            end=date(2017, 7, 1),
            start=date(2020, 6, 29),
        )


def test_range_iter_year() -> None:
    date_range = DateRange(
        start=date(2017, 7, 1),
        end=date(2020, 6, 29),
    )

    assert date_range.iter_year() == range(2017, 2021, 1)


def test_range_contains() -> None:
    less = date(2018, 6, 29)
    start = date(2018, 7, 1)
    between = date(2018, 7, 12)
    end = date(2018, 7, 23)
    great = date(2018, 7, 30)

    date_range = DateRange(start, end)

    assert not less in date_range
    assert start in date_range
    assert between in date_range
    assert end in date_range
    assert not great in date_range
