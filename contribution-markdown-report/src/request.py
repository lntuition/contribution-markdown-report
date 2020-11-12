from typing import Dict, Optional

import requests


class Request:
    @staticmethod
    def fetch_text(
        url: str,
        params: Optional[Dict[str, str]] = None,
    ) -> str:
        response = requests.get(url, params)

        status = response.status_code
        if status != 200:
            raise Exception(f"{status} : Failed to get text")

        return response.text
