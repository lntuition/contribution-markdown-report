import os
from unittest.mock import MagicMock

import pytest

from src.markdown import MarkdownSection
from src.report import Report


class FakeMarkdownSection(MarkdownSection):
    def __init__(self, text: str) -> None:
        self.__text = text

    def write(self, info: MagicMock) -> str:
        return self.__text


class TestReport:
    def test_get_brief(self) -> None:
        mock_info = MagicMock()

        report = Report(sections=[], info=mock_info, file_name="")

        assert report.get_brief() == mock_info.brief

    @pytest.mark.usefixtures("fake_root")
    def test_generate(self) -> None:
        fake_section_texts = ["First", "Second", "Third"]
        fake_sections = [FakeMarkdownSection(text) for text in fake_section_texts]
        file_name = "test_file_name"

        report = Report(sections=fake_sections, info=MagicMock(), file_name=file_name)
        report.generate()

        assert os.path.isfile(file_name)

        with open(file_name, "r") as report:
            assert report.read() == "".join(fake_section_texts)
