import pandas as pd
import pytest

from src.collector import Collector
from src.date import dateBuilder, dateRange


@pytest.mark.parametrize(
    ("start_expr", "end_expr", "start_cnt", "end_cnt"),
    [
        ("2017-03-01", "2017-08-15", 3, 8),
        ("2017-06-25", "2018-04-19", 6, 4),
    ],
    ids=[
        "Single Year",
        "Multiple Year",
    ],
)
@pytest.mark.usefixtures("use_snapshot")
def test_collect(start_expr: str, end_expr: str, start_cnt: int, end_cnt: int) -> None:
    data = Collector.collect(
        user="lntuition",
        date_range=dateRange(
            start=dateBuilder.build(start_expr),
            end=dateBuilder.build(end_expr),
        ),
    )

    assert data.user == "lntuition"
    assert data.df.iloc[0]["date"] == pd.Timestamp(start_expr)
    assert data.df.iloc[-1]["date"] == pd.Timestamp(end_expr)
    assert data.df.iloc[0]["count"] == pd.to_numeric(start_cnt)
    assert data.df.iloc[-1]["count"] == pd.to_numeric(end_cnt)
