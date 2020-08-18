import pandas as pd

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from requests import get


class RequestException(Exception):
    pass


def crawl_data(username: str, start_date_str: str) -> pd.DataFrame:
    end = datetime.today() - timedelta(days=1)
    end_date_str = end.strftime("%Y-%m-%d")

    dates = pd.date_range(start_date_str, end, name="date")
    counts = []

    for year in range(int(start_date_str[:4]), end.year + 1):
        response = get(f"https://github.com/{username}?from={year}-01-01")

        status = response.status_code
        if status != 200:
            raise RequestException(f"status code : {status}")

        counts.extend(
            map(
                lambda x: int(x["data-count"]),
                filter(
                    lambda x: start_date_str <= x["data-date"] <= end_date_str,
                    BeautifulSoup(
                        response.text, "html.parser").select(".day")
                )
            )
        )

    return pd.DataFrame({
        "count": counts,
        "date": dates,
    })
