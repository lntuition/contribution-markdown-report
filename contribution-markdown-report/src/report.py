import os
import warnings
from typing import Optional, Sequence, Type, Union

import numpy as np
import pandas as pd
import seaborn as sns
from tabulate import tabulate

from .contribution import ContributionInfo
from .language import BaseLanguageSetting


class Report:
    def __init__(
        self, info: ContributionInfo, setting: Type[BaseLanguageSetting], headings: Sequence[str], file_name: str
    ) -> None:
        self._info = info
        self._setting = setting
        self._headings = headings
        self._file_name = file_name

    @staticmethod
    def __format_value(val: Union[pd.Timestamp, int, float, str]) -> str:
        if isinstance(val, pd.Timestamp):
            val = val.strftime("%Y-%m-%d")
        elif isinstance(val, float):
            val = round(val, 2)
        elif isinstance(val, str) and val.endswith(".png"):
            return f"![]({val})"

        return f"**{val}**"

    def attribute(self, key: str) -> str:
        key = key.lower()
        if key == "brief":
            return self._info.brief

        raise Exception(f"{key} isn't supported attribute")

    def header_heading(self) -> str:
        repo_url = "https://github.com/lntuition/contribution-markdown-report"
        issue_url = f"{repo_url}/issues"

        title = self._setting.header_title(user=self._info.user)
        repository = self._setting.repository(url=repo_url)
        issue = self._setting.issue(url=issue_url)
        ending = self._setting.ending()

        return f"# {title}\n{repository} {issue} {ending} :airplane:\n"

    def summary_heading(self) -> str:
        sequences = [
            ("today", ":+1:"),
            ("maximum", ":muscle:"),
            ("total", ":clap:"),
            ("today_peak", ":walking:"),
            ("maximum_peak", ":running:"),
        ]

        text = f"## {self._setting.summary_title()}\n"
        for attr, emoji in sequences:
            kwargs = getattr(self._info, attr)()
            for key, val in kwargs.items():
                kwargs[key] = self.__format_value(val)

            summary = getattr(self._setting, attr)(**kwargs)
            text += f"- {summary} {emoji}\n"

        return text

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

    def graph_heading(self) -> str:
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
            series = getattr(self._info, attr)()
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

    def generate(self) -> None:
        text = ""
        for heading in self._headings:
            try:
                func = getattr(self, f"{heading}_heading")
            except AttributeError:
                warnings.warn(f"{heading} isn't supported heading, ignore")

            text += func()

        with open(self._file_name, "w") as markdown:
            markdown.write(text)
