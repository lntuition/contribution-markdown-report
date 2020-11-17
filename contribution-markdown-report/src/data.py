from dataclasses import dataclass

import pandas as pd
from bs4 import BeautifulSoup

from src.date import dateBuilder, dateRange
from src.request import Request


@dataclass(frozen=True)
class ContributionData:
    user: str
    df: pd.DataFrame


class ContributionDataBuilder:
    @staticmethod
    def build(user: str, date_range: dateRange) -> ContributionData:
        data = []
        for year in date_range.iter_year():
            url = f"https://github.com/{user}"
            params = {
                "from": f"{year}-01-01",
            }

            text = Request.fetch_text(url, params)
            rects = BeautifulSoup(text, "html.parser").findAll("rect")

            for rect in rects:
                data_date = rect["data-date"]
                data_count = rect["data-count"]

                if dateBuilder.build(data_date) in date_range:
                    data.append(
                        [
                            pd.Timestamp(data_date),
                            pd.to_numeric(data_count),
                        ]
                    )

        return ContributionData(
            user=user,
            df=pd.DataFrame(
                data=data,
                columns=["date", "count"],
            ),
        )
