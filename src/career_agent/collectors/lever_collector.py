from career_agent.clients.lever_client import LeverClient
from career_agent.models.enums import Source
from career_agent.models.source_job_offer import SourceJobOffer


class LeverCollector:
    def __init__(self, client=None):
        self.client = client or LeverClient()

    def collect(
        self,
        payload,
        metadata=None,
    ):
        metadata = metadata or {}

        return [
            SourceJobOffer(
                source=Source.LEVER,
                raw_data=job,
                metadata=metadata,
            )
            for job in payload
        ]

    def collect_from_api(
        self,
        board: str,
    ):
        payload = self.client.get_jobs(board)

        return self.collect(
            payload,
            metadata={
                "company_name": board.title(),
                "board": board,
            },
        )