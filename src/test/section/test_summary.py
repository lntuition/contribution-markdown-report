import datetime
import random

from datetime import date

from lib.section.summary import SummaryGenerator
from test.section.test_base import mock_data, mock_language_setting


def test_summary_today_configure(mock_language_setting):
    length = random.randint(1, 1000)
    count = [random.randint(0, 50) for _ in range(length)]
    start = datetime.date(
        year=random.randint(2010, 2015),
        month=random.randint(1, 12),
        day=random.randint(1, 28),
    )
    finish = start + datetime.timedelta(days=length-1)
    print(length, count, start, finish)

    summary = SummaryGenerator(
        data=mock_data(
            count=count,
            start=start,
            finish=finish,
        ),
        setting=mock_language_setting
    )
    config = summary.today_configure()

    assert config["today"] == finish
    assert config["length"] == length
    assert config["count"] == count[-1]
