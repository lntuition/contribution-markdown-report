from datetime import date
from typing import Dict, Union

import pandas as pd
import requests
from bs4 import BeautifulSoup

from .date import DateBuilder, DateRange


class ContributionInfo:
    def __init__(self, user: str, brief: str, dataframe: pd.DataFrame) -> None:
        self.__user = user
        self.__brief = brief
        self.__dataframe = dataframe

        self.__add_continous_col()
        self.__add_dayofweek_col()
        self.__add_month_col()
        self.__add_year_col()

        self.__dataframe_len = len(dataframe)
        self.__bins = [-1, 0, 2, 4, 6, 1_000_000]  # Over millions not concerned
        self.__labels = ["0", "1-2", "3-4", "5-6", "7+"]

    @property
    def user(self) -> str:
        return self.__user

    @property
    def brief(self) -> str:
        return self.__brief

    @property
    def dataframe(self) -> pd.DataFrame:
        # Expose for testing, not using this directly
        return self.__dataframe

    def __add_continous_col(self) -> None:
        exist = pd.Series(data=self.__dataframe["count"] > 0)
        continous = exist * (exist.groupby((exist != exist.shift()).cumsum()).cumcount() + 1)

        self.__dataframe["continous"] = continous

    def __add_dayofweek_col(self) -> None:
        self.__dataframe["dayofweek"] = self.__dataframe["date"].dt.dayofweek

    def __add_month_col(self) -> None:
        self.__dataframe["month"] = self.__dataframe["date"].dt.month - 1

    def __add_year_col(self) -> None:
        self.__dataframe["year"] = self.__dataframe["date"].dt.year

    def today(self) -> Dict[str, Union[pd.Timestamp, int]]:
        idx = -1
        row = self.__dataframe.iloc[idx]

        return {
            "date": row["date"],
            "count": row["count"],
            "length": self.__dataframe_len,
        }

    def maximum(self) -> Dict[str, Union[pd.Timestamp, int]]:
        idx = self.__dataframe["count"].idxmax()
        row = self.__dataframe.iloc[idx]

        return {
            "date": row["date"],
            "count": row["count"],
        }

    def total(self) -> Dict[str, Union[int, float]]:
        return {
            "_sum": self.__dataframe["count"].sum(),
            "avg": round(self.__dataframe["count"].mean(), 2),
        }

    def today_peak(self) -> Dict[str, Union[pd.Timestamp, int]]:
        end_idx = -1
        end_row = self.__dataframe.iloc[end_idx]

        start_idx = end_idx - max(0, end_row["continous"] - 1)
        start_row = self.__dataframe.iloc[start_idx]

        return {
            "start_date": start_row["date"],
            "length": end_row["continous"],
        }

    def maximum_peak(self) -> Dict[str, Union[pd.Timestamp, int]]:
        end_idx = self.__dataframe["continous"].idxmax()
        end_row = self.__dataframe.iloc[end_idx]

        start_idx = end_idx - max(0, end_row["continous"] - 1)
        start_row = self.__dataframe.iloc[start_idx]

        return {
            "start_date": start_row["date"],
            "end_date": end_row["date"],
            "length": end_row["continous"],
        }

    def count_sum_recent(self) -> pd.Series:
        slice_idx = max(-28, -self.__dataframe_len)

        return pd.cut(
            self.__dataframe[slice_idx:]["count"],
            bins=self.__bins,
            labels=self.__labels,
        ).value_counts()

    def count_sum_full(self) -> pd.Series:
        return pd.cut(
            self.__dataframe["count"],
            bins=self.__bins,
            labels=self.__labels,
        ).value_counts()

    def dayofweek_sum_recent(self) -> pd.Series:
        slice_idx = max(-112, -self.__dataframe_len)

        return self.__dataframe[slice_idx:].groupby("dayofweek")["count"].sum()

    def dayofweek_mean_full(self) -> pd.Series:
        return self.__dataframe.groupby("dayofweek")["count"].mean()

    def month_sum_recent(self) -> pd.Series:
        slice_idx = max(-365, -self.__dataframe_len)

        return self.__dataframe[slice_idx:].groupby("month")["count"].sum()

    def year_sum_full(self) -> pd.Series:
        return self.__dataframe.groupby("year")["count"].sum()


class ContributionInfoCollector:
    def __init__(self, user: str, start: date, end: date) -> None:
        self.__user = user
        self.__start = start
        self.__end = end

    @staticmethod
    def __fetch_text(url: str) -> str:
        response = requests.get(url)

        status = response.status_code
        if status != 200:
            raise Exception(f"{status} : Failed to get text")

        return response.text

    def collect(self) -> ContributionInfo:
        date_range = DateRange(start=self.__start, end=self.__end)

        data = []
        for year in date_range.iter_year():
            url = f"https://github.com/{self.__user}?from={year}-01-01"
            text = self.__fetch_text(url)

            for rect in BeautifulSoup(text, "html.parser").findAll("rect"):
                rect_date, rect_count = rect["data-date"], rect["data-count"]

                if DateBuilder.build(rect_date) in date_range:
                    column = [
                        pd.to_numeric(rect_count),
                        pd.Timestamp(rect_date),
                    ]

                    data.append(column)

        brief = f"{self.__user}'s contribution report on {self.__end}"
        dataframe = pd.DataFrame(data=data, columns=["count", "date"])

        return ContributionInfo(user=self.__user, brief=brief, dataframe=dataframe)
