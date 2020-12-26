import os
from typing import List

import pandas as pd
import pytest

from src.extractor import Extractor
from src.writer import Writer


def __writer() -> Writer:
    return Writer(
        extractor=Extractor(
            user="lntuition",
            df=pd.DataFrame(
                {
                    "count": [0],
                    "date": pd.date_range(
                        start="2010-12-25",
                        end="2010-12-25",
                    ),
                }
            ),
        ),
        skeleton_string_map={
            "header-section": "header-section {user}",
            "repository": "repository {link}",
            "repository-title": "repository-title",
            "issue": "issue {link}",
            "issue-title": "issue-title",
            "summary-section": "summary-section",
            "today": "today {date} {count} {length}",
            "today-peak": "today-peak {start} {length}",
            "max": "max {date} {count}",
            "max-peak": "max-peak {start} {end} {length}",
            "total": "total {sum} {avg}",
            "graph-section": "graph-section",
            "count-sum-recent": "count-sum-recent",
            "count-sum-full": "count-sum-full",
            "dayofweek-sum-recent": "dayofweek-sum-recent",
            "dayofweek-mean-full": "dayofweek-mean-full",
            "month-sum-recent": "month-sum-recent",
            "year-sum-full": "year-sum-full",
            "contribution-count": "contribution-count",
            "day": "day",
            "dayofweek": "dayofweek",
            "month": "month",
            "year": "year",
        },
        skeleton_list_map={
            "dayofweek": ["zero", "one", "two", "three", "four", "five", "six"],
            "month": ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven"],
        },
    )


def __expected_write() -> List[str]:
    return [
        "# header-section lntuition",
        "repository [repository-title](https://github.com/lntuition/contribution-markdown-report).",
        "issue [issue-title](https://github.com/lntuition/contribution-markdown-report/issues).",
        "## summary-section",
        "today **2010-12-25** **0** **1**. :+1:",
        "max **2010-12-25** **0**. :muscle:",
        "total **0** **0.0**. :clap:",
        "today-peak **2010-12-25** **0**. :walking:",
        "max-peak **2010-12-25** **2010-12-25** **0**. :running:",
        "## graph-section",
        "|        **count-sum-recent**         |         **count-sum-full**         |",
        "|:-----------------------------------:|:----------------------------------:|",
        "|   ![](asset/count-sum-recent.png)   |   ![](asset/count-sum-full.png)    |",
        "|      **dayofweek-sum-recent**       |      **dayofweek-mean-full**       |",
        "| ![](asset/dayofweek-sum-recent.png) | ![](asset/dayofweek-mean-full.png) |",
        "|        **month-sum-recent**         |         **year-sum-full**          |",
        "|   ![](asset/month-sum-recent.png)   |    ![](asset/year-sum-full.png)    |",
    ]


@pytest.mark.usefixtures("use_temporary_path")
def test_write() -> None:
    keys = [
        "count-sum-recent",
        "count-sum-full",
        "dayofweek-sum-recent",
        "dayofweek-mean-full",
        "month-sum-recent",
        "year-sum-full",
    ]

    __writer().write(file_name="README")

    assert os.path.isfile("README.md")
    for key in keys:
        assert os.path.isfile(
            "asset/{}.png".format(key),
        )

    with open("README.md", "r") as fp:
        assert __expected_write() == fp.read().split("\n")
