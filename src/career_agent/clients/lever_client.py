import requests


class LeverClient:

    BASE_URL = "https://api.lever.co/v0"

    def __init__(self) -> None:
        self._session = requests.Session()

    def get_jobs(
        self,
        company: str,
    ) -> dict:
        response = self._session.get(
            f"{self.BASE_URL}/postings/{company}",
            timeout=10,
        )
        response.raise_for_status()

        return response.json()