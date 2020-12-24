from datetime import date

import pandas as pd
from bs4 import BeautifulSoup

from src.date import DateRange
from src.extractor import Extractor
from src.request import Request


class Collector:
    @staticmethod
    def collect(user: str, date_range: DateRange) -> Extractor:
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

                if date.fromisoformat(data_date) in date_range:
                    data.append(
                        [
                            pd.Timestamp(data_date),
                            pd.to_numeric(data_count),
                        ]
                    )

        return Extractor(
            user=user,
            df=pd.DataFrame(
                data=data,
                columns=["date", "count"],
            ),
        )
