import math
import numpy as np
import pandas as pd
import seaborn as sns

from matplotlib.axes import Axes
from typing import Any, List, Optional, Tuple

from lib.language.base import LanguageSetting
from lib.section.base import SectionGenerator
from lib.util.directory import change_workdir


class GraphGenerator(SectionGenerator):
    def __init__(self, data: pd.DataFrame, setting: LanguageSetting, workdir: str = "asset") -> None:
        super().__init__(setting=setting)
        self.data = data
        self.workdir = workdir

    @staticmethod
    def __label_series(series: pd.Series, label: List[str]) -> pd.Series:
        return series.rename(index=lambda x: label[x])

    @staticmethod
    def __draw_barplot(series: pd.Series) -> Axes:
        sns.set_style("whitegrid")
        ax = sns.barplot(x=series.index, y=series, palette="pastel")
        sns.despine(ax=ax, top=True, right=True)

        return ax

    @staticmethod
    def __label_axis(ax: Axes, xlabel: str, ylabel: str) -> None:
        ax.set(xlabel=xlabel, ylabel=ylabel)

    @staticmethod
    def __annotate_axis(ax: Axes) -> None:
        for p in ax.patches:
            height = p.get_height()
            if math.isclose(height, 0.0):
                continue

            ax.annotate(
                f"{height:.0f}" if height.is_integer() else f"{height:.2f}",
                (p.get_x() + p.get_width() / 2, height * 1.02),
                ha="center"
            )

    def __save_barplot(self, ax: Axes, filename: str) -> None:
        with change_workdir(self.workdir):
            fig = ax.get_figure()
            fig.savefig(filename, dpi=200, bbox_inches="tight")
            fig.clf()

    def __generate_with_setting(
        self,
        series: pd.Series,
        xlabel: str,
        ylabel: str,
        title: str,
        filename: str,
        label: Optional[List[str]] = None,
    ) -> Tuple[str, str]:
        if label:
            self.__label_series(series=series, label=label)
        ax = self.__draw_barplot(series=series)

        self.__label_axis(ax=ax, xlabel=xlabel, ylabel=ylabel)
        self.__annotate_axis(ax=ax)
        self.__save_barplot(ax=ax, filename=filename)

        return (
            self._bold_markdown(title),
            self._image_markdown(f"{self.workdir}/{filename}")
        )

    @staticmethod
    def __formatize_table(info: List[Tuple[str, str]]) -> str:
        table = []
        for idx in range(0, len(info), 2):
            front_title, front_image = info[idx]
            back_title, back_image = info[idx+1]

            table.append(f"| {front_title} | {back_title} |")
            table.append(f"| {front_image} | {back_image} |")

        table.insert(1, "|:--:|:--:|")

        return "\n".join(table)

    def count_sum_recent_series(self) -> pd.Series:
        return pd.cut(
            self.data[max(-28, -len(self.data.index)):]["count"],
            bins=[-1, 0, 2, 4, 6, np.inf],
            labels=["0", "1-2", "3-4", "5-6", "7+"]
        ).value_counts()

    def count_sum_full_series(self) -> pd.Series:
        return pd.cut(
            self.data["count"],
            bins=[-1, 0, 2, 4, 6, np.inf],
            labels=["0", "1-2", "3-4", "5-6", "7+"]
        ).value_counts()

    def dayofweek_sum_recent_series(self) -> pd.Series:
        return self.data[
            max(-112, -len(self.data.index)):
        ].groupby(
            self.data["date"].dt.dayofweek
        )["count"].sum()

    def dayofweek_mean_full_series(self) -> pd.Series:
        return self.data.groupby(
            self.data["date"].dt.dayofweek
        )["count"].mean()

    def month_sum_recent_series(self) -> pd.Series:
        return self.data[
            max(-365, -len(self.data.index)):
        ].groupby(
            self.data["date"].dt.month
        )["count"].sum().rename(lambda x: x - 1)

    def month_mean_full_series(self) -> pd.Series:
        month_groupby = self.data.groupby(
            self.data["date"].dt.month
        )["count"]

        return month_groupby.mean().rename(lambda x: x - 1).multiply(
            pd.Series(
                [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            ).combine(
                month_groupby.count().rename(lambda x: x - 1), min, fill_value=0
            )
        )

    def generate(self) -> str:
        title = self.setting.graph_title()

        params = [
            {
                "series": self.count_sum_recent_series(),
                "xlabel": self.setting.graph_contribution_axis(),
                "ylabel": self.setting.graph_day_axis(),
                "title": self.setting.graph_count_sum_recent_title(),
                "filename": "count_sum_recent.png",
            },
            {
                "series": self.count_sum_full_series(),
                "xlabel": self.setting.graph_contribution_axis(),
                "ylabel": self.setting.graph_day_axis(),
                "title": self.setting.graph_count_sum_full_title(),
                "filename": "count_sum_full.png",
            },
            {
                "series": self.dayofweek_sum_recent_series(),
                "label": self.setting.graph_dayofweek_label(),
                "xlabel": self.setting.graph_dayofweek_axis(),
                "ylabel": self.setting.graph_contribution_axis(),
                "title": self.setting.graph_dayofweek_sum_recent_title(),
                "filename": "dayofweek_sum_recent.png",
            },
            {
                "series": self.dayofweek_mean_full_series(),
                "label": self.setting.graph_dayofweek_label(),
                "xlabel": self.setting.graph_dayofweek_axis(),
                "ylabel": self.setting.graph_contribution_axis(),
                "title": self.setting.graph_dayofweek_mean_full_title(),
                "filename": "dayofweek_mean_full.png",
            },
            {
                "series": self.month_sum_recent_series(),
                "label": self.setting.graph_month_label(),
                "xlabel": self.setting.graph_month_axis(),
                "ylabel": self.setting.graph_contribution_axis(),
                "title": self.setting.graph_month_sum_recent_title(),
                "filename": "month_sum_recent.png",
            },
            {
                "series": self.month_mean_full_series(),
                "label": self.setting.graph_month_label(),
                "xlabel": self.setting.graph_month_axis(),
                "ylabel": self.setting.graph_contribution_axis(),
                "title": self.setting.graph_month_mean_full_title(),
                "filename": "month_mean_full.png",
            },
        ]
        table = self.__formatize_table(
            info=list(map(lambda x: self.__generate_with_setting(**x), params))
        )

        return f"## {title}\n{table}"
