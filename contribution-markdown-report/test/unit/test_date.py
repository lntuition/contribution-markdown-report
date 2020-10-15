from typing import List

import pytest
from freezegun import freeze_time

from src.date import Date, DateInterval


@pytest.fixture
def big_date() -> Date:
    yield Date("2018-04-01")


@pytest.fixture
def small_date() -> Date:
    yield Date("2018-03-01")


class TestDate:
    def test_correct_format(self) -> None:
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
            ("Notdate"),
        ],
    )
    def test_incorrect_format(self, str_date: str) -> None:
        with pytest.raises(Exception):
            Date(str_date)

    @freeze_time("2019-07-02")
    def test_reserved_format(self) -> None:
        date = Date("yesterday")

        assert str(date) == "2019-07-01"

    def test_year_property(self) -> None:
        date = Date("2020-01-01")

        assert date.year == 2020

    def test_compare_less_than(self, big_date: Date, small_date: Date) -> None:
        assert small_date < big_date
        assert not big_date < small_date
        assert not small_date < small_date
        assert not big_date < big_date

    def test_compare_less_equal(self, big_date: Date, small_date: Date) -> None:
        assert small_date <= big_date
        assert not big_date <= small_date
        assert small_date <= small_date
        assert big_date <= big_date

    def test_compare_great_than(self, big_date: Date, small_date: Date) -> None:
        assert not small_date > big_date
        assert big_date > small_date
        assert not small_date > small_date
        assert not big_date > big_date

    def test_compare_great_equal(self, big_date: Date, small_date: Date) -> None:
        assert not small_date >= big_date
        assert big_date >= small_date
        assert small_date >= small_date
        assert big_date >= big_date


class TestDateInterval:
    def test_correct_period(self, big_date: Date, small_date: Date) -> None:
        assert DateInterval(start=small_date, end=big_date)

    def test_incorrect_period(self, big_date: Date, small_date: Date) -> None:
        with pytest.raises(Exception):
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
    def test_iter_year(self, str_start: str, str_end: str, sequence: List[int]) -> None:
        start = Date(str_start)
        end = Date(str_end)
        interval = DateInterval(start, end)

        for result, expected in zip(interval.iter_year(), sequence):
            assert result == expected

    def test_contains(self) -> None:
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
