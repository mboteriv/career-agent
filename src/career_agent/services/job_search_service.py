from career_agent.models.job_search_criteria import JobSearchCriteria
from career_agent.models.job_offer import JobOffer
from career_agent.repositories.job_offer_repository import (
    JobOfferRepository,
)


class JobSearchService:

    def __init__(
        self,
        repository=None,
    ) -> None:

        self._repository = (
            repository
            or JobOfferRepository()
        )

    def search(
        self,
        criteria: JobSearchCriteria,
    ) -> list[JobOffer]:

        return self._repository.search(
            criteria,
        )