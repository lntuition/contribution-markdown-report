from functools import reduce
from pandas import DataFrame

from lib.language.factory import FactoryLanguageSetting
from lib.section.graph import GraphGenerator
from lib.section.header import HeaderGenerator
from lib.section.summary import SummaryGenerator
from lib.util.directory import change_workdir


class ReportWriter():
    def __init__(self, username: str, data: DataFrame, language: str) -> None:
        self.username = username
        self.data = data
        self._set_language(language=language)

    def _set_language(self, language: str) -> None:
        self.language = language
        self.setting = FactoryLanguageSetting().create_setting(language=language)

    def change_language(self, language: str) -> None:
        if language != self.language:
            self._set_language(language=language)

    def _generate_report(self) -> str:
        return reduce(
            lambda a, b: a + b,
            map(
                lambda x: x.generate(),
                [
                    HeaderGenerator(
                        username=self.username,
                        setting=self.setting,
                    ),
                    SummaryGenerator(
                        data=self.data,
                        setting=self.setting,
                    ),
                    GraphGenerator(
                        data=self.data,
                        setting=self.setting,
                    )
                ]
            )
        )

    def write(self, workdir: str, filename: str) -> None:
        with change_workdir(workdir), open(filename, "w") as fp:
            fp.write(self._generate_report())
