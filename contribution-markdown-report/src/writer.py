from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

import pandas as pd
import seaborn as sns

from attribute import Graph, Header, Summary
from setting import Setting
from util import safe_chdir


class Writer(ABC):
    @abstractmethod
    def write(self, setting: Setting) -> str:
        pass


class HeaderWriter(Header, Writer):
    def __init__(self, user: str) -> None:
        self.__user = user

    def write(self, setting: Setting) -> str:
        repo_url = "https://github.com/lntuition/contribution-markdown-report"
        issue_url = f"{repo_url}/issues"

        title = setting.title(user=self.__user)
        repository = setting.repository(url=repo_url)
        issue = setting.issue(url=issue_url)
        ending = setting.ending()

        return f"# {title}\n{repository} {issue} {ending} :airplane:\n"


class SummaryWriter(Summary, Writer):
    def __init__(self, data: pd.DataFrame) -> None:
        self.__data = data

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
                "start": self.__data[cur_start_idx]["date"],
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

    def write(self, setting: Setting) -> str:
        sequences = [
            ("today", ":+1:"),
            ("maximum", ":muscle:"),
            ("total", ":clap:"),
            ("peak", ":walking:"),
            ("cur_peak", ":running:"),
        ]
        params = self.__params()

        text = f"## {setting.title()}\n"
        for key, emoji in sequences:
            formatted = self.__format_params(params[key])
            summary = getattr(setting, key)(**formatted)
            text += f"- {summary} {emoji}\n"

        return text


class GraphWriter(Graph, Writer):
    def __init__(self, data: pd.DataFrame) -> None:
        self.__data = data

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
        series: pd.Series, xlabel: str, ylabel: str, filename: str, label: Optional[List[str]] = None
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

    def write(self, setting: Setting) -> str:
        bar_sequences = [
            (
                "count_sum_recent",
                {
                    "xlabel": setting.contribution_axis(),
                    "ylabel": setting.day_axis(),
                },
            ),
            (
                "count_sum_full",
                {
                    "xlabel": setting.contribution_axis(),
                    "ylabel": setting.day_axis(),
                },
            ),
            (
                "dayofweek_sum_recent",
                {
                    "label": setting.dayofweek_label(),
                    "xlabel": setting.dayofweek_axis(),
                    "ylabel": setting.contribution_axis(),
                },
            ),
            (
                "dayofweek_mean_full",
                {
                    "label": setting.dayofweek_label(),
                    "xlabel": setting.dayofweek_axis(),
                    "ylabel": setting.contribution_axis(),
                },
            ),
            (
                "month_sum_recent",
                {
                    "label": setting.month_label(),
                    "xlabel": setting.month_axis(),
                    "ylabel": setting.contribution_axis(),
                },
            ),
            (
                "month_mean_full",
                {
                    "label": setting.month_label(),
                    "xlabel": setting.month_axis(),
                    "ylabel": setting.contribution_axis(),
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

                bar_title = getattr(setting, f"{key}_title")()
                bar_image = f"![]({asset}/{params['filename']})"

                cells.append(bar_title)
                cells.append(bar_image)

        cells_length = len(cells)
        for i in range(0, cells_length, 4):
            cells[i + 1], cells[i + 2] = cells[i + 2], cells[i + 1]

        text = f"## {setting.title()}\n| {cells[0]} | {cells[1]} |\n|:--:|:--:|\n"
        for i in range(2, cells_length, 2):
            text += f"| {cells[i]} | {cells[i + 1]} |\n"

        return text
