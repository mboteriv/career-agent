from career_agent.clients.lever_client import LeverClient
from career_agent.models.source_job_offer import SourceJobOffer
from career_agent.models.enums import Source


class LeverCollector:
    def __init__(self, client=None):
        self.client = client or LeverClient()

    def collect(self, payload):
        return [SourceJobOffer(source=Source.LEVER,raw_data=job) for job in payload]