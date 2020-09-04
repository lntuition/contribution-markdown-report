import pandas as pd

from datetime import datetime
from textwrap import dedent
from typing import Any, Callable, Dict, TypeVar, Union

from lib.language.base import LanguageSetting
from lib.section.base import SectionGenerator


T = TypeVar("T")
Config = Dict[str, Any]


class SummaryGenerator(SectionGenerator):
    def __init__(self, data: pd.DataFrame, setting: LanguageSetting) -> None:
        super().__init__(setting=setting)
        self.data = data

    def __formatize_for_markdown(self, arg: Any) -> str:
        if isinstance(arg, datetime):
            arg = arg.strftime("%Y-%m-%d")
        elif isinstance(arg, float):
            arg = round(arg, 2)

        return self._bold_markdown(arg)

    def __generate_with_setting(
        self,
        setting: Callable[..., T],
        config: Union[Callable[..., Config], Config]
    ) -> T:
        if callable(config):
            config = config()

        return setting(
            **{k: self.__formatize_for_markdown(v) for k, v in config.items()}
        )

    def today_configure(self) -> Config:
        today = self.data.iloc[-1]

        return {
            "today": today["date"],
            "length": len(self.data.index),
            "count": today["count"],
        }

    def maximum_configure(self) -> Config:
        maximum = self.data.iloc[
            self.data["count"].idxmax()
        ]

        return {
            "date": maximum["date"],
            "count": maximum["count"],
        }

    def total_configure(self) -> Config:
        counts = self.data["count"]

        return {
            "sum": counts.sum(),
            "avg": counts.mean(),
        }

    def peak_configure(self) -> Config:
        exist = pd.Series(data=(self.data["count"] > 0))
        continuous = exist * (exist.groupby(
            (exist != exist.shift()).cumsum()
        ).cumcount() + 1)

        cur_len = continuous.iloc[-1]
        max_idx = continuous.idxmax()
        max_len = continuous.iloc[max_idx]

        return {
            "peak": {
                "length": max_len,
                "start": self.data.iloc[max_idx - max(0, max_len-1)]["date"],
                "end": self.data.iloc[max_idx]["date"],
            },
            "cur_peak": {
                "length": cur_len,
                "start": self.data.iloc[-1 - max(0, cur_len-1)]["date"]
            },
        }

    def generate(self) -> str:
        title = self.setting.summary_title()

        today = self.__generate_with_setting(
            setting=self.setting.summary_today,
            config=self.today_configure,
        )
        maximum = self.__generate_with_setting(
            setting=self.setting.summary_maximum,
            config=self.maximum_configure,
        )
        total = self.__generate_with_setting(
            setting=self.setting.summary_total,
            config=self.total_configure,
        )

        peak_config = self.peak_configure()
        peak = self.__generate_with_setting(
            setting=self.setting.summary_peak,
            config=peak_config["peak"],
        )
        cur_peak = self.__generate_with_setting(
            setting=self.setting.summary_cur_peak,
            config=peak_config["cur_peak"],
        )

        return dedent(f"""
            ## {title}
            - {today} :+1:
            - {maximum} :muscle:
            - {total} :clap:
            - {peak} :walking:
            - {cur_peak} :running:
        """)
