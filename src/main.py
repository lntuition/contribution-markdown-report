import sys
import traceback

from functools import reduce

from lib.collect.crawler import crawl_data
from lib.language.factory import FactoryLanguageSetting
from lib.section.graph import GraphGenerator
from lib.section.header import HeaderGenerator
from lib.section.summary import SummaryGenerator
from lib.util.directory import change_workdir


if __name__ == "__main__":
    try:
        _, username, start, end, workdir = sys.argv

        # Setup
        data = crawl_data(username=username, start=start, end=end)
        setting = FactoryLanguageSetting().get_setting(language="english")

        # Generate
        with change_workdir(workdir), open("README.md", "w") as fp:
            fp.write(
                reduce(
                    lambda a, b: a + b,
                    map(
                        lambda x: x.generate(),
                        [
                            HeaderGenerator(
                                username=username,
                                setting=setting,
                            ),
                            SummaryGenerator(
                                data=data,
                                setting=setting,
                            ),
                            GraphGenerator(
                                data=data,
                                setting=setting,
                            )
                        ]
                    )
                )
            )

        sys.exit(0)
    except Exception:
        traceback.print_exc()

        sys.exit(1)
