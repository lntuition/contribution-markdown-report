from typing import List, Mapping, cast

import pandas as pd


class Extractor:
    def __init__(self, user: str, df: pd.DataFrame) -> None:
        self.__user = user
        self.__df = df

        exist = df["count"] > 0

        self.__df["dayofweek"] = df["date"].dt.dayofweek
        self.__df["month"] = df["date"].dt.month - 1
        self.__df["year"] = df["date"].dt.year
        self.__df["peak"] = exist * (exist.groupby((exist != exist.shift()).cumsum()).cumcount() + 1)

    def fetch_user(self) -> str:
        return self.__user

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

    @staticmethod
    def __fmt_float(f: float) -> float:
        return round(f, 2)

    @staticmethod
    def __fmt_timestamp(ts: pd.Timestamp) -> str:
        return ts.strftime("%Y-%m-%d")

    def fetch_map(self, key: str) -> Mapping[str, str]:
        key = key.lower()

        if key == "total":
            count = self.__df["count"]
            return {
                "sum": count.sum(),
                "avg": cast(
                    str,
                    self.__fmt_float(
                        count.mean(),
                    ),
                ),
            }
        elif key == "today":
            row = self.__df.iloc[-1]
            return {
                "date": self.__fmt_timestamp(row["date"]),
                "count": row["count"],
                "length": cast(
                    str,
                    len(self.__df),
                ),
            }
        elif key == "today-peak":
            end = self.__df.iloc[-1]
            start = self.__df.iloc[-1 - max(0, end["peak"] - 1)]
            return {
                "start": self.__fmt_timestamp(start["date"]),
                "length": end["peak"],
            }
        elif key == "max":
            row = self.__df.iloc[self.__df["count"].idxmax()]
            return {
                "date": self.__fmt_timestamp(row["date"]),
                "count": row["count"],
            }
        elif key == "max-peak":
            idx = self.__df["peak"].idxmax()
            end = self.__df.iloc[idx]
            start = self.__df.iloc[idx - max(0, end["peak"] - 1)]
            return {
                "start": self.__fmt_timestamp(start["date"]),
                "end": self.__fmt_timestamp(end["date"]),
                "length": end["peak"],
            }
        else:
            raise Exception(f"Not supported key : {key}")
