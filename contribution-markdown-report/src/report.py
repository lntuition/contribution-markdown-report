from typing import Iterable, Sequence

from setting import Setting
from util import safe_chdir
from writer import Writer


class Report:
    @staticmethod
    def generate(
        writers: Sequence[Writer], settings: Iterable[Setting], path: str, file_name: str = "README.md"
    ) -> None:
        setting_dict = {}
        for setting in settings:
            key = setting.get_attribute()
            setting_dict[key] = setting

        text = ""
        for writer in writers:
            key = writer.get_attribute()
            setting = setting_dict[key]

            writer.generate(setting=setting)

        with safe_chdir(path), open(file_name, "w") as report:
            report.write(text)
