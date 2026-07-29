import requests

from app.config.config import REQUEST_TIMEOUT, USER_AGENT


class WebsiteFetcher:

    def fetch(self, url: str) -> str:
        response = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        return response.text