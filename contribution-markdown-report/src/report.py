from typing import Sequence

from section.base import Section
from util import safe_chdir


class Report:
    @staticmethod
    def generate(sections: Sequence[Section], path: str, file_name: str = "README.md") -> None:
        with safe_chdir(path):
            text = ""
            for section in sections:
                text += section.write()

            with open(file_name, "w") as report:
                report.write(text)
