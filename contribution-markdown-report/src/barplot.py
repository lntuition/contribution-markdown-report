from typing import List

import seaborn
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.text import Annotation
from pandas import Series


class BarplotAxesBuilder:
    @staticmethod
    def build(
        series: Series,
        *,
        style: str = "whitegrid",
        palette: str = "pastel",
    ) -> Axes:
        figure = Figure(tight_layout=True)
        axes = figure.add_subplot()

        seaborn.set_theme(style=style, palette=palette)
        seaborn.barplot(x=series.index, y=series, ax=axes)
        seaborn.despine(ax=axes)

        return axes


class Barplot:
    def __init__(self, axes: Axes) -> None:
        self.__axes = axes

    def get_xticklabels(self) -> List[str]:
        return [xticklabel.get_text() for xticklabel in self.__axes.get_xticklabels()]

    def get_xlabel(self) -> str:
        return self.__axes.get_xlabel()

    def get_ylabel(self) -> str:
        return self.__axes.get_ylabel()

    def get_annotations(self) -> List[str]:
        return [child.get_text() for child in self.__axes.get_children() if isinstance(child, Annotation)]

    def set_xticklabels(self, labels: List[str]) -> None:
        xticklabels = self.__axes.get_xticklabels()

        for xticklabel in xticklabels:
            old_text = xticklabel.get_text()

            idx = int(old_text)
            new_text = labels[idx]

            xticklabel.set_text(new_text)

        self.__axes.set_xticklabels(xticklabels)

    def set_xlabel(self, label: str) -> None:
        self.__axes.set_xlabel(label)

    def set_ylabel(self, label: str) -> None:
        self.__axes.set_ylabel(label)

    def set_annotations(
        self,
        *,
        ha: str = "center",
        va: str = "bottom",
    ) -> None:
        for patch in self.__axes.patches:
            x = patch.get_x()
            y = patch.get_y()

            height = patch.get_height()
            width = patch.get_width()

            if round(height, 2) != 0:
                self.__axes.annotate(
                    text=f"{height:.0f}" if height.is_integer() else f"{height:.2f}",
                    xy=(x + width / 2, y + height * 1.025),
                    ha=ha,
                    va=va,
                )

    def save(self, file_name: str) -> None:
        figure = self.__axes.get_figure()
        figure.savefig(file_name + ".png")
