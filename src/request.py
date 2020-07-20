import requests

from bs4 import BeautifulSoup
from typing import Any, Dict, List


def request_github_commit(username: str) -> List[Dict[str, Any]]:
    response = requests.get(f"https://github.com/{username}")
    soup = BeautifulSoup(response.text, "html.parser")
    info = soup.select(".day")
    return info
