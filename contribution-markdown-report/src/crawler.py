import pandas as pd
from bs4 import BeautifulSoup

from date import Date, DateInterval
from request import Request


class Crawler:
    @staticmethod
    def execute(user: str, interval: DateInterval) -> pd.DataFrame:
        data = []
        for year in interval.iter_year():
            url = f"https://github.com/{user}?from={year}-01-01"
            text = Request.fetch(url)

            for rect in BeautifulSoup(text, "html.parser").findAll("rect"):
                rect_date, rect_count = rect["data-date"], rect["data-count"]

                if Date(rect_date) in interval:
                    column = [
                        pd.to_numeric(rect_count),
                        pd.Timestamp(rect_date),
                    ]

                    data.append(column)

        return pd.DataFrame(data=data, columns=["count", "date"])
