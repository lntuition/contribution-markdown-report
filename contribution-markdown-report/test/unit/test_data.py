import os
from datetime import date
from typing import Dict
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.data import ContributionData, ContributionDataBuilder
from src.date import dateBuilder, dateRange


def fake_fetch_text(url: str, params: Dict[str, str]) -> str:
    snapshot_path = os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__),
            )
        ),
        "asset",
        f"{params['from'][:4]}_snapshot.html",
    )

    with open(snapshot_path, "r") as snapshot:
        return snapshot.read()


class TestContributionDataBuilder:
    @pytest.mark.parametrize(
        ("start_expr", "end_expr", "start_cnt", "end_cnt"),
        [
            ("2019-07-01", "2019-07-01", 0, 0),
            ("2019-07-01", "2019-07-16", 0, 1),
            ("2019-07-01", "2019-08-01", 0, 2),
            ("2019-07-01", "2019-09-01", 0, 3),
            ("2019-01-01", "2019-12-31", 0, 7),
            ("2017-01-01", "2020-07-01", 0, 2),
        ],
        ids=[
            "One day",
            "Many days",
            "One month",
            "Many months",
            "One year",
            "Many years",
        ],
    )
    @patch("src.request.Request.fetch_text", wraps=fake_fetch_text)
    def test_build(
        self,
        _: MagicMock,
        start_expr: str,
        end_expr: str,
        start_cnt: int,
        end_cnt: int,
    ) -> None:
        user = "lntuition"
        date_range = dateRange(
            start=dateBuilder.build(start_expr),
            end=dateBuilder.build(end_expr),
        )

        data = ContributionDataBuilder.build(user, date_range)

        assert data.user == user
        assert data.df.iloc[0]["date"] == pd.Timestamp(start_expr)
        assert data.df.iloc[-1]["date"] == pd.Timestamp(end_expr)
        assert data.df.iloc[0]["count"] == pd.to_numeric(start_cnt)
        assert data.df.iloc[-1]["count"] == pd.to_numeric(end_cnt)
