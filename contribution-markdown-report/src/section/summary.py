import warnings
from typing import Any, Dict

import pandas as pd

from section.base import Section


class SummarySetting:
    @staticmethod
    def title() -> str:
        return "Summary"

    @staticmethod
    def today(date: str, count: str, length: str) -> str:
        return f"{date} was {length}th day since the start of trip, and there was {count} new contribution."

    @staticmethod
    def maximum(date: str, count: str) -> str:
        return f"Daily maximum contribution day is {date}, which is {count}."

    @staticmethod
    def total(_sum: str, avg: str) -> str:
        return f"During the trip, total contribuition count is {_sum} and average contribution count is {avg}."

    @staticmethod
    def peak(length: str, start: str, end: str) -> str:
        return f"Longest continuous contribution trip was {length} days from {start} to {end}."

    @staticmethod
    def cur_peak(length: str, start: str) -> str:
        return f"Current continuous contribution trip is {length} days from {start}."


class SummarySettingFactory:
    @staticmethod
    def create_setting(language: str) -> SummarySetting:
        if language == "english":  # Default
            pass
        else:
            warnings.warn("Not supported languge, use default setting")

        return SummarySetting()


class SummarySection(Section):
    def __init__(self, data: pd.DataFrame, setting: SummarySetting) -> None:
        self.__data = data
        self.__setting = setting

    def __params(self) -> Dict[str, Dict[str, Any]]:
        counts = self.__data["count"]

        today = self.__data.iloc[-1]
        maximum_idx = counts.idxmax()
        maximum = self.__data.iloc[maximum_idx]

        exist = pd.Series(data=(self.__data["count"] > 0))
        continuous = exist * (exist.groupby((exist != exist.shift()).cumsum()).cumcount() + 1)

        peak_end_idx = continuous.idxmax()
        peak_length = continuous.iloc[peak_end_idx]
        peak_start_idx = peak_end_idx - max(0, peak_length - 1)

        cur_peak_length = continuous.iloc[-1]
        cur_start_idx = -1 - max(0, cur_peak_length - 1)

        return {
            "today": {
                "date": today["date"],
                "count": today["count"],
                "length": len(self.__data.index),
            },
            "total": {
                "_sum": counts.sum(),
                "avg": counts.mean(),
            },
            "maximum": {
                "date": maximum["date"],
                "count": maximum["count"],
            },
            "peak": {
                "length": peak_length,
                "start": self.__data.iloc[peak_start_idx]["date"],
                "end": self.__data.iloc[peak_end_idx]["date"],
            },
            "cur_peak": {
                "length": cur_peak_length,
                "start": self.__data.iloc[cur_start_idx]["date"],
            },
        }

    @staticmethod
    def __format_params(params: Dict[str, Any]) -> Dict[str, str]:
        for key, val in params.items():
            if isinstance(val, pd.Timestamp):
                val = val.strftime("%Y-%m-%d")
            elif isinstance(val, float):
                val = round(val, 2)

            params[key] = f"**{val}**"

        return params

    def write(self) -> str:
        sequences = [
            ("today", ":+1:"),
            ("maximum", ":muscle:"),
            ("total", ":clap:"),
            ("peak", ":walking:"),
            ("cur_peak", ":running:"),
        ]
        params = self.__params()

        text = f"## {self.__setting.title()}\n"
        for key, emoji in sequences:
            formatted = self.__format_params(params[key])
            summary = getattr(self.__setting, key)(**formatted)
            text += f"- {summary} {emoji}\n"

        return text
