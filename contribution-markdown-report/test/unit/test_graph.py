import os
from typing import List
from unittest.mock import MagicMock, patch

import pytest
import seaborn
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from pandas import Series

from src.graph import Barplot, BarplotAxesBuilder


class TestBarplotAxesBuilder:
    @staticmethod
    def barplot_axes(index: List[int], data: List[int]) -> Axes:
        return BarplotAxesBuilder.build(
            series=Series(
                index=index,
                data=data,
            )
        )

    @patch("seaborn.set_theme")
    def test_build(self, mock_set_theme: MagicMock) -> None:
        index = [7, 8, 9, 10, 11]
        data = [23, 0, 13, 42, 38]

        barplot_axes = self.barplot_axes(index=index, data=data)

        assert ["7", "8", "9", "10", "11"] == [xticklabel.get_text() for xticklabel in barplot_axes.get_xticklabels()]
        assert data == [patch.get_height() for patch in barplot_axes.patches]

        assert not barplot_axes.spines["right"].get_visible()
        assert not barplot_axes.spines["top"].get_visible()


class TestBarplot:
    @staticmethod
    def barplot(index: List[int] = [0, 1], data: List[int] = [2, 3]) -> Barplot:
        figure = Figure(tight_layout=True)
        axes = figure.add_subplot()

        seaborn.barplot(x=index, y=data, ax=axes)

        return Barplot(axes=axes)

    def test_set_xticklabels(self) -> None:
        index = [5, 4, 3, 2, 1]
        data = [23, 0, 13, 42, 38]
        labels = ["zero", "one", "two", "three", "four", "five", "six"]

        barplot = self.barplot(index=index, data=data)
        barplot.set_xticklabels(labels=labels)

        assert ["one", "two", "three", "four", "five"] == barplot.get_xticklabels()

    def test_set_xlabel(self) -> None:
        xlabel = "xlabel"

        barplot = self.barplot()
        barplot.set_xlabel(label=xlabel)

        assert xlabel == barplot.get_xlabel()

    def test_set_ylabel(self) -> None:
        ylabel = "ylabel"

        barplot = self.barplot()
        barplot.set_ylabel(label=ylabel)

        assert ylabel == barplot.get_ylabel()

    def test_set_annotations(self) -> None:
        index = [1, 2, 3, 4, 5]
        data = [23.256, 23.254, 0, 1, 19]

        barplot = self.barplot(index=index, data=data)
        barplot.set_annotations()

        assert ["23.26", "23.25", "1", "19"] == barplot.get_annotations()

    @pytest.mark.usefixtures("fake_root")
    def test_save(self) -> None:
        file_name = "file_name.png"

        barplot = self.barplot()
        barplot.save(file_name=file_name)

        assert os.path.isfile(file_name)
