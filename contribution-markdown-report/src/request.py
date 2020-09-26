import requests


class RequestException(Exception):
    pass


def fetch_raw_text(url: str) -> str:
    response = requests.get(url)

    status = response.status_code
    if status != 200:
        raise RequestException(f"{status} : fail request")

    return response.text
