import os
from datetime import date, timedelta
from typing import Sequence, Union
from unittest.mock import MagicMock, patch
from urllib.parse import parse_qs, urlparse

import pandas as pd
import pytest

from src.contribution import ContributionInfo, ContributionInfoCollector
from src.date import Date


def _fake_requests_get(url: str) -> MagicMock:
    parts = urlparse(url)
    query_string = parse_qs(parts.query)

    snapshot_path = os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__),
            )
        ),
        "asset",
        f"{query_string['from'][0][:4]}_snapshot.html",
    )

    if os.path.isfile(snapshot_path):
        status_code = 200
        with open(snapshot_path, "r") as snapshot:
            text = snapshot.read()
    else:
        status_code = 404
        text = "Not found"

    mock_response = MagicMock()
    mock_response.status_code = status_code
    mock_response.text = text

    return mock_response


@pytest.mark.parametrize(
    ("str_start", "str_end", "count_start", "count_end"),
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
class TestContributionInfoCollectorSuccess:
    @staticmethod
    def __test_template(str_start: str, str_end: str, count_start: int, count_end: int) -> None:
        user = "lntuition"
        date_start = Date(str_start)
        date_end = Date(str_end)

        info = ContributionInfoCollector(user=user, start=date_start, end=date_end).collect()

        assert info.user == user
        assert info.brief == f"{user}'s contribution report on {date_end}"
        assert info.dataframe.iloc[0]["date"] == pd.Timestamp(str_start)
        assert info.dataframe.iloc[-1]["date"] == pd.Timestamp(str_end)
        assert info.dataframe.iloc[0]["count"] == pd.to_numeric(count_start)
        assert info.dataframe.iloc[-1]["count"] == pd.to_numeric(count_end)

    @patch("requests.get", wraps=_fake_requests_get)
    def test_with_patch(self, _, str_start: str, str_end: str, count_start: int, count_end: int) -> None:
        self.__test_template(str_start, str_end, count_start, count_end)

    @pytest.mark.usefixtures("live_server")
    def test_with_live_server(self, str_start: str, str_end: str, count_start: int, count_end: int) -> None:
        self.__test_template(str_start, str_end, count_start, count_end)


class TestContributionInfoCollectorFail:
    @staticmethod
    def __test_template(user: str, start: Date, end: Date) -> None:
        with pytest.raises(Exception):
            ContributionInfoCollector(
                user=user,
                start=start,
                end=end,
            ).collect()

    @patch("requests.get", wraps=_fake_requests_get)
    def test_with_patch(self, _) -> None:
        self.__test_template(user="lntuition", start=Date("2011-01-01"), end=Date("2011-01-01"))

    @pytest.mark.usefixtures("dead_server")
    def test_with_dead_server(self) -> None:
        self.__test_template(user="lntuition", start=Date("2019-07-01"), end=Date("2019-07-01"))


class TestContributionInfo:
    @staticmethod
    def _contribution_info_only_dataframe(
        counts: Sequence[int], start: Union[str, date], end: Union[str, date]
    ) -> ContributionInfo:
        return ContributionInfo(
            user="",
            brief="",
            dataframe=pd.DataFrame(
                {
                    "count": counts,
                    "date": pd.date_range(start, end),
                }
            ),
        )

    def test_today(self) -> None:
        counts = [0, 1, 2, 3, 4]
        start = "2019-07-01"
        end = "2019-07-05"

        info = self._contribution_info_only_dataframe(counts=counts, start=start, end=end)
        today = info.today()

        assert today["date"] == pd.Timestamp(end)
        assert today["count"] == counts[-1]
        assert today["length"] == len(counts)

    def test_maximum(self) -> None:
        counts = [0, 4, 2, 3, 1]
        start = "2019-07-01"
        end = "2019-07-05"

        maximum_date = "2019-07-02"
        maximum_count = 4

        info = self._contribution_info_only_dataframe(counts=counts, start=start, end=end)
        maximun = info.maximum()

        assert maximun["date"] == pd.Timestamp(maximum_date)
        assert maximun["count"] == maximum_count

    def test_total(self) -> None:
        counts = [0, 4, 3, 3, 1]
        start = "2019-07-01"
        end = "2019-07-05"

        info = self._contribution_info_only_dataframe(counts=counts, start=start, end=end)
        total = info.total()

        assert total["_sum"] == sum(counts)
        assert total["avg"] == sum(counts) / len(counts)

    @pytest.mark.parametrize(
        ("start", "end", "peak_start", "peak_length", "counts"),
        [
            ("2019-07-01", "2019-07-05", "2019-07-01", 5, [1, 1, 2, 1, 3]),
            ("2019-07-01", "2019-07-07", "2019-07-06", 2, [1, 0, 1, 2, 0, 3, 2]),
            ("2019-07-01", "2019-07-02", "2019-07-02", 1, [0, 2]),
            ("2019-07-01", "2019-07-01", "2019-07-01", 0, [0]),
        ],
        ids=[
            "All days",
            "Many days",
            "One day",
            "No day",
        ],
    )
    def test_today_peak(self, counts: Sequence[int], start: str, end: str, peak_start: str, peak_length: int) -> None:
        info = self._contribution_info_only_dataframe(counts=counts, start=start, end=end)
        today_peak = info.today_peak()

        assert today_peak["start_date"] == pd.Timestamp(peak_start)
        assert today_peak["length"] == peak_length

    @pytest.mark.parametrize(
        ("start", "end", "peak_start", "peak_end", "peak_length", "counts"),
        [
            ("2019-07-01", "2019-07-05", "2019-07-01", "2019-07-05", 5, [1, 1, 2, 1, 3]),
            ("2019-07-01", "2019-07-08", "2019-07-03", "2019-07-05", 3, [1, 0, 1, 2, 3, 0, 3, 2]),
            ("2019-07-01", "2019-07-02", "2019-07-01", "2019-07-01", 1, [2, 0]),
            ("2019-07-01", "2019-07-02", "2019-07-02", "2019-07-02", 1, [0, 2]),
            ("2019-07-01", "2019-07-01", "2019-07-01", "2019-07-01", 0, [0]),
        ],
        ids=[
            "All days",
            "Many days",
            "One day:start",
            "One day:end",
            "No day",
        ],
    )
    def test_maximum_peak(
        self, counts: Sequence[int], start: str, end: str, peak_start: str, peak_end: str, peak_length: int
    ) -> None:
        info = self._contribution_info_only_dataframe(counts=counts, start=start, end=end)
        maximum_peak = info.maximum_peak()

        assert maximum_peak["start_date"] == pd.Timestamp(peak_start)
        assert maximum_peak["end_date"] == pd.Timestamp(peak_end)
        assert maximum_peak["length"] == peak_length

    def test_count_sum_recent_under(self) -> None:
        start = "2019-07-01"
        end = "2019-07-10"

        counts = [0, 1, 2, 3, 4, 5, 6, 7, 6, 5]
        counter = {
            "0": 1,
            "1-2": 2,
            "3-4": 2,
            "5-6": 4,
            "7+": 1,
        }

        info = self._contribution_info_only_dataframe(counts=counts, start=start, end=end)
        count_sum_recent = info.count_sum_recent()

        for key, val in count_sum_recent.items():
            assert val == counter[key]

    @pytest.mark.parametrize(
        ("offset"),
        [0, 1, 10, 48],
        ids=lambda offset: f"{offset} days",
    )
    def test_count_sum_recent_over(self, offset: int) -> None:
        start = "2019-07-01"
        end = date(2019, 7, 28) + timedelta(days=offset)

        counts = [100] * offset + [0, 1, 2, 3, 4, 5, 6, 7] + [0] * 20
        counter = {
            "0": 21,
            "1-2": 2,
            "3-4": 2,
            "5-6": 2,
            "7+": 1,
        }

        info = self._contribution_info_only_dataframe(counts=counts, start=start, end=end)
        count_sum_recent = info.count_sum_recent()

        for key, val in count_sum_recent.items():
            assert val == counter[key]

    @pytest.mark.parametrize(
        ("offset"),
        range(9),
        ids=lambda offset: f"{offset+8} days",
    )
    def test_count_sum_full(self, offset: int) -> None:
        start = "2019-07-01"
        end = date(2019, 7, 8) + timedelta(days=offset)

        counts_key = ["0", "1-2", "1-2", "3-4", "3-4", "5-6", "5-6", "7+"]
        counts_val = [0, 1, 2, 3, 4, 5, 6, 7]
        counter = {
            "0": 1,
            "1-2": 2,
            "3-4": 2,
            "5-6": 2,
            "7+": 1,
        }

        counts = counts_val
        for i in range(offset):
            count_val = counts_val[i % 8]
            count_key = counts_key[i % 8]

            counts.append(count_val)
            counter[count_key] += 1

        info = self._contribution_info_only_dataframe(counts=counts, start=start, end=end)
        count_sum_full = info.count_sum_full()

        for key, val in count_sum_full.items():
            assert val == counter[key]

    def test_dayofweek_sum_recent_under(self):
        start = "2019-07-01"
        end = "2019-07-23"

        counts_by_dayofweek = [513, 127, 366, 378, 118, 923, 854]
        counts = counts_by_dayofweek + [0] * 16

        info = self._contribution_info_only_dataframe(counts=counts, start=start, end=end)
        dayofweek_sum_recent = info.dayofweek_sum_recent()

        for key, val in dayofweek_sum_recent.items():
            assert val == counts_by_dayofweek[key]

    @pytest.mark.parametrize(
        ("offset"),
        [0, 1, 7, 20, 43],
        ids=lambda offset: f"{offset} days",
    )
    def test_dayofweek_sum_recent_over(self, offset: int) -> None:
        start = "2019-07-01"
        end = date(2019, 10, 20) + timedelta(days=offset)

        counts_by_dayofweek = [513, 127, 366, 378, 118, 923, 854]
        counts = [1] * offset + counts_by_dayofweek + [0] * 105

        info = self._contribution_info_only_dataframe(counts=counts, start=start, end=end)
        dayofweek_sum_recent = info.dayofweek_sum_recent()

        for key, val in dayofweek_sum_recent.items():
            assert val == counts_by_dayofweek[key - offset % 7]

    @pytest.mark.parametrize(
        ("offset"),
        range(8),
        ids=lambda offset: f"{offset+7} days",
    )
    def test_dayofweek_mean_full(self, offset: int) -> None:
        start = "2019-07-01"
        end = date(2019, 7, 7) + timedelta(days=offset)

        counts_by_dayofweek = [157, 831, 293, 421, 389, 520, 235]
        counts = counts_by_dayofweek + [0] * offset

        days_by_dayofweek = [1, 1, 1, 1, 1, 1, 1]
        for i in range(offset):
            days_by_dayofweek[i % 7] += 1

        info = self._contribution_info_only_dataframe(counts=counts, start=start, end=end)
        dayofweek_mean_full = info.dayofweek_mean_full()

        for key, val in dayofweek_mean_full.items():
            assert val == counts_by_dayofweek[key] / days_by_dayofweek[key]

    def test_month_sum_recent_under(self) -> None:
        start = "2019-08-15"
        end = "2019-12-31"

        counts_by_month = {
            7: [123] + [0] * 16,  # Aug
            8: [498] + [0] * 29,  # Sep
            9: [158] + [0] * 30,  # Oct
            10: [783] + [0] * 29,  # Nov
            11: [154] + [0] * 30,  # Dec
        }
        counts = []
        for val in counts_by_month.values():
            counts += val

        info = self._contribution_info_only_dataframe(counts=counts, start=start, end=end)
        month_sum_recent = info.month_sum_recent()

        for key, val in month_sum_recent.items():
            assert val == sum(counts_by_month[key])

    @pytest.mark.parametrize(
        ("offset"),
        [0, 1, 97, 365, 366],
        ids=lambda offset: f"{offset} days",
    )
    def test_month_sum_recent_over(self, offset: int) -> None:
        start = date(2019, 1, 1) - timedelta(days=offset)
        end = "2019-12-31"

        counts_by_month = {
            0: [513] + [0] * 30,  # Jan
            1: [127] + [0] * 27,
            2: [366] + [0] * 30,
            3: [378] + [0] * 29,
            4: [118] + [0] * 30,
            5: [923] + [0] * 29,
            6: [854] + [0] * 30,
            7: [123] + [0] * 30,
            8: [498] + [0] * 29,
            9: [158] + [0] * 30,
            10: [783] + [0] * 29,
            11: [154] + [0] * 30,  # Dec
        }
        counts = [715] * offset
        for val in counts_by_month.values():
            counts += val

        info = self._contribution_info_only_dataframe(counts=counts, start=start, end=end)
        month_sum_recent = info.month_sum_recent()

        for key, val in month_sum_recent.items():
            assert val == sum(counts_by_month[key])

    def test_year_sum_full(self) -> None:
        start = "2017-03-01"
        end = "2020-09-21"

        counts_by_year = {
            2017: [198] + [0] * 305,
            2018: [233] + [0] * 364,
            2019: [978] + [0] * 364,
            2020: [354] + [0] * 264,
        }
        counts = []
        for val in counts_by_year.values():
            counts += val

        info = self._contribution_info_only_dataframe(counts=counts, start=start, end=end)
        year_sum_full = info.year_sum_full()

        for key, val in year_sum_full.items():
            assert val == sum(counts_by_year[key])
