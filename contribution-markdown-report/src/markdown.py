import os
from abc import ABC, abstractmethod
from typing import Optional, Sequence, Union

import numpy as np
import pandas as pd
import seaborn as sns
from tabulate import tabulate

from .contribution import ContributionInfo
from .language import LanguageSetting


class MarkdownSection(ABC):
    def __init__(self, setting: LanguageSetting) -> None:
        self._setting = setting

    @property
    def setting(self) -> LanguageSetting:
        # Expose for testing, not using this directly
        return self._setting

    @abstractmethod
    def write(self, info: ContributionInfo) -> str:
        pass


class MarkdownHeaderSection(MarkdownSection):
    def write(self, info: ContributionInfo) -> str:
        repo_url = "https://github.com/lntuition/contribution-markdown-report"
        issue_url = f"{repo_url}/issues"

        title = self._setting.header_title(user=info.user)
        repository = self._setting.repository(url=repo_url)
        issue = self._setting.issue(url=issue_url)
        ending = self._setting.ending()

        return f"# {title}\n{repository} {issue} {ending} :airplane:\n"


class MarkdownSummarySection(MarkdownSection):
    @staticmethod
    def __format_value(val: Union[pd.Timestamp, int, float, str]) -> str:
        if isinstance(val, pd.Timestamp):
            val = val.strftime("%Y-%m-%d")
        elif isinstance(val, float):
            val = round(val, 2)

        return f"**{val}**"

    def write(self, info: ContributionInfo) -> str:
        sequences = [
            ("today", ":+1:"),
            ("maximum", ":muscle:"),
            ("total", ":clap:"),
            ("today_peak", ":walking:"),
            ("maximum_peak", ":running:"),
        ]

        text = f"## {self._setting.summary_title()}\n"
        for attr, emoji in sequences:
            kwargs = getattr(info, attr)()
            for key, val in kwargs.items():
                kwargs[key] = self.__format_value(val)

            summary = getattr(self._setting, attr)(**kwargs)
            text += f"- {summary} {emoji}\n"

        return text


class MarkdownGraphSection(MarkdownSection):
    @staticmethod
    def __format_value(val: str) -> str:
        if val.endswith(".png"):
            return f"![]({val})"

        return f"**{val}**"

    @staticmethod
    def __draw_barplot(
        series: pd.Series,
        label: Optional[Sequence[str]],
        xlabel: str,
        ylabel: str,
        file_name: str,
    ) -> None:
        if label:
            series = series.rename(index=lambda x: label[x])

        sns.set_style("whitegrid")
        axes = sns.barplot(x=series.index, y=series, palette="pastel")
        axes.set(xlabel=xlabel, ylabel=ylabel)
        sns.despine(ax=axes)

        for patch in axes.patches:
            height = round(patch.get_height(), 2)

            if height != 0:
                axes.annotate(
                    text=f"{height}",
                    xy=(patch.get_x() + patch.get_width() / 2, height * 1.02),
                    ha="center",
                    va="bottom",
                )

        fig = axes.get_figure()
        fig.savefig(file_name, dpi=200, bbox_inches="tight")
        fig.clf()

    def write(self, info: ContributionInfo) -> str:
        bar_sequences = [
            (
                "count_sum_recent",
                self._setting.contribution_axis(),
                self._setting.day_axis(),
                None,
            ),
            (
                "dayofweek_sum_recent",
                self._setting.dayofweek_axis(),
                self._setting.contribution_axis(),
                self._setting.dayofweek_label(),
            ),
            (
                "month_sum_recent",
                self._setting.month_axis(),
                self._setting.contribution_axis(),
                self._setting.month_label(),
            ),
            (
                "count_sum_full",
                self._setting.contribution_axis(),
                self._setting.day_axis(),
                None,
            ),
            (
                "dayofweek_mean_full",
                self._setting.dayofweek_axis(),
                self._setting.contribution_axis(),
                self._setting.dayofweek_label(),
            ),
            (
                "year_sum_full",
                self._setting.year_axis(),
                self._setting.contribution_axis(),
                None,
            ),
        ]

        asset_dir = "asset"
        cur_dir = os.getcwd()
        os.makedirs(asset_dir, exist_ok=True)
        os.chdir(asset_dir)

        table = np.array([])
        for attr, xlabel, ylabel, label in bar_sequences:
            series = getattr(info, attr)()
            file_name = f"{attr}.png"

            self.__draw_barplot(series, label, xlabel, ylabel, file_name)

            elems = [
                getattr(self._setting, f"{attr}_title")(),
                os.path.join(asset_dir, file_name),
            ]
            for i, elem in enumerate(elems):
                elems[i] = self.__format_value(elem)

            table = np.append(table, elems)

        os.chdir(cur_dir)

        return f"## {self._setting.graph_title()}\n" + tabulate(
            np.reshape(table, (-1, 2), order="F"),
            headers="firstrow",
            tablefmt="pipe",
            colalign=["center", "center"],
        )


class MarkdownSectionBuilder:
    def __init__(self, setting: LanguageSetting) -> None:
        self.__setting = setting

    def build_header(self) -> MarkdownHeaderSection:
        return MarkdownHeaderSection(setting=self.__setting)

    def build_summary(self) -> MarkdownSummarySection:
        return MarkdownSummarySection(setting=self.__setting)

    def build_graph(self) -> MarkdownGraphSection:
        return MarkdownGraphSection(setting=self.__setting)
