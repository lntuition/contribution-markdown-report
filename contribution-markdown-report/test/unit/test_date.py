from datetime import datetime, timedelta

import pytest

from date import Date, DateFormatException, DateInterval, DateIntervalException


def test_date_format():
    test_date = "2019-07-01"

    assert str(Date(test_date)) == test_date


def test_date_wrong_format():
    with pytest.raises(DateFormatException):
        Date("2020/01/01")

    with pytest.raises(DateFormatException):
        Date("2020/01/84")

    with pytest.raises(DateFormatException):
        Date("not date format")


def test_date_reserved_format():
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    assert str(Date("yesterday")) == yesterday


def test_date_year_property():
    assert Date("2018-01-03").year == 2018


def test_date_lt():
    assert Date("2018-03-01") < Date("2018-04-01")
    assert not Date("2018-03-01") < Date("2018-03-01")


def test_date_le():
    assert Date("2018-03-01") <= Date("2018-04-01")
    assert Date("2018-03-01") <= Date("2018-03-01")


def test_date_ge():
    assert Date("2018-04-01") >= Date("2018-03-01")
    assert Date("2018-03-01") >= Date("2018-03-01")


def test_date_gt():
    assert Date("2018-04-01") >= Date("2018-03-01")
    assert not Date("2018-03-01") > Date("2018-03-01")


def test_date_int_casting():
    assert int(Date("2016-02-23")) == 20160223


def test_date_interval_wrong():
    with pytest.raises(DateIntervalException):
        DateInterval(start=Date("2018-07-01"), end=Date("2018-06-30"))


def test_date_interval_iter_year():
    assert [2018] == [year for year in DateInterval(start=Date("2018-06-01"), end=Date("2018-06-02")).iter_year()]
    assert [2016, 2017, 2018, 2019] == [
        year for year in DateInterval(start=Date("2016-12-25"), end=Date("2019-01-01")).iter_year()
    ]


def test_date_interval_contains():
    interval = DateInterval(start=Date("2018-07-01"), end=Date("2018-07-22"))

    assert Date("2018-07-15") in interval
    assert not Date("2018-07-23") in interval
