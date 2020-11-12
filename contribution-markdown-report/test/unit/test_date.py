from datetime import date
from typing import List

import pytest
from freezegun import freeze_time

from src.date import dateBuilder, dateRange


class TestdateBuilder:
    def test_correct_format(self) -> None:
        assert dateBuilder.build("2019-07-01") == date(2019, 7, 1)

    @pytest.mark.parametrize(
        ("expr"),
        [
            ("2020.01.01"),
            ("2020/01/01"),
            ("2020-13-01"),
            ("2020-01-84"),
            ("JUSTSTRING"),
        ],
    )
    def test_incorrect_format(self, expr: str) -> None:
        with pytest.raises(Exception):
            dateBuilder.build(expr)

    @freeze_time("2019-07-02")
    def test_reserved_format(self) -> None:
        assert dateBuilder.build("yesterday") == date(2019, 7, 1)


class TestdateInterval:
    @classmethod
    def setup_class(cls):
        cls.start = date(2017, 7, 1)
        cls.end = date(2020, 6, 29)

    def test_correct_period(self) -> None:
        try:
            dateRange(self.start, self.end)
        except Exception as error:
            pytest.fail(f"{error} : Unexpected exception")

    def test_incorrect_period(self) -> None:
        with pytest.raises(Exception):
            dateRange(self.end, self.start)

    def test_iter_year(self) -> None:
        date_range = dateRange(self.start, self.end)

        assert [year for year in date_range.iter_year()] == [2017, 2018, 2019, 2020]

    def test_contains(self) -> None:
        less = date(2018, 6, 29)
        start = date(2018, 7, 1)
        between = date(2018, 7, 12)
        end = date(2018, 7, 23)
        great = date(2018, 7, 30)

        date_range = dateRange(start, end)

        assert not less in date_range
        assert start in date_range
        assert between in date_range
        assert end in date_range
        assert not great in date_range
