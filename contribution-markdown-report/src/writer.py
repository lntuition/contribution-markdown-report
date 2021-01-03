from typing import List, Mapping

import numpy as np
from pandas import Series
from tabulate import tabulate

from .barplot import Barplot
from .extractor import Extractor
from .markdown import MarkdownBuilder
from .util import change_path


class Writer:
    def __init__(
        self,
        extractor: Extractor,
        skeleton_string_map: Mapping[str, str],
        skeleton_list_map: Mapping[str, List[str]],
    ) -> None:
        self.__extractor = extractor
        self.__skeleton_string_map = skeleton_string_map
        self.__skeleton_list_map = skeleton_list_map

    def __header(self) -> str:
        text = str(
            MarkdownBuilder(
                expr=self.__skeleton_string_map["header-section"],
                fmt={
                    "user": self.__extractor.fetch_user(),
                },
            ).to_heading(level=1),
        )
        text += str(
            MarkdownBuilder(
                expr=self.__skeleton_string_map["repository"],
                fmt={
                    "link": MarkdownBuilder(
                        expr=self.__skeleton_string_map["repository-title"],
                        end="",
                    ).link_url("https://github.com/lntuition/contribution-markdown-report"),
                },
                end=".\n",
            ),
        )
        text += str(
            MarkdownBuilder(
                expr=self.__skeleton_string_map["issue"],
                fmt={
                    "link": MarkdownBuilder(
                        expr=self.__skeleton_string_map["issue-title"],
                        end="",
                    ).link_url("https://github.com/lntuition/contribution-markdown-report/issues"),
                },
                end=".\n",
            ),
        )

        return text

    def __summary(self) -> str:
        text = str(
            MarkdownBuilder(
                expr=self.__skeleton_string_map["summary-section"],
            ).to_heading(level=2),
        )

        seqs_key = ["today", "max", "total", "today-peak", "max-peak"]
        seqs_expr = ["+1", "muscle", "clap", "walking", "running"]
        for seq_key, seq_expr in zip(seqs_key, seqs_expr):
            fmt = {}
            for fmt_key, fmt_val in self.__extractor.fetch_map(seq_key).items():
                fmt[fmt_key] = MarkdownBuilder(
                    expr=fmt_val,
                    end="",
                ).to_bold()

            text += str(
                MarkdownBuilder(
                    expr=self.__skeleton_string_map[seq_key],
                    fmt=fmt,
                    end=". ",
                ).to_list(is_ordered=False),
            )
            text += str(
                MarkdownBuilder(seq_expr).to_emoji(),
            )

        return text

    def __barplot_based_count(self, series: Series) -> Barplot:
        return (
            Barplot(series)
            .set_xlabel(self.__skeleton_string_map["contribution-count"])
            .set_ylabel(self.__skeleton_string_map["day"])
            .set_annotations()
        )

    def __barplot_based_dayofweek(self, series: Series) -> Barplot:
        return (
            Barplot(series)
            .set_xticklabels(self.__skeleton_list_map["dayofweek"])
            .set_xlabel(self.__skeleton_string_map["dayofweek"])
            .set_ylabel(self.__skeleton_string_map["contribution-count"])
            .set_annotations()
        )

    def __barplot_based_month(self, series: Series) -> Barplot:
        return (
            Barplot(series)
            .set_xticklabels(self.__skeleton_list_map["month"])
            .set_xlabel(self.__skeleton_string_map["month"])
            .set_ylabel(self.__skeleton_string_map["contribution-count"])
            .set_annotations()
        )

    def __barplot_based_year(self, series: Series) -> Barplot:
        return (
            Barplot(series)
            .set_xlabel(self.__skeleton_string_map["year"])
            .set_ylabel(self.__skeleton_string_map["contribution-count"])
            .set_annotations()
        )

    def __graph(self) -> str:
        text = str(
            MarkdownBuilder(
                expr=self.__skeleton_string_map["graph-section"],
            ).to_heading(level=2)
        )

        table = []
        seqs_map = {
            "count-sum-recent": self.__barplot_based_count(
                series=self.__extractor.fetch_cut(
                    length=28,
                ),
            ),
            "dayofweek-sum-recent": self.__barplot_based_dayofweek(
                series=self.__extractor.fetch_series(
                    group="dayofweek",
                    combinator="sum",
                    length=112,
                ),
            ),
            "month-sum-recent": self.__barplot_based_month(
                series=self.__extractor.fetch_series(
                    group="month",
                    combinator="sum",
                ),
            ),
            "count-sum-full": self.__barplot_based_count(
                series=self.__extractor.fetch_cut(),
            ),
            "dayofweek-mean-full": self.__barplot_based_dayofweek(
                series=self.__extractor.fetch_series(
                    group="dayofweek",
                    combinator="mean",
                ),
            ),
            "year-sum-full": self.__barplot_based_year(
                series=self.__extractor.fetch_series(
                    group="year",
                    combinator="sum",
                ),
            ),
        }
        for seq_key, seq_val in seqs_map.items():
            table.append(
                MarkdownBuilder(
                    expr=self.__skeleton_string_map[seq_key],
                    end="",
                ).to_bold(),
            )

            table.append(
                MarkdownBuilder(expr="",).link_image(
                    path="asset/{}.png".format(seq_key),
                ),
            )

            with change_path("asset"):
                seq_val.save(seq_key)

        text += tabulate(
            np.reshape(table, (-1, 2), order="F"),
            headers="firstrow",
            tablefmt="pipe",
            colalign=["center", "center"],
        )

        return text

    def write(self, file_name: str) -> None:
        text = self.__header() + self.__summary() + self.__graph()
        with open(file_name + ".md", "w") as fp:
            fp.write(text)
