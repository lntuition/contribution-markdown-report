import warnings
from typing import Any, Dict, List, Optional, Sequence, Tuple

import pandas as pd
import seaborn as sns

from section.base import Section
from util import safe_chdir


class GraphSetting:
    @staticmethod
    def title() -> str:
        return "Graph"

    @staticmethod
    def dayofweek_label() -> Sequence[str]:
        return ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    @staticmethod
    def month_label() -> Sequence[str]:
        return ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    @staticmethod
    def contribution_axis() -> str:
        return "contribution count"

    @staticmethod
    def day_axis() -> str:
        return "day"

    @staticmethod
    def dayofweek_axis() -> str:
        return "day of week"

    @staticmethod
    def month_axis() -> str:
        return "month"

    @staticmethod
    def count_sum_recent_title() -> str:
        return "Number of days per contribution up to the last 4 weeks"

    @staticmethod
    def count_sum_full_title() -> str:
        return "Number of days per contribution"

    @staticmethod
    def dayofweek_sum_recent_title() -> str:
        return "Number of contribution per day of week up to the last 12 weeks"

    @staticmethod
    def dayofweek_mean_full_title() -> str:
        return "Average of contribution per day of week"

    @staticmethod
    def month_sum_recent_title() -> str:
        return "Number of contribution per month up to the last year"

    @staticmethod
    def month_mean_full_title() -> str:
        return "Average of contribution per month"


class GraphSettingFactory:
    @staticmethod
    def create_setting(language: str) -> GraphSetting:
        if language == "english":  # Default
            pass
        else:
            warnings.warn("Not supported languge, use default setting")

        return GraphSetting()


class GraphSection(Section):
    def __init__(self, data: pd.DataFrame, setting: GraphSetting) -> None:
        self.__data = data
        self.__setting = setting

    # Public for testing
    def bar_series(self) -> Dict[str, pd.Series]:
        length = len(self.__data.index)
        dates = self.__data["date"].dt

        cnt_slice = max(-28, -length)
        cnt_bins = [-1, 0, 2, 4, 6, 1_000_000]  # Over millions not concerned
        cnt_labels = ["0", "1-2", "3-4", "5-6", "7+"]

        count_sum_recent = pd.cut(self.__data[cnt_slice:]["count"], bins=cnt_bins, labels=cnt_labels).value_counts()
        count_sum_full = pd.cut(self.__data["count"], bins=cnt_bins, labels=cnt_labels).value_counts()

        dayofweek_slice = max(-112, -length)
        dayofweek_groupby = dates.dayofweek

        dayofweek_sum_recent = self.__data[dayofweek_slice:].groupby(dayofweek_groupby)["count"].sum()
        dayofweek_mean_full = self.__data.groupby(dayofweek_groupby)["count"].mean()

        month_slice = max(-365, -length)
        month_groupby = dates.month
        month_counts = self.__data.groupby(month_groupby)["count"]

        month_sum_recent = self.__data[month_slice:].groupby(month_groupby)["count"].sum().rename(lambda x: x - 1)
        month_mean_full = (
            month_counts.mean()
            .rename(lambda x: x - 1)
            .multiply(
                pd.Series([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]).combine(
                    month_counts.count().rename(lambda x: x - 1), min, fill_value=0
                )
            )
        )

        return {
            "count_sum_recent": count_sum_recent,
            "count_sum_full": count_sum_full,
            "dayofweek_sum_recent": dayofweek_sum_recent,
            "dayofweek_mean_full": dayofweek_mean_full,
            "month_sum_recent": month_sum_recent,
            "month_mean_full": month_mean_full,
        }

    @staticmethod
    def __draw_barplot(
        series: pd.Series, xlabel: str, ylabel: str, filename: str, label: Optional[Sequence[str]] = None
    ) -> None:
        if label:
            series = series.rename(index=lambda x: label[x])

        sns.set_style("whitegrid")
        axes = sns.barplot(x=series.index, y=series, palette="pastel")
        axes.set(xlabel=xlabel, ylabel=ylabel)
        sns.despine(ax=axes, top=True, right=True)

        for patch in axes.patches:
            height = patch.get_height()

            if height.is_integer():
                height = int(height)

                if height == 0:
                    continue
            else:
                height = round(height, 2)

            axes.annotate(
                text=f"{height}", xy=(patch.get_x() + patch.get_width() / 2, height * 1.02), ha="center", va="bottom"
            )

        fig = axes.get_figure()
        fig.savefig(filename, dpi=200, bbox_inches="tight")
        fig.clf()

    def write(self) -> str:
        bar_sequences: List[Tuple[str, Dict[str, Any]]] = [
            (
                "count_sum_recent",
                {
                    "xlabel": self.__setting.contribution_axis(),
                    "ylabel": self.__setting.day_axis(),
                },
            ),
            (
                "count_sum_full",
                {
                    "xlabel": self.__setting.contribution_axis(),
                    "ylabel": self.__setting.day_axis(),
                },
            ),
            (
                "dayofweek_sum_recent",
                {
                    "label": self.__setting.dayofweek_label(),
                    "xlabel": self.__setting.dayofweek_axis(),
                    "ylabel": self.__setting.contribution_axis(),
                },
            ),
            (
                "dayofweek_mean_full",
                {
                    "label": self.__setting.dayofweek_label(),
                    "xlabel": self.__setting.dayofweek_axis(),
                    "ylabel": self.__setting.contribution_axis(),
                },
            ),
            (
                "month_sum_recent",
                {
                    "label": self.__setting.month_label(),
                    "xlabel": self.__setting.month_axis(),
                    "ylabel": self.__setting.contribution_axis(),
                },
            ),
            (
                "month_mean_full",
                {
                    "label": self.__setting.month_label(),
                    "xlabel": self.__setting.month_axis(),
                    "ylabel": self.__setting.contribution_axis(),
                },
            ),
        ]
        bar_series = self.bar_series()

        cells = []
        asset = "asset"
        with safe_chdir(asset):
            for key, params in bar_sequences:
                params["series"] = bar_series[key]
                params["filename"] = f"{key}.png"

                self.__draw_barplot(**params)

                bar_title = f"**{getattr(self.__setting, f'{key}_title')()}**"
                bar_image = f"![]({asset}/{params['filename']})"

                cells.append(bar_title)
                cells.append(bar_image)

        cells_length = len(cells)
        for i in range(0, cells_length, 4):
            cells[i + 1], cells[i + 2] = cells[i + 2], cells[i + 1]

        text = f"## {self.__setting.title()}\n| {cells[0]} | {cells[1]} |\n|:--:|:--:|\n"
        for i in range(2, cells_length, 2):
            text += f"| {cells[i]} | {cells[i + 1]} |\n"

        return text
