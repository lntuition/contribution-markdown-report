import argparse
import sys
import traceback
from functools import reduce

from crawler import crawl_data
from directory import change_workdir
from language.factory import language_setting_factory
from section.graph import GraphGenerator
from section.header import HeaderGenerator
from section.summary import SummaryGenerator

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Contribution report generator")
        parser.add_argument("username", type=str, metavar="Username", help="User who created report")
        parser.add_argument("language", type=str, metavar="Language", help="Language used in report")
        parser.add_argument("start", type=str, metavar="Start", help="Start date in report")
        parser.add_argument("finish", type=str, metavar="Finish", help="Finish date in report")
        parser.add_argument("workdir", type=str, metavar="Workdir", help="Directory where report will be generated")

        # Setup
        args = parser.parse_args()
        data = crawl_data(username=args.username, start=args.start, finish=args.finish)
        setting = language_setting_factory(language=args.language)

        # Generate
        with change_workdir(args.workdir), open("README.md", "w") as fp:
            fp.write(
                reduce(
                    lambda a, b: a + b,
                    map(
                        lambda x: x.generate(),
                        [
                            HeaderGenerator(
                                username=args.username,
                                setting=setting,
                            ),
                            SummaryGenerator(
                                data=data,
                                setting=setting,
                            ),
                            GraphGenerator(
                                data=data,
                                setting=setting,
                            ),
                        ],
                    ),
                )
            )

        sys.exit(0)
    except Exception:
        traceback.print_exc()

        sys.exit(1)
