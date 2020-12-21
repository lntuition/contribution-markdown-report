from typing import Dict, List

import pandas as pd


class Extractor:
    def __init__(self, user: str, df: pd.DataFrame) -> None:
        self.__user = user
        self.__df = df

        self.__df["dayofweek"] = df["date"].dt.dayofweek
        self.__df["month"] = df["date"].dt.month - 1
        self.__df["year"] = df["date"].dt.year

    def fetch_series(self, group: str, combinator: str, length: int = 0) -> pd.Series:
        if group not in ["dayofweek", "month", "year"]:
            raise Exception("Not supported group")

        if combinator not in ["sum", "mean"]:
            raise Exception("Not supported combinator")

        if length < 0:
            raise Exception("Length must not be less than 0")

        idx = -min(length, len(self.__df))
        grouped = self.__df[idx:].groupby(group)
        series = getattr(grouped["count"], combinator)()

        return series

    def fetch_cut(
        self,
        length: int = 0,
        bins: List[int] = [-1, 0, 2, 4, 6, 1_000],
        labels: List[str] = ["0", "1-2", "3-4", "5-6", "7+"],
    ) -> pd.Series:
        idx = -min(length, len(self.__df))

        return pd.cut(
            self.__df[idx:]["count"],
            bins=bins,
            labels=labels,
        ).value_counts()
