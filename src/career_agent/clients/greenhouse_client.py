import requests


class GreenhouseClient:

    BASE_URL = "https://boards-api.greenhouse.io/v1"

    def __init__(self) -> None:
        self._session = requests.Session()

    def get_jobs(
        self,
        board: str,
    ) -> dict:

        response = self._session.get(
            f"{self.BASE_URL}/boards/{board}/jobs",
            timeout=10,
        )

        response.raise_for_status()

        return response.json()