import pandas as pd

from datetime import datetime

from lib.base.type import ConfigType
from lib.language.base import BaseLanguageSetting
from lib.section.base import BaseSectionGenerator


class SummaryGenerator(BaseSectionGenerator):
    def __init__(self, data: pd.DataFrame, setting: BaseLanguageSetting) -> None:
        self.data = data
        self.setting = setting

    @staticmethod
    def __format_date(date: datetime) -> str:
        return date.strftime("%Y-%m-%d")

    def today_configure(self) -> ConfigType:
        today = self.data.iloc[-1]

        return {
            "date": self.__format_date(
                today["date"]
            ),
            "count": today["count"],
        }

    def max_configure(self) -> ConfigType:
        maximum = self.data.iloc[
            self.data["count"].idxmax()
        ]

        return {
            "date": self.__format_date(
                maximum["date"]
            ),
            "count": maximum["count"],
        }

    def total_configure(self) -> ConfigType:
        counts = self.data["count"]

        return {
            "length": len(counts.index),
            "sum": counts.sum(),
            "average": counts.mean(),
        }

    def continuous_configure(self) -> ConfigType:
        exist = pd.Series(data=(self.data["count"] > 0))
        continuous = exist * (exist.groupby(
            (exist != exist.shift()).cumsum()
        ).cumcount() + 1)

        cur_len = continuous.iloc[-1]
        max_idx = continuous.idxmax()
        max_len = continuous.iloc[max_idx]

        return {
            "current": {
                "length": cur_len,
                "start": self.__format_date(
                    self.data.iloc[-1 - max(0, cur_len-1)]["date"]
                ),
                # current end = today date
            },
            "max": {
                "length": max_len,
                "start": self.__format_date(
                    self.data.iloc[max_idx - max(0, max_len-1)]["date"]
                ),
                "end": self.__format_date(
                    self.data.iloc[max_idx]["date"]
                ),
            },
        }

    def generate(self) -> str:
        return self.setting.format_summary(
            today=self.today_configure(),
            maximum=self.max_configure(),
            total=self.total_configure(),
            continuous=self.continuous_configure(),
        )
