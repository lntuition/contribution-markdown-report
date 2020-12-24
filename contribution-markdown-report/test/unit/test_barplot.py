import os

import pytest
from pandas import Series

from src.barplot import Barplot


def __barplot() -> Barplot:
    return Barplot(
        series=Series(
            index=[1, 2, 3, 4, 5],
            data=[23.256, 23.254, 0, 1, 19],
        ),
    )


def test_barplot_set_xticklabels() -> None:
    barplot = __barplot().set_xticklabels(
        labels=["zero", "one", "two", "three", "four", "five", "six"],
    )

    assert ["one", "two", "three", "four", "five"] == barplot.get_xticklabels()


def test_barplot_set_xlabel() -> None:
    barplot = __barplot().set_xlabel("xlabel")

    assert "xlabel" == barplot.get_xlabel()


def test_barplot_set_ylabel() -> None:
    barplot = __barplot().set_ylabel("ylabel")

    assert "ylabel" == barplot.get_ylabel()


def test_barplot_set_annotations() -> None:
    barplot = __barplot().set_annotations()

    assert ["23.26", "23.25", "1", "19"] == barplot.get_annotations()


@pytest.mark.usefixtures("use_temporary_path")
def test_barplot_save() -> None:
    __barplot().save("BARPLOT")

    assert os.path.isfile("BARPLOT.png")
