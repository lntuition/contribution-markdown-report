from typing import List

import pytest
from freezegun import freeze_time

from date import Date, DateFormatException, DateInterval, DateIntervalException


def test_date_correct_format() -> None:
    str_date = "2019-07-01"

    date = Date(str_date)

    assert str(date) == str_date


@pytest.mark.parametrize(
    ("str_date"),
    [
        ("2020.01.01"),
        ("2020/01/01"),
        ("2020-13-01"),
        ("2020-01-84"),
        ("fakeformat"),
    ],
)
def test_date_incorrect_format(str_date: str) -> None:
    with pytest.raises(DateFormatException):
        Date(str_date)


@freeze_time("2019-07-02")
def test_date_reserved_format() -> None:
    date = Date("yesterday")

    assert str(date) == "2019-07-01"


@pytest.mark.parametrize(
    ("str_date", "year"),
    [
        ("2020-01-01", 2020),
        ("2019-01-01", 2019),
    ],
    ids=[
        "Even",
        "Odd",
    ],
)
def test_date_year_property(str_date: str, year: int) -> None:
    date = Date(str_date)

    assert date.year == year


@pytest.fixture
def big_date() -> Date:
    yield Date("2018-04-01")


@pytest.fixture
def small_date() -> Date:
    yield Date("2018-03-01")


def test_date_compare_less_than(big_date: Date, small_date: Date) -> None:
    assert small_date < big_date
    assert not big_date < small_date
    assert not small_date < small_date
    assert not big_date < big_date


def test_date_compare_less_equal(big_date: Date, small_date: Date) -> None:
    assert small_date <= big_date
    assert not big_date <= small_date
    assert small_date <= small_date
    assert big_date <= big_date


def test_date_compare_great_than(big_date: Date, small_date: Date) -> None:
    assert not small_date > big_date
    assert big_date > small_date
    assert not small_date > small_date
    assert not big_date > big_date


def test_date_compare_great_equal(big_date: Date, small_date: Date) -> None:
    assert not small_date >= big_date
    assert big_date >= small_date
    assert small_date >= small_date
    assert big_date >= big_date


def test_date_interval_correct_period(big_date: Date, small_date: Date) -> None:
    assert DateInterval(start=small_date, end=big_date)


def test_date_interval_incorrect_period(big_date: Date, small_date: Date) -> None:
    with pytest.raises(DateIntervalException):
        DateInterval(start=big_date, end=small_date)


@pytest.mark.parametrize(
    ("str_start", "str_end", "sequence"),
    [
        ("2018-06-01", "2018-06-01", [2018]),
        ("2018-01-01", "2019-12-31", [2018, 2019]),
        ("2017-07-01", "2020-06-13", [2017, 2018, 2019, 2020]),
    ],
    ids=[
        "Single",
        "Double",
        "Multiple",
    ],
)
def test_date_interval_iter_year(str_start: str, str_end: str, sequence: List[int]) -> None:
    start = Date(str_start)
    end = Date(str_end)
    interval = DateInterval(start, end)

    for result, expected in zip(interval.iter_year(), sequence):
        assert result == expected


def test_date_interval_contains() -> None:
    less = Date("2018-06-29")
    start = Date("2018-07-01")
    between = Date("2018-07-12")
    end = Date("2018-07-23")
    great = Date("2018-07-30")

    interval = DateInterval(start, end)

    assert not less in interval
    assert start in interval
    assert between in interval
    assert end in interval
    assert not great in interval
