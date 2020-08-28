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
    def format_date(date: datetime) -> str:
        return date.strftime("%Y-%m-%d")

    def day_based_configure(self) -> ConfigType:
        today = self.data.iloc[-1]

        return {
            "today": {
                "date": self.format_date(
                    today["date"]
                ),
                "count": today["count"],
            }
        }

    def count_based_configure(self) -> ConfigType:
        counts = self.data["count"]
        maximum = self.data.iloc[counts.idxmax()]

        return {
            "total": {
                "length": len(counts.index),
                "sum": counts.sum(),
                "average": counts.mean(),
            },
            "max": {
                "date": self.format_date(
                    maximum["date"]
                ),
                "count": maximum["count"],
            },
        }

    def continuous_based_configure(self) -> ConfigType:
        exist = pd.Series(data=(self.data["count"] > 0))
        continuous = exist * (exist.groupby(
            (exist != exist.shift()).cumsum()
        ).cumcount() + 1)

        cur_len = continuous.iloc[-1]
        max_idx = continuous.idxmax()
        max_len = continuous.iloc[max_idx]

        return {
            "continuous": {
                "current": {
                    "length": cur_len,
                    "start": self.format_date(
                        self.data.iloc[-1 - max(0, cur_len-1)]["date"]
                    ),
                },
                "max": {
                    "length": max_len,
                    "start": self.format_date(
                        self.data.iloc[max_idx - max(0, max_len-1)]["date"]
                    ),
                    "end": self.format_date(
                        self.data.iloc[max_idx]["date"]
                    ),
                },
            },
        }

    def configure(self) -> ConfigType:
        return {
            **self.day_based_configure(),
            **self.count_based_configure(),
            **self.continuous_based_configure(),
        }

    def process(self, config: ConfigType) -> str:
        return self.setting.format_summary(config=config)
