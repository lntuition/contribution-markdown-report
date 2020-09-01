import math
import numpy as np
import pandas as pd
import seaborn as sns

from textwrap import dedent
from typing import Iterable, Optional

from lib.base.type import ConfigType
from lib.language.base import LanguageSetting
from lib.section.base import SectionGenerator
from lib.util.directory import change_workdir


class GraphGenerator(SectionGenerator):
    def __init__(self, data: pd.DataFrame, setting: LanguageSetting, workdir: str = "asset") -> None:
        super().__init__(setting=setting)
        self.data = data
        self.workdir = workdir

    def save_barplot(self, series: pd.Series, config: ConfigType, percent: bool, filename: str) -> None:
        sns.set_style("whitegrid")

        label = config.get("label", None)
        if label:
            series.rename(index=lambda x: label[x])

        ax = sns.barplot(x=series.index, y=series, palette="pastel")
        ax.set(xlabel=config["x"], ylabel=config["y"])
        sns.despine(ax=ax, top=True, right=True)

        if percent:
            total = series.sum()

        for p in ax.patches:
            height = p.get_height()
            if math.isclose(height, 0.0):
                continue

            annotation = f"{height:.2f}"
            if height.is_integer():
                annotation = f"{height:.0f}"

            if percent:
                annotation += f"({100 * height / total:.1f}%)"

            ax.annotate(
                annotation,
                (p.get_x() + p.get_width() / 2, height * 1.02),
                ha="center"
            )

        fig = ax.get_figure()
        fig.savefig(filename, dpi=200, bbox_inches="tight")
        fig.clf()

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
        )["count"].sum()

    def month_sum_recent_series(self) -> pd.Series:
        return self.data[
            max(-365, -len(self.data.index)):
        ].groupby(
            self.data["date"].dt.month
        )["count"].sum()

    def month_mean_full_series(self) -> pd.Series:
        month_groupby = self.data.groupby(
            self.data["date"].dt.month
        )["count"]

        return month_groupby.mean().multiply(
            pd.Series(
                [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            ).combine(
                month_groupby.count(), min, fill_value=0
            )
        )

    def generate(self) -> str:
        config = self.setting.config_graph()

        assets = []
        with change_workdir(self.workdir):
            for info, title in config["title"].items():
                plot, based, reducer, bounds = info.split(":")
                filename = f"{based}_{reducer}_{bounds}.png"

                self.save_barplot(
                    series=getattr(
                        self,
                        f"{based}_{reducer}_{bounds}_series"
                    )(),
                    config=config[plot][based],
                    percent=(reducer == "sum"),
                    filename=filename,
                )

                assets.append({
                    "title": title,
                    "src": f"{self.workdir}/{filename}",
                })

        return dedent(f"""
            ## {config["section"]["title"]}
            | **{assets[0]["title"]}** | **{assets[1]["title"]}** |
            |:------------------------:|:------------------------:|
            | ![]({assets[0]["src"]})  | ![]({assets[1]["src"]})  |
            | **{assets[2]["title"]}** | **{assets[3]["title"]}** |
            | ![]({assets[2]["src"]})  | ![]({assets[3]["src"]})  |
            | **{assets[4]["title"]}** | **{assets[5]["title"]}** |
            | ![]({assets[4]["src"]})  | ![]({assets[5]["src"]})  |
        """)
