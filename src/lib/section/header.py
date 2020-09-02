from textwrap import dedent

from lib.language.base import LanguageSetting
from lib.section.base import SectionGenerator


class HeaderGenerator(SectionGenerator):
    def __init__(self, username: str, setting: LanguageSetting) -> None:
        super().__init__(setting=setting)
        self.username = username

    def generate(self) -> str:
        repo_url = "https://github.com/lntuition/contribution-markdown-report"

        greeting = self.setting.header_greeting(
            username=self.username
        )
        notice = self.setting.header_notice(
            repo_url=repo_url,
            issue_url=f"{repo_url}/issues"
        )

        return dedent(f"""
            # {greeting}
            {notice} :airplane:
        """)
