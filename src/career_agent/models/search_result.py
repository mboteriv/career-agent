from pydantic import BaseModel, ConfigDict

from career_agent.models.job_offer import JobOffer


class SearchResult(BaseModel):

    model_config = ConfigDict(frozen=True)

    jobs: list[JobOffer]

    total: int

    page: int

    page_size: int