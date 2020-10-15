from typing import Sequence

from .contribution import ContributionInfo
from .markdown import MarkdownSection


class Report:
    def __init__(self, sections: Sequence[MarkdownSection], info: ContributionInfo, file_name: str) -> None:
        self.__sections = sections
        self.__info = info
        self.__file_name = file_name

    def get_brief(self) -> str:
        return self.__info.brief

    def generate(self) -> None:
        with open(self.__file_name, "w") as report:
            for section in self.__sections:
                text = section.write(info=self.__info)
                report.write(text)
