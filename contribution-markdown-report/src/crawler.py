import pandas as pd
from bs4 import BeautifulSoup

from date import DateInterval
from request import fetch_text


def crawl_data(user: str, interval: DateInterval) -> pd.DataFrame:
    data = []
    for year in interval.iter_year():
        url = f"https://github.com/{user}?from={year}-01-01"
        text = fetch_text(url)

        for rect in BeautifulSoup(text, "html.parser").findAll("rect"):
            if interval.is_between(rect["data-date"]):
                data.append([int(rect["data-count"]), pd.Timestamp(rect["data-date"])])

    return pd.DataFrame(data=data, columns=["count", "date"])
