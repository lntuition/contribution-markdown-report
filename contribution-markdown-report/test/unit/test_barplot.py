import os

import pytest
import seaborn
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from pandas import Series

from src.barplot import Barplot, BarplotAxesBuilder


def test_barplot_axes_build() -> None:
    barplot_axes = BarplotAxesBuilder.build(
        series=Series(
            index=[7, 8, 9, 10, 11],
            data=[23, 0, 13, 42, 38],
        )
    )

    assert ["7", "8", "9", "10", "11"] == [xticklabel.get_text() for xticklabel in barplot_axes.get_xticklabels()]
    assert [23, 0, 13, 42, 38] == [patch.get_height() for patch in barplot_axes.patches]

    assert not barplot_axes.spines["right"].get_visible()
    assert not barplot_axes.spines["top"].get_visible()


def __barplot() -> Barplot:
    return Barplot(
        axes=seaborn.barplot(
            x=[1, 2, 3, 4, 5],
            y=[23.256, 23.254, 0, 1, 19],
            ax=Figure(
                tight_layout=True,
            ).add_subplot(),
        ),
    )


def test_barplot_set_xticklabels() -> None:
    barplot = __barplot()
    barplot.set_xticklabels(
        labels=["zero", "one", "two", "three", "four", "five", "six"],
    )

    assert ["one", "two", "three", "four", "five"] == barplot.get_xticklabels()


def test_barplot_set_xlabel() -> None:
    barplot = __barplot()
    barplot.set_xlabel("xlabel")

    assert "xlabel" == barplot.get_xlabel()


def test_barplot_set_ylabel() -> None:
    barplot = __barplot()
    barplot.set_ylabel("ylabel")

    assert "ylabel" == barplot.get_ylabel()


def test_barplot_set_annotations() -> None:
    barplot = __barplot()
    barplot.set_annotations()

    assert ["23.26", "23.25", "1", "19"] == barplot.get_annotations()


@pytest.mark.usefixtures("use_temporary_path")
def test_barplot_save() -> None:
    __barplot().save("BARPLOT")

    assert os.path.isfile("BARPLOT.png")
