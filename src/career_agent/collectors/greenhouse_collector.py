from datetime import UTC, datetime

from career_agent.clients.greenhouse_client import GreenhouseClient

from career_agent.dto.source_job_offer import SourceJobOffer
from career_agent.models.enums import Source


class GreenhouseCollector:

    def __init__(self) -> None:
        self._client = GreenhouseClient()

    def collect(self, payload: dict) -> list[SourceJobOffer]:
        collected_at = datetime.now(UTC)

        return [
            SourceJobOffer(
                source=Source.GREENHOUSE,
                payload=job,
                collected_at=collected_at,
            )
            for job in payload.get("jobs", [])
        ]

    def collect_from_api(
    self,
    board: str,
) -> list[SourceJobOffer]:
        payload = self._client.get_jobs(board)

        return self.collect(payload)