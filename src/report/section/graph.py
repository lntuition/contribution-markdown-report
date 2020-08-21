import numpy as np
import os
import pandas as pd
import seaborn as sns

from matplotlib.axes import Axes
from textwrap import dedent
from typing import Tuple

from base.type import ConfigType


class GraphGenerator():
    def _config_graph(self) -> ConfigType:
        raise NotImplementedError()

    def _generate_barplot_axes(
        self,
        series: pd.Series,
        config: ConfigType,
        percent: bool,
        workdir: str,
        filename: str
    ) -> str:
        sns.set_style("whitegrid")

        ax = sns.barplot(x=series.index, y=series, palette="pastel")
        ax.set(xlabel=config["x"], ylabel=config["y"])

        if percent:
            total = series.sum()

        _, max_height = ax.get_ylim()
        for p in ax.patches:
            height = p.get_height()
            annotation = f"{height:.2f}"
            if height.is_integer():
                annotation = f"{height:.0f}"
            if percent:
                annotation += f"({100 * height / total:.1f}%)"

            ax.annotate(
                annotation,
                (
                    p.get_x() + p.get_width() / 2,
                    height + (0.03 if max_height < 5 else 0.3)
                ),
                ha="center"
            )

        sns.despine(ax=ax, top=True, right=True)

        fig = ax.get_figure()
        fig.savefig(filename, dpi=200, bbox_inches="tight")
        fig.clf()

        return f"{workdir}/{filename}"

    def generate_graph(self, data: pd.DataFrame, workdir: str) -> str:
        os.makedirs(workdir, exist_ok=True)
        os.chdir(workdir)

        config = self._config_graph()
        total_dates = len(data.index)

        count_sum_recent = pd.cut(
            data[max(-28, -total_dates):]["count"],
            bins=[-1, 0, 2, 4, 6, np.inf],
            labels=["0", "1-2", "3-4", "5-6", "7+"]
        ).value_counts()

        count_sum_recent_src = self._generate_barplot_axes(
            series=count_sum_recent,
            config=config["count"],
            percent=True,
            workdir=workdir,
            filename="count_sum_recent.png"
        )

        count_sum_full = pd.cut(
            data["count"],
            bins=[-1, 0, 2, 4, 6, np.inf],
            labels=["0", "1-2", "3-4", "5-6", "7+"]
        ).value_counts()

        count_sum_full_src = self._generate_barplot_axes(
            series=count_sum_full,
            config=config["count"],
            percent=True,
            workdir=workdir,
            filename="count_sum_full.png"
        )

        dayofweek_sum_recent = data[
            max(-112, -total_dates):
        ].groupby(
            data["date"].dt.dayofweek
        )["count"].sum().rename(
            index=lambda x: config["dayofweek"]["label"][x]
        )

        dayofweek_sum_recent_src = self._generate_barplot_axes(
            series=dayofweek_sum_recent,
            config=config["dayofweek"],
            percent=True,
            workdir=workdir,
            filename="dayofweek_sum_recent.png"
        )

        dayofweek_mean_full = data.groupby(
            data["date"].dt.dayofweek
        )["count"].mean().rename(
            index=lambda x: config["dayofweek"]["label"][x]
        )

        dayofweek_mean_full_src = self._generate_barplot_axes(
            series=dayofweek_mean_full,
            config=config["dayofweek"],
            percent=False,
            workdir=workdir,
            filename="dayofweek_mean_full.png"
        )

        month_sum_recent = data[
            max(-365, -total_dates):
        ].groupby(
            data["date"].dt.month
        )["count"].sum().rename(
            index=lambda x: config["month"]["label"][x]
        )

        month_sum_recent_src = self._generate_barplot_axes(
            series=month_sum_recent,
            config=config["month"],
            percent=True,
            workdir=workdir,
            filename="month_sum_recent.png"
        )

        month_mean_full = data.groupby(
            data["date"].dt.month
        )["count"]

        days_per_month = pd.Series([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]).combine(
            month_mean_full.count(), min, fill_value=0
        )

        month_mean_full = month_mean_full.mean().multiply(
            days_per_month
        ).rename(
            index=lambda x: config["month"]["label"][x]
        )

        month_mean_full_src = self._generate_barplot_axes(
            series=month_mean_full,
            config=config["month"],
            percent=False,
            workdir=workdir,
            filename="month_mean_full.png"
        )

        os.chdir("..")

        return dedent(f"""
            ## {config["section_name"]}
            | {config["count"]["title"]["sum_recent"]}         | {config["count"]["title"]["sum_full"]}          |
            |:------------------------------------------------:|:-----------------------------------------------:|
            | ![]({count_sum_recent_src})                      | ![]({count_sum_full_src})                       |
            | **{config["dayofweek"]["title"]["sum_recent"]}** | **{config["dayofweek"]["title"]["mean_full"]}** |
            | ![]({dayofweek_sum_recent_src})                  | ![]({dayofweek_mean_full_src})                  |
            | **{config["month"]["title"]["sum_recent"]}**     | **{config["month"]["title"]["mean_full"]}**     |
            | ![]({month_sum_recent_src})                      | ![]({month_mean_full_src})                      |
        """)
